#!/bin/sh
# Start the data steward as a background service, block until it is ready, then hand over.
#
# The steward is the agent's ONLY channel to project data (spec.STEWARD_BASE, loopback
# only — the container has no network). Starting it here, in the container's main process,
# means it is already up for every `exec` Harbor makes into the container.
set -eu

: "${DMAIC_STEWARD_HOST:=127.0.0.1}"
: "${DMAIC_STEWARD_PORT:=8731}"
: "${DMAIC_STEWARD_AUDIT:=/workspace/.steward/audit.jsonl}"
: "${DMAIC_STEWARD_DATA_DIR:=/workspace/data}"
: "${STEWARD_READY_TIMEOUT:=30}"

LOG=/workspace/.steward/service.log
mkdir -p "$(dirname "$DMAIC_STEWARD_AUDIT")" "$DMAIC_STEWARD_DATA_DIR"

# Fail fast and loudly if the baked payload violates the strict agent-side schema.
python3 -m dmaic_harbor.steward_service --check

python3 -m dmaic_harbor.steward_service >"$LOG" 2>&1 &
STEWARD_PID=$!

# Readiness check (no curl in the slim image — urllib is always there).
i=0
while [ "$i" -lt "$((STEWARD_READY_TIMEOUT * 10))" ]; do
    if python3 - <<'PY' >/dev/null 2>&1
import json, os, sys, urllib.request
# proxies disabled: the runtime may inject HTTP_PROXY, and the steward is loopback-only
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
url = "http://%s:%s/healthz" % (os.environ["DMAIC_STEWARD_HOST"],
                                os.environ["DMAIC_STEWARD_PORT"])
with opener.open(url, timeout=2) as r:
    sys.exit(0 if json.loads(r.read()).get("ok") else 1)
PY
    then
        echo "steward: ready on http://${DMAIC_STEWARD_HOST}:${DMAIC_STEWARD_PORT}"
        break
    fi
    if ! kill -0 "$STEWARD_PID" 2>/dev/null; then
        echo "steward: service died during startup" >&2
        cat "$LOG" >&2 || true
        exit 1
    fi
    i=$((i + 1))
    sleep 0.1
done

if [ "$i" -ge "$((STEWARD_READY_TIMEOUT * 10))" ]; then
    echo "steward: not ready after ${STEWARD_READY_TIMEOUT}s" >&2
    cat "$LOG" >&2 || true
    exit 1
fi

exec "$@"
