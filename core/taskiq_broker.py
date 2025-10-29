__all__ = ("broker", "redis_source", "scheduler")

import logging

from taskiq import TaskiqScheduler, TaskiqEvents, TaskiqState, Context
from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource, RedisStreamBroker, ListQueueBroker

from core.config import settings

result_backend = RedisAsyncResultBackend(
    redis_url=settings.broker.redis_url,
)

# broker = RedisStreamBroker(
broker = ListQueueBroker(
        url=settings.broker.redis_url,
).with_result_backend(result_backend)

redis_source = RedisScheduleSource(settings.broker.redis_url)
scheduler = TaskiqScheduler(broker, sources=[redis_source])

log = logging.getLogger(__name__)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    logging.basicConfig(
        level=settings.broker.log_level_value,
        format=settings.broker.log_format,
        datefmt=settings.logging.date_format,
    )
    log.info("Worker startup complete, got state: %s", state)

@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def on_worker_shutdown(state: TaskiqState):
    from core.redis_store import HealthCheckManager, CancelCheckManager
    await HealthCheckManager.clear()
    await CancelCheckManager.clear()
#