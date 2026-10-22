#!/usr/bin/env bash
# Second-domain portability pilot: the three OpenAI-family contestants, one after another, on
# the 12-task life-sciences dataset. Sequential on purpose: the podman VM has 10 CPUs and each
# trial is a 4-CPU agent container plus a verifier, so two campaigns at once would starve both.
#
# Same environment as scripts/run-campaign.sh, minus its `docker images` base-image probe: with
# several hundred per-task verifier images in the store that listing no longer returns inside
# the API timeout (measured 2026-09-23: >2 min, while `podman ps` answers at once). The base
# images were verified present by the e2e runs that precede every launch of this script.
#     scripts/run-pilot-campaigns.sh
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
# Operator configuration: DMAIC_PILOT_PROVIDER is the id, in providers.json, of the
# provider that serves the pilot contestants; DMAIC_ENV_FILE is the credential file
# (default ~/.config/dmaic/campaign.env); DOCKER_HOST and BUILDX_BUILDER default to a
# rootless podman socket and a builder named "proxied".
: "${DMAIC_PILOT_PROVIDER:?set DMAIC_PILOT_PROVIDER to the provider id in providers.json}"
LOGDIR=output/research/portability_pilot
mkdir -p "$LOGDIR"
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
    # The framework refuses to start ("Docker daemon is not running") when the podman API does
    # not answer inside its own timeout, which happens while another campaign saturates the VM.
    # Wait for a quick `docker info` before each launch rather than burning the attempt.
    local n=0
    until timeout 30 docker info --format '{{.ServerVersion}}' >/dev/null 2>&1; do
        n=$((n + 1))
        [ $((n % 4)) -eq 1 ] && echo "== $(date -u +%FT%TZ) podman API not answering; waiting" \
            | tee -a "$LOGDIR/campaigns.log"
        sleep 120
    done
}
for name in gpt6astra gpt56sol gpt56luna; do
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
echo "== $(date -u +%FT%TZ) ALL CAMPAIGNS DONE" | tee -a "$LOGDIR/campaigns.log"
