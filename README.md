# tgbot_02_teleton
Commands for run taskiq: 
taskiq worker core.taskiq_broker:broker --fs-discover --tasks-pattern "**/tasks.py" --workers 1 --no-configure-logging
taskiq scheduler core.taskiq_broker:scheduler --skip-first-run

alembic init -t async migrations
alembic revision --autogenerate -m 'initial'
