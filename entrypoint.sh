#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

log() { printf '%s %s\n' "[entrypoint]" "$*"; }

log "Starting entrypoint…"

# ── БЕЗ ВНЕШНЕЙ БД ─────────────────────────────────────────────────────────────
log "No external DB configured. Skipping DB readiness check."

# ── Миграции ───────────────────────────────────────────────────────────────────
log "Applying migrations…"
python manage.py migrate --noinput

# ── Статика ────────────────────────────────────────────────────────────────────
log "Collecting static files…"
mkdir -p /app/collected_static
python manage.py collectstatic --noinput

# ── Локали (не критично) ───────────────────────────────────────────────────────
log "Compiling translations (best effort)…"
python - <<'PY' || true
import subprocess
try:
    subprocess.check_call(["python", "manage.py", "compilemessages"])
except Exception as e:
    print("[entrypoint] compilemessages skipped/failed:", repr(e))
PY

log "Startup done. Launching app: $*"
exec "$@"
