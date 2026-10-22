#!/usr/bin/env bash
# Run one campaign, refusing to start if the host cannot finish it.
#
#     scripts/run-campaign.sh <job-config.yaml> <provider-id>
#
# Every guard below is a failure that actually happened in this repository, each of which
# wasted hours and in one case destroyed 35 completed trials:
#
#  * DISK. `harbor run` builds one verifier image per task. A 97-task campaign exhausted a
#    16 GiB filesystem at trial 35 and died with ENOSPC mid-write. Harbor's own preflight
#    warns at 20 GiB; that warning was overridden by hand and it was right.
#  * BASE IMAGES. `docker image prune -af` to reclaim that space deleted the verifier base
#    AND `gogost/gost`, which is what harbor builds its no-network egress sidecar from.
#    Without them every task either pip-installs the scientific stack itself or fails with
#    "network_mode='no-network' is not supported" -- an error that reads like a benchmark
#    defect and is not one. This happened TWICE.
#  * BUILDX DRIVER. Harbor builds through `docker buildx`, so DOCKER_BUILDKIT=0 does not
#    reach it. The default buildx builder uses the docker-container driver, which keeps its
#    own image store, cannot see the local one, and therefore resolves even a present base
#    image over the registry -- dying on any momentary EOF. BUILDX_BUILDER names a
#    docker-container builder configured to reach the registry (operator configuration;
#    default `proxied`). DOCKER_HOST defaults to the rootless podman socket and
#    DMAIC_ENV_FILE to ~/.config/dmaic/campaign.env; override any of them in the environment.
set -euo pipefail

CONFIG="${1:?usage: run-campaign.sh <job-config.yaml> <provider-id>}"
PROVIDER="${2:?usage: run-campaign.sh <job-config.yaml> <provider-id>}"
cd "$(dirname "${BASH_SOURCE[0]}")/.."

export DOCKER_HOST="${DOCKER_HOST:-unix://$(podman machine inspect --format \
    '{{.ConnectionInfo.PodmanSocket.Path}}' 2>/dev/null)}"
export BUILDX_BUILDER="${BUILDX_BUILDER:-proxied}"
export DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0

fail() { echo "REFUSING TO START: $*" >&2; exit 1; }

free_gib=$(df -g . | awk 'NR==2 {print $4}')
[ "${free_gib:-0}" -ge 25 ] || fail "only ${free_gib} GiB free; a 97-task campaign needs ~25"

for img in "ghcr.io/dmaic-bench/verifier:0.1.0-base" "gogost/gost" "python:3.12.7-slim-bookworm"; do
    docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "${img%%:*}" \
        || fail "base image missing: $img  (verifier base: scripts/build-verifier-base.sh;
        gost: podman pull --tls-verify=false docker.io/gogost/gost:3.2.7-nightly.20260602)"
done

docker buildx inspect "$BUILDX_BUILDER" --bootstrap >/dev/null 2>&1 \
    || fail "buildx builder '$BUILDX_BUILDER' will not start"

set +u
source "${DMAIC_ENV_FILE:-$HOME/.config/dmaic/campaign.env}" >/dev/null 2>&1
source scripts/agent-env.sh "$PROVIDER" >/dev/null 2>&1
set -u
[ -n "${OPENAI_API_KEY:-}${ANTHROPIC_API_KEY:-}" ] || fail "no credential for provider $PROVIDER"

echo "preflight OK: ${free_gib} GiB free, base images present, builder $BUILDX_BUILDER"
exec harbor run -c "$CONFIG"
