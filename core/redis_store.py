from redis.asyncio import Redis


class AsyncNamespacedRedis:
    def __init__(self, namespace: str, redis_client: Redis = None):
        self.namespace = namespace
        self.redis = redis_client or Redis(
            host='localhost',
            port=6379,
            decode_responses=True
        )

    def _make_key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    async def set(self, key: str, value: str, **kwargs):
        return await self.redis.set(self._make_key(key), value, **kwargs)

    async def get(self, key: str):
        return await self.redis.get(self._make_key(key))

    async def hset(self, key: str, mapping: dict = None, **kwargs):
        return await self.redis.hset(self._make_key(key), mapping=mapping, **kwargs)

    async def hgetall(self, key: str):
        return await self.redis.hgetall(self._make_key(key))

    async def delete(self, key: str):
        return await self.redis.delete(self._make_key(key))

    async def exists(self, key: str):
        return await self.redis.exists(self._make_key(key))

    async def keys(self, pattern: str = "*"):
        return await self.redis.keys(self._make_key(pattern))

    async def incr(self, key: str):
        return await self.redis.incr(self._make_key(key))

    async def expire(self, key: str, time: int):
        return await self.redis.expire(self._make_key(key), time)

    async def close(self):
        await self.redis.close()