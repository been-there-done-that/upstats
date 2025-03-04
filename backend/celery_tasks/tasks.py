import logging

from base import app
from database import SessionLocal
from models import Events

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
    return dict(status='ok')


@app.on_after_configure.connect
def task_initializer(*args, **kwargs):  # noqa
    app.add_periodic_task(5.0, add.s(2, 3), name="add-every-5-seconds")
    app.add_periodic_task(10.0, basic_thingy.s({'a': 2, 'b': 3}), name="basic-thingy-every-5-seconds")
