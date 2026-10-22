#!/usr/bin/env bash
# Build the verifier BASE image once, so the per-task builds never touch a package index.
#
# WHY THIS EXISTS
# ---------------
# Two consecutive G3 runs lost all 312 trials to the network, and neither failure was a
# benchmark defect:
#
#   1. every buildx builder on this host uses the `docker-container` driver, which has its
#      own image store and CANNOT see the local one. So a build resolves even an
#      already-present base image over the registry, and a momentary `registry-1.docker.io`
#      EOF kills all 156 image builds at once.
#   2. a host that routes egress through a local proxy does not pass it to a build container,
#      so `pip install` inside the image build gets ECONNREFUSED while the host reaches PyPI
#      fine. Pass that proxy as PIP_PROXY (argument or environment variable); it is optional.
#
# The repository already had the right answer and it was not being used: the verifier
# Dockerfile takes `ARG BASE_IMAGE`, and `dmaic-harbor-build` rewrites its default to
# `DEFAULT_VERIFIER_BASE` unless `--bench-wheel` is passed. Passing `--bench-wheel` forces
# the standalone path, where every one of the 156 verifier images pip-installs the whole
# scientific stack itself. Build the base once instead; pip short-circuits an exact pin that
# is already satisfied, so the per-task builds run offline.
#
# USAGE
#   scripts/build-verifier-base.sh [PIP_PROXY]
#   # then, WITHOUT --bench-wheel:
#   python -m dmaic_harbor.build --v2 --with-faults --out harbor/datasets/dmaic-bench
#   # and run with the legacy builder so the local base image is visible:
#   DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 harbor run -c <job>.yaml
set -euo pipefail

PIP_PROXY="${1:-${PIP_PROXY:-}}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# The tag MUST track spec.PACKAGE_VERSION: `build.DEFAULT_VERIFIER_BASE` is derived from it,
# so a hardcoded version here silently drifts on a package bump and every per-task verifier
# build then tries to PULL a tag that was never built (observed on the 0.1.0 -> 0.2.0 bump:
# every trial of a freshly built dataset died in `docker compose build`).
TAG="$(python3 -c 'import sys; sys.path.insert(0, "'"$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"'/harbor/src"); from dmaic_harbor import spec; print(f"{spec.VERIFIER_IMAGE}:{spec.PACKAGE_VERSION}-base")')"
CTX="$(mktemp -d)"
trap 'rm -rf "$CTX"' EXIT

python3 -m build --wheel --outdir "$CTX" "$ROOT" >/dev/null
WHEEL="$(basename "$(ls "$CTX"/dmaic_bench-*.whl | head -1)")"

# The proxy is a build ARG and deliberately never an ENV, so it does not persist into the
# image -- a baked proxy would follow the verifier into a no-network trial.
{
  echo "FROM python:3.12.7-slim-bookworm"
  echo "ARG PIP_PROXY="
  sed -n '/^RUN pip install --no-cache-dir --retries 5 --timeout 180 .$/,/^      attrs==/p' \
      "$ROOT/harbor/templates/verifier/Dockerfile" \
    | sed '1s|.*|RUN pip install --no-cache-dir --retries 5 --timeout 180 ${PIP_PROXY:+--proxy $PIP_PROXY} \\|'
  echo "COPY $WHEEL /tmp/"
  echo "RUN pip install --no-cache-dir --no-deps /tmp/$WHEEL \\"
  echo " && rm -f /tmp/$WHEEL"
} > "$CTX/Dockerfile"

# podman build, NOT `docker build`: podman resolves the base image from the local store
# first, which is the whole point.
podman build ${PIP_PROXY:+--build-arg PIP_PROXY="$PIP_PROXY"} -t "$TAG" "$CTX"
echo "built $TAG"
