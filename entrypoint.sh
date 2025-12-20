#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "[entrypoint] Starting: $*"
exec "$@"