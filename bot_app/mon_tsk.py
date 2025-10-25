import asyncio
import json
from taskiq_redis import RedisAsyncResultBackend


async def inspect_all_tasks():
    result_backend = RedisAsyncResultBackend("redis://localhost:6379")

    import redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    task_keys = r.keys("taskiq:result:*")
    print(f"Found {len(task_keys)} tasks:")

    for key in task_keys:
        task_id = key.replace("taskiq:result:", "")
        result = await result_backend.get_result(task_id)

        if result:
            print(f"\n📋 Task: {task_id}")
            print(f"   Status: {result.status}")
            print(f"   Result: {result.return_value}")
            if result.error:
                print(f"   Error: {result.error}")


if __name__ == "__main__":
    asyncio.run(inspect_all_tasks())