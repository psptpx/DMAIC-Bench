#!/usr/bin/env bash
# Extended second-domain pilot: six campaigns in sequence -- the three contestants on the
# protocol brief (k = 3), then on the thresholds-only brief (k = 1). Waits for the v1
# GPT-5.6-sol campaign to finish first so two campaigns never share the VM.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
# Operator configuration: DMAIC_PILOT_PROVIDER is the id, in providers.json, of the
# provider that serves the pilot contestants; DMAIC_ENV_FILE is the credential file
# (default ~/.config/dmaic/campaign.env); DOCKER_HOST and BUILDX_BUILDER default to a
# rootless podman socket and a builder named "proxied".
: "${DMAIC_PILOT_PROVIDER:?set DMAIC_PILOT_PROVIDER to the provider id in providers.json}"
LOGDIR=output/research/portability_pilot
mkdir -p "$LOGDIR"
while pgrep -f "harbor run -c campaign-pilot-gpt56sol.local.yaml" >/dev/null; do sleep 60; done
export DOCKER_HOST="${DOCKER_HOST:-unix://$(podman machine inspect --format \
    '{{.ConnectionInfo.PodmanSocket.Path}}' 2>/dev/null)}"
export BUILDX_BUILDER="${BUILDX_BUILDER:-proxied}"
export DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0
set +u
source "${DMAIC_ENV_FILE:-$HOME/.config/dmaic/campaign.env}" >/dev/null 2>&1
source scripts/agent-env.sh "$DMAIC_PILOT_PROVIDER" >/dev/null 2>&1
set -u
[ -n "${OPENAI_API_KEY:-}" ] || { echo "no credential for provider $DMAIC_PILOT_PROVIDER" >&2; exit 1; }
wait_for_api() {
    until timeout 30 docker info --format '{{.ServerVersion}}' >/dev/null 2>&1; do
        echo "== $(date -u +%FT%TZ) podman API not answering; waiting" | tee -a "$LOGDIR/campaigns.log"
        sleep 120
    done
}
for name in gpt6astra-v2 gpt56sol-v2 gpt56luna-v2 gpt6astra-v2-bare gpt56sol-v2-bare gpt56luna-v2-bare; do
    cfg="campaign-pilot-$name.local.yaml"
    wait_for_api
    echo "== $(date -u +%FT%TZ) launching $cfg" | tee -a "$LOGDIR/campaigns.log"
    harbor run -c "$cfg" > "$LOGDIR/campaign-$name.log" 2>&1
    rc=$?
    echo "== $(date -u +%FT%TZ) $cfg exited rc=$rc" | tee -a "$LOGDIR/campaigns.log"
    if [ "$rc" -ne 0 ]; then
        wait_for_api
        echo "== $(date -u +%FT%TZ) resuming $cfg" | tee -a "$LOGDIR/campaigns.log"
        harbor run -c "$cfg" >> "$LOGDIR/campaign-$name.log" 2>&1
        echo "== $(date -u +%FT%TZ) $cfg resume exited rc=$?" | tee -a "$LOGDIR/campaigns.log"
    fi
done
echo "== $(date -u +%FT%TZ) ALL V2 CAMPAIGNS DONE" | tee -a "$LOGDIR/campaigns.log"
