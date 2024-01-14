import logging

from apps.authorization.workers.regular import storage_regular

logger = logging.getLogger(__name__)


@storage_regular.task
def example_task() -> None:
    """Пример задачи."""
    raise NotImplementedError()
