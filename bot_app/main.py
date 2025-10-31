import asyncio
import logging
from datetime import datetime, timezone, timedelta

import aioconsole

from core.config import settings
from core.redis_store import HealthCheckManager, CancelCheckManager
from core.taskiq_broker import broker
from core.tg_client import tg_managers
from bot_app.tasks import initial_client
from data_app.crud.user import get_active_users

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


log = logging.getLogger(__name__)


async def initial_clients() -> list:
    tg_manager_for_worker = tg_managers["worker"]
    users = await get_active_users()
    tasks_list = []
    for user in users:
        client = await tg_manager_for_worker.get_client(user.phone_number)
        # log.info(await TelegramManager.get_user_chats(client))
        await tg_manager_for_worker.close_client(user.phone_number)
        task = await initial_client.kiq(
            user_id=user.id,
            phone_number=user.phone_number)
        await HealthCheckManager.set_timestamp(task.task_id)
        tasks_list.append(task.task_id)
    return tasks_list

async def check_health(task_lists: list):
    log.info("Starting health check")
    try:
        while True:
            for task in task_lists:
                last_timestamp_str = await HealthCheckManager.get(task)
                if not last_timestamp_str:
                    log.warning(f"Heartbeat timeout for task {task}: missing timestamp")
                else:
                    last_timestamp = datetime.fromisoformat(last_timestamp_str)
                    if last_timestamp.tzinfo is None:
                        last_timestamp = last_timestamp.replace(tzinfo=timezone.utc)
                    if datetime.now(timezone.utc) - last_timestamp > timedelta(seconds=settings.healthcheck.heartbeat_timeout):
                        log.warning(f"Heartbeat timeout for task {task}: {last_timestamp}")
                    else:
                        log.info(f"Health Check for task {task} ok: {last_timestamp}")
            await asyncio.sleep(settings.healthcheck.period)
    except asyncio.CancelledError:
        log.info("Background check health task cancelled")
    except Exception as e:
        log.exception("Check_health error: %s", e)
    finally:
        pass

async def main():
    monitor_for_task = None
    try:
        await broker.startup()
        tasks_list = await initial_clients()
        print(tasks_list)
        if len(tasks_list) > 0:
            log.info("Try starting health check")
            monitor_for_task = asyncio.create_task(check_health(tasks_list))


        # while True:
        #     user_input = await aioconsole.ainput("uhahah > ")
        #     if user_input.lower() in ('quit', 'exit', 'q'):
        #         break
        #     if user_input in tasks_list:
        #         await CancelCheckManager.set(user_input, 1)
        #         log.info(f"Task {user_input} removed from task list")
        #         # tasks_list.remove(user_input)


    except (KeyboardInterrupt, asyncio.CancelledError):
        log.info("Stopped by user")
    finally:
        if monitor_for_task and not monitor_for_task.done():
            monitor_for_task.cancel()
            try:
                await asyncio.wait_for(monitor_for_task, timeout=5)
            except asyncio.TimeoutError:
                log.warning("Monitor task didn't cancel in time")
            except asyncio.CancelledError:
                log.info("Monitor task cancelled successfully")
        await broker.shutdown()
        await HealthCheckManager.close()
        await CancelCheckManager.close()
        log.info("Main script done")




if __name__ == "__main__":
    asyncio.run(main())


