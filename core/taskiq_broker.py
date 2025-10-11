__all__ = ("broker", "redis_source", "scheduler")

import logging

from taskiq import TaskiqScheduler, TaskiqEvents, TaskiqState
from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource, RedisStreamBroker

from core.config import settings

result_backend = RedisAsyncResultBackend(
    redis_url=settings.broker.redis_url,
)

broker = RedisStreamBroker(
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

# client_for_task:TelegramClient|None = None

# @broker.on_event(TaskiqEvents.WORKER_STARTUP)
# async def startup(state: TaskiqState) -> None:
#     global client_for_task
#     tg_manager_for_worker = TelegramManager(suffix="_task")
#     client_for_task = await tg_manager_for_worker.get_client()
#     await client_for_task.start()
#     state.client = client_for_task
#     print("✅ Клиент инициализирован в воркере")
#
# @broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
# async def shutdown(state: TaskiqState) -> None:
#     client = getattr(state, "client", None)
#     if client and client.is_connected():
#         await client.disconnect()

