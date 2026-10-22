#!/usr/bin/env bash
# Re-run the one sol thresholds-only trial lost to a gateway 524, after the luna control ends.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
# Operator configuration: DMAIC_PILOT_PROVIDER is the id, in providers.json, of the
# provider that serves the pilot contestants; DMAIC_ENV_FILE is the credential file
# (default ~/.config/dmaic/campaign.env); DOCKER_HOST and BUILDX_BUILDER default to a
# rootless podman socket and a builder named "proxied".
: "${DMAIC_PILOT_PROVIDER:?set DMAIC_PILOT_PROVIDER to the provider id in providers.json}"
LOGDIR=output/research/portability_pilot
until grep -q "ALL V2 CAMPAIGNS DONE" "$LOGDIR/campaigns.log"; do sleep 60; done
export DOCKER_HOST="${DOCKER_HOST:-unix://$(podman machine inspect --format \
    '{{.ConnectionInfo.PodmanSocket.Path}}' 2>/dev/null)}"
export BUILDX_BUILDER="${BUILDX_BUILDER:-proxied}" DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0
set +u; source "${DMAIC_ENV_FILE:-$HOME/.config/dmaic/campaign.env}" >/dev/null 2>&1; source scripts/agent-env.sh "$DMAIC_PILOT_PROVIDER" >/dev/null 2>&1; set -u
cfg=campaign-pilot-gpt56sol-v2-bare-fill.local.yaml
echo "== $(date -u +%FT%TZ) launching $cfg" | tee -a "$LOGDIR/campaigns.log"
harbor run -c "$cfg" > "$LOGDIR/campaign-gpt56sol-v2-bare-fill.log" 2>&1
echo "== $(date -u +%FT%TZ) $cfg exited rc=$? ; ALL FILLS DONE" | tee -a "$LOGDIR/campaigns.log"
