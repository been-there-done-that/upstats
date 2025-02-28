import datetime
import uuid
from typing import List, Optional, Dict

import httpx
import pydantic
from fastapi import FastAPI, Depends
import asyncio
import concurrent.futures
import requests
from contextlib import asynccontextmanager

from pydantic import BaseModel, model_validator
from pydantic.v1 import UUID4
from sqlalchemy import select, func, update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from choices import MethodChoices
from database import scoped_session, scoped_session_context
from models import Events, EventLogs, LastEventRuns

executor = concurrent.futures.ThreadPoolExecutor()


INTERVAL = 5


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
    task = asyncio.create_task(process_tasks())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EventCreate(BaseModel):
    name: str
    url: str
    method: MethodChoices
    frequency: int

    @model_validator(mode="after")
    def check_resource_or_contractor(cls, values):  # noqa
        if values.frequency not in [60, 300, 900, 1800, 3600, 43200, 86400]:
            raise ValueError(f"Invalid frequency provided...")
        return values

    class Config:
        use_enum_values = True


class EventUpdate(EventCreate):
    eid: str


@app.get("/api/v1/event")
def get_event(db: Session = Depends(scoped_session)):
    subquery = (
        db.query(LastEventRuns.eid, LastEventRuns.id, LastEventRuns.run_at, LastEventRuns.status_code)
        .order_by(LastEventRuns.run_at.desc())
        .subquery()
    )

    events_query = (
        db.query(
            Events.eid,
            Events.name,
            Events.url,
            Events.deleted,
            Events.frequency,
            func.array_agg(
                func.jsonb_build_object(
                    "id", subquery.c.id, "date", subquery.c.run_at, "status_code", subquery.c.status_code
                )
            ).label("beats"),
        )
        .outerjoin(subquery, Events.id == subquery.c.eid)
        .group_by(Events.id)
    )
    column_names = [desc["name"] for desc in events_query.column_descriptions]

    results = events_query.all()
    return [dict(zip(column_names, rs)) for rs in results]


@app.post("/api/v1/event")
def create_event(body: EventCreate, db: Session = Depends(scoped_session)):
    stmt_intermediate = insert(Events).values([body.model_dump()])
    stmt = stmt_intermediate.on_conflict_do_nothing()
    db.execute(stmt)
    return dict(status="ok")


@app.patch("/api/v1/event")
def update_event(body: EventUpdate, db: Session = Depends(scoped_session)):
    stmt_intermediate = insert(Events).values([body.model_dump()])
    stmt = stmt_intermediate.on_conflict_do_update(
        index_elements=["eid"],
        set_=dict(
            name=stmt_intermediate.excluded.name,
            url=stmt_intermediate.excluded.url,
            frequency=stmt_intermediate.excluded.frequency,
            method=stmt_intermediate.excluded.method,
            deleted=stmt_intermediate.excluded.deleted,
        ),
    )
    db.execute(stmt)
    return dict(status="ok")


@app.get("/api/v1/event/{eid}/logs")
def get_event(eid: str, db: Session = Depends(scoped_session)):
    today_start = func.date_trunc("day", func.current_timestamp())

    sub_results = (
        db.query(EventLogs.run_at.label("x"), EventLogs.time_took.label("y"))
        .filter(EventLogs.run_at.between(today_start, func.current_timestamp()))
        .join(Events, and_(Events.id == EventLogs.eid, Events.eid == eid))
        .order_by(EventLogs.run_at.desc())
        .all()
    )
    rows = (
        db.query(
            Events.eid,
            Events.name,
            Events.url,
            Events.deleted,
            Events.frequency,
        )
        .filter(Events.eid==eid).first()
    )
    data = dict(rows._mapping)  # noqa
    data['logs'] = [r._mapping for r in sub_results]   # noqa
    return  data


def fetch_url(event: dict):
    error = None
    time_took = 0
    status_code = 0
    start_time = datetime.datetime.now(datetime.timezone.utc)
    with httpx.Client() as client:
        try:
            response = client.send(httpx.Request(method=event["method"].upper(), url=event["url"]))
            print(event["url"], response.status_code)
            # this will convert the time we have received into milliseconds
            time_took = round(response.elapsed.total_seconds() * 1000, 2)
            status_code = response.status_code
        except httpx.ConnectError as e:
            print("Invalid URL, unable to access the url")
            error = e.__str__()

    with scoped_session_context() as db:
        db.execute(
            insert(EventLogs).values(
                dict(
                    status_code=status_code,
                    eid=event["id"],
                    run_at=start_time,
                    time_took=time_took,
                    error=error,
                    success=100 <= status_code <= 499,
                )
            )
        )


async def process_tasks():
    while True:
        with scoped_session_context() as db:
            stmt = (
                select(Events)
                .where(
                    (Events.last_run_at.is_(None))
                    | (func.extract("epoch", func.now() - Events.last_run_at) >= Events.frequency)
                )
                .order_by(Events.id)
            )
            events = [i.__dict__ for i in db.execute(stmt).scalars().all()]
        loop = asyncio.get_running_loop()
        print("Execution started", datetime.datetime.now())
        for event in events:
            print(loop.run_in_executor(executor, fetch_url, event))

        update_stmt = (
            update(Events).values(dict(last_run_at=func.now())).where(Events.id.in_([e["id"] for e in events]))
        )
        db.execute(update_stmt)
        db.commit()
        print("Execution Ended", datetime.datetime.now())
        await asyncio.sleep(INTERVAL)
