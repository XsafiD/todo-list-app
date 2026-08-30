#!/usr/bin/env bash
set -euo pipefail

# Tunggu DB siap — healthcheck mysql bisa lolos saat init server sementara
# (pertama kali volume dibuat), alembic yang jalan terlalu cepat akan ditolak.
echo "→ Waiting for database..."
python - <<'PY'
import os, sys, time
import pymysql

for attempt in range(30):
    try:
        pymysql.connect(
            host=os.environ.get("DB_HOST", "mysql"),
            port=int(os.environ.get("DB_PORT", "3306")),
            user=os.environ.get("DB_USER", "dashboardku"),
            password=os.environ.get("DB_PASS", ""),
            database=os.environ.get("DB_NAME", "dashboardku"),
        )
        sys.exit(0)
    except pymysql.MySQLError:
        time.sleep(2)
sys.exit("Database tidak tersedia setelah 60 detik.")
PY

echo "→ Running migrations..."
alembic upgrade head

echo "→ Starting application..."
exec gunicorn --bind 0.0.0.0:5000 \
     --workers 1 --threads 4 \
     --timeout 120 \
     --access-logfile - \
     "app:create_app()"