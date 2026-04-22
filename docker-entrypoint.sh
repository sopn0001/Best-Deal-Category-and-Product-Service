#!/bin/sh
# Wait for MongoDB, then seed if the database is empty (seed_data.py exits 0 when data already exists).

if [ "${RUN_SEED:-true}" = "false" ]; then
  echo "RUN_SEED=false — skipping seed_data.py"
  exec uvicorn main:app --host 0.0.0.0 --port 5001
fi

echo "Waiting for MongoDB at ${MONGO_URL:-mongodb://localhost:27017} …"
while true; do
  if python seed_data.py; then
    break
  fi
  echo "seed_data.py failed (Mongo likely not ready). Retrying in 3s…"
  sleep 3
done

exec uvicorn main:app --host 0.0.0.0 --port 5001
