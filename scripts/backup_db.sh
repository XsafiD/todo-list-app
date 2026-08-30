#!/usr/bin/env bash
# Backup harian DB production → backups/db-YYYY-MM-DD.sql.gz (keep 7).
# Dipanggil manual (make backup) atau via cron — docs Deployment §5.8.
set -euo pipefail

cd "$(dirname "$0")/.."
ENV_FILE=".env.production"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "ERROR: $ENV_FILE tidak ditemukan — jalankan di server production." >&2
    exit 1
fi

set -a; source "$ENV_FILE"; set +a
: "${MYSQL_ROOT_PASSWORD:?MYSQL_ROOT_PASSWORD kosong di $ENV_FILE}"
: "${DB_NAME:?DB_NAME kosong di $ENV_FILE}"

mkdir -p backups
BACKUP_FILE="backups/db-$(date +%F).sql.gz"

docker compose -f docker-compose.prod.yml exec -T \
    -e MYSQL_PWD="$MYSQL_ROOT_PASSWORD" \
    mysql mysqldump -u root --single-transaction --routines --triggers "$DB_NAME" \
    | gzip > "$BACKUP_FILE"

# Retensi: keep 7 file terbaru
ls -1t backups/db-*.sql.gz | tail -n +8 | xargs -r rm --

echo "OK: $BACKUP_FILE ($(du -h "$BACKUP_FILE" | cut -f1))"
