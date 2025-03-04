import logging
import datetime

import httpx
from sqlalchemy import func, select, update, insert

from base import app
from database import SessionLocal, scoped_session_context
from models import Events, EventLogs

logger = logging.getLogger(__name__)


class CelerySessionMaker(app.Task):
    def __init__(self):
        self.sessions = {}

    def before_start(self, task_id, args, kwargs):
        self.sessions[task_id] = SessionLocal()
        super().before_start(task_id, args, kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        session = self.sessions.pop(task_id)
        session.close()
        super().after_return(status, retval, task_id, args, kwargs, einfo)

    @property
    def session(self) -> SessionLocal:
        return self.sessions[self.request.id]


@app.task
def add(x, y):
    """Simple task that adds two numbers and logs the result."""
    result = x + y
    logger.info(f"Task executed: {x} + {y} = {result}")
    return result


@app.task(bind=True, base=CelerySessionMaker)
def basic_thingy(self, event):
    x = self.session.query(Events).limit(10)
    print(event, x)
    return dict(status="ok")


@app.task
def fetcher(event: dict):
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

    return dict(status="ok")


@app.on_after_configure.connect
def task_initializer(*args, **kwargs):  # noqa
    with scoped_session_context() as db:
        stmt = (
            select(Events)
            .where(
                (Events.last_run_at.is_(None))
                | (func.extract("epoch", func.now() - Events.last_run_at) >= Events.frequency)
            )
            .order_by(Events.id)
        )
        print("Execution started", datetime.datetime.now())
        for ev in db.execute(stmt).scalars().all():
            ev = ev.__dict__.copy()
            ev.pop("_sa_instance_state")
            print(ev)
            app.add_periodic_task(ev["frequency"], fetcher.s(ev), name=ev["eid"])
        print("Execution Ended", datetime.datetime.now())
