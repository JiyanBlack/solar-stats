wait-port solar-stats-postgres15:5432
cron
uvicorn backend.main:app --host 0.0.0.0 --port 3000 --reload