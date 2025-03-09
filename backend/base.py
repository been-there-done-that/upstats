from celery import Celery
import logging
from dotenv import load_dotenv
import os

load_dotenv()


REDIS_URL = f"{os.getenv('REDIS_URL')}/0"
DATABASE_URL = f"postgresql://{os.getenv('USER_NAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DBNAME')}"

app = Celery(
    "upstats",
    broker_url=REDIS_URL,
    result_backend=f"db+{DATABASE_URL}",
    database_create_tables_at_setup=True,
    broker_connection_retry_on_startup=True,
    timezone="UTC",
    beat_schedule={},
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
