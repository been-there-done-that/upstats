import asyncio
import concurrent.futures
import datetime
import httpx
from sqlalchemy import select, func, update, insert

from database import scoped_session_context
from models import Events, EventLogs

INTERVAL = 5

executor = concurrent.futures.ThreadPoolExecutor()


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


if __name__ == "__main__":
    asyncio.run(process_tasks())
