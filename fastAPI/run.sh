#!/usr/bin/env bash
# run.sh — start the GPS Services FastAPI server.
#
# Usage:
#   ./run.sh                  # serve on 0.0.0.0:8000
#   PORT=8080 ./run.sh        # custom port
#   HOST=127.0.0.1 ./run.sh   # custom host
#   ./run.sh --reload         # dev mode with auto-reload (extra args are passed to uvicorn)
#
# Then open:
#   http://localhost:8000/map           (interactive GNSS map interface)
#   http://localhost:8000/gpsservice/test (API status)

set -euo pipefail

cd "$(dirname "$0")"

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

if command -v uv >/dev/null 2>&1; then
    uv sync --frozen 2>/dev/null || uv sync
    exec uv run uvicorn app:app --host "$HOST" --port "$PORT" "$@"
elif python3 -c "import uvicorn" >/dev/null 2>&1; then
    exec python3 -m uvicorn app:app --host "$HOST" --port "$PORT" "$@"
else
    echo "error: neither 'uv' nor 'uvicorn' is available." >&2
    echo "Install uv (https://docs.astral.sh/uv/) or run: pip install -r requirements.txt" >&2
    exit 1
fi
