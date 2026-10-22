#!/usr/bin/env bash
# Wait for the v1 GPT-5.6-sol campaign, validate the four new trap tasks with the reference
# solution end to end, then hand over to the six-campaign runner.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
# Operator configuration: DOCKER_HOST and BUILDX_BUILDER default to a rootless podman
# socket and a builder named "proxied"; the runner it hands over to needs DMAIC_PILOT_PROVIDER.
LOGDIR=output/research/portability_pilot
while pgrep -f "harbor run -c campaign-pilot-gpt56sol.local.yaml" >/dev/null; do sleep 60; done
echo "== $(date -u +%FT%TZ) v1 sol finished; running e2e on the trap tasks" | tee -a "$LOGDIR/campaigns.log"
export DOCKER_HOST="${DOCKER_HOST:-unix://$(podman machine inspect --format \
    '{{.ConnectionInfo.PodmanSocket.Path}}' 2>/dev/null)}"
export BUILDX_BUILDER="${BUILDX_BUILDER:-proxied}" DOCKER_BUILDKIT=0
mkdir -p "$LOGDIR/e2e-v2"
for t in dmaic-adb_c40-t3-s6-clean dmaic-adb_c40-t3-s7-clean dmaic-adb_c41-t3-s6-clean dmaic-adb_c41-t3-s7-clean dmaic-adb_c40-t3-s0-clean dmaic-adb_c41-t3-s0-clean; do
    bash harbor/scripts/e2e.sh "harbor/datasets/portability-pilot-v2/$t" > "$LOGDIR/e2e-v2/$t.log" 2>&1
    echo "$t exit=$? reward=$(grep -m1 '"reward"' "$LOGDIR/e2e-v2/$t.log" | tr -d ' ,') pq=$(grep -m1 '"pq"' "$LOGDIR/e2e-v2/$t.log" | tr -d ' ,') nf=$(grep -m1 '"nf"' "$LOGDIR/e2e-v2/$t.log" | tr -d ' ,') leak=$(grep -m1 'truth values reachable' "$LOGDIR/e2e-v2/$t.log" | tr -d ' ')" >> "$LOGDIR/e2e-v2/summary.txt"
done
echo "== $(date -u +%FT%TZ) e2e done; launching the v2 runner" | tee -a "$LOGDIR/campaigns.log"
exec scripts/run-pilot-v2-campaigns.sh
