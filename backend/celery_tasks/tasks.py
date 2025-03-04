import logging

from base import app


logger = logging.getLogger(__name__)


@app.task
def add(x, y):
    """Simple task that adds two numbers and logs the result."""
    result = x + y
    logger.info(f"Task executed: {x} + {y} = {result}")
    return result


@app.on_after_configure.connect
def task_initializer(*args, **kwargs):  # noqa
    app.add_periodic_task(5.0, add.s(2, 3), name="add-every-10-seconds")
