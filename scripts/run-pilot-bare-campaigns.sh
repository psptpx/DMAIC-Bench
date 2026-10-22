#!/usr/bin/env bash
# The thresholds-only control of the portability pilot: same twelve tasks, brief stating the
# numbers and not the stop rules, k = 1, run after the main pilot campaigns have all finished.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
# Operator configuration: DMAIC_PILOT_PROVIDER is the id, in providers.json, of the
# provider that serves the pilot contestants; DMAIC_ENV_FILE is the credential file
# (default ~/.config/dmaic/campaign.env); DOCKER_HOST and BUILDX_BUILDER default to a
# rootless podman socket and a builder named "proxied".
: "${DMAIC_PILOT_PROVIDER:?set DMAIC_PILOT_PROVIDER to the provider id in providers.json}"
LOGDIR=output/research/portability_pilot
until grep -q "ALL CAMPAIGNS DONE" "$LOGDIR/campaigns.log" 2>/dev/null; do sleep 120; done
export DOCKER_HOST="${DOCKER_HOST:-unix://$(podman machine inspect --format \
    '{{.ConnectionInfo.PodmanSocket.Path}}' 2>/dev/null)}"
export BUILDX_BUILDER="${BUILDX_BUILDER:-proxied}"
export DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0
set +u
source "${DMAIC_ENV_FILE:-$HOME/.config/dmaic/campaign.env}" >/dev/null 2>&1
source scripts/agent-env.sh "$DMAIC_PILOT_PROVIDER" >/dev/null 2>&1
set -u
wait_for_api() {
    until timeout 30 docker info --format '{{.ServerVersion}}' >/dev/null 2>&1; do sleep 120; done
}
for name in gpt6astra gpt56sol gpt56luna; do
    cfg="campaign-pilot-$name-bare.local.yaml"
    wait_for_api
    echo "== $(date -u +%FT%TZ) launching $cfg" | tee -a "$LOGDIR/campaigns.log"
    harbor run -c "$cfg" > "$LOGDIR/campaign-$name-bare.log" 2>&1
    rc=$?
    echo "== $(date -u +%FT%TZ) $cfg exited rc=$rc" | tee -a "$LOGDIR/campaigns.log"
    if [ "$rc" -ne 0 ]; then
        wait_for_api
        echo "== $(date -u +%FT%TZ) resuming $cfg" | tee -a "$LOGDIR/campaigns.log"
        harbor run -c "$cfg" >> "$LOGDIR/campaign-$name-bare.log" 2>&1
        echo "== $(date -u +%FT%TZ) $cfg resume exited rc=$?" | tee -a "$LOGDIR/campaigns.log"
    fi
done
echo "== $(date -u +%FT%TZ) ALL BARE CAMPAIGNS DONE" | tee -a "$LOGDIR/campaigns.log"
