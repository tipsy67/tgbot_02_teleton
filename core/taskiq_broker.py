__all__ = ("broker", "redis_source", "scheduler")

from taskiq import TaskiqScheduler
from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource, RedisStreamBroker

from core.config import settings

# broker = AioPikaBroker(url=settings.rabbitmq.url)
#

result_backend = RedisAsyncResultBackend(
    redis_url=settings.broker.redis_url,
)

broker = RedisStreamBroker(
    url=settings.broker.redis_url,
).with_result_backend(result_backend)

redis_source = RedisScheduleSource(settings.broker.redis_url)
scheduler = TaskiqScheduler(broker, sources=[redis_source])


