import datetime
from typing import List

from fastapi import FastAPI, Depends
import asyncio
import concurrent.futures
import requests
from contextlib import asynccontextmanager

from pydantic import BaseModel, model_validator
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from choices import MethodChoices
from database import scoped_session
from models import Events

executor = concurrent.futures.ThreadPoolExecutor()

INTERVAL = 5


@asynccontextmanager
async def lifespan(app: FastAPI):
    # task = asyncio.create_task(process_tasks())
    yield
    # task.cancel()


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


@app.get("/api/v1/event", response_model=List[EventUpdate])
def get_event(db: Session = Depends(scoped_session)):
    return db.query(Events).all()


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
        index_elements=["rid"],
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


def fetch_url(url: str):
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Error fetching {url}: {e}")


async def process_tasks():
    while True:
        urls = ["https://example.com", "https://example.org"] * 1000  # Example URLs
        loop = asyncio.get_running_loop()
        print("Execution started", datetime.datetime.now())
        for url in urls:
            loop.run_in_executor(executor, fetch_url, url)
        print("Execution Ended", datetime.datetime.now())
        await asyncio.sleep(INTERVAL)
