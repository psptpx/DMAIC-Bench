# No `# syntax=` directive on purpose. This Dockerfile uses no BuildKit frontend feature
# (no `--mount`, no `--chmod`, no heredocs), so pinning a frontend buys nothing and costs
# an extra image pull at build time -- which is a real failure mode on a restricted
# network: the build dies resolving `docker/dockerfile:1` before it touches our layers.
#
# DMAIC-Bench SEPARATE verifier image  (dmaic_harbor.spec.VERIFIER_IMAGE)
# =============================================================================
# This image holds TRUTH + THE ORACLE and nothing else. The agent's image holds the DATA
# and the PUBLIC gate thresholds and nothing else. That split is the whole reason the task
# runs with `environment_mode = "separate"`.
#
# HOW HARBOR BUILDS THIS
# ----------------------
# For a separate verifier Harbor uses the task's `tests/` directory as the Docker build
# context (`harbor/trial/trial.py::_verifier_env_build_context` -> `task.paths.tests_dir`)
# and builds `<context>/Dockerfile` with NO build args
# (`harbor/environments/docker/docker-compose-build.yaml`). Every ARG default below must
# therefore already be the value we want in production.
#
# REQUIRED BUILD CONTEXT — the builder MUST create every one of these paths
# -------------------------------------------------------------------------
#     Dockerfile                     <- this file
#     test.sh                        <- host-side copy, for Harbor's test-path discovery
#     stage/verify.py.txt            <- dmaic_harbor/verify.py, VERBATIM CONTENT
#     stage/spec.py.txt              <- dmaic_harbor/spec.py,   VERBATIM CONTENT
#     stage/test.sh                  <- baked to /tests/test.sh
#     stage/truth.json               <- THE PER-TASK TRUTH PACKAGE
#     stage/package/                 <- MUST EXIST. Holds ONE of:
#                                        *.whl                      (preferred; on a DLP
#                                                                    workstation it is the
#                                                                    ONLY safe mode, since a
#                                                                    staged source tree is
#                                                                    full of *.py files)
#                                        pyproject.toml + dmaic_bench/
#                                        dmaic_bench/           (source tree only)
#                                        .keep                      (when BASE_IMAGE
#                                                                    already has the package)
#
# Every COPY source below is a named path that always exists, so nothing is copied that we
# do not deliberately ship. This is on purpose: a `COPY .` writes the whole filtered build
# context into an image layer PERMANENTLY, and a later `rm -rf` in another RUN does not
# remove it from layer history — anyone who can pull the image recovers it with
# `docker save`. Staging into `stage/` is what lets every source path exist unconditionally
# without resorting to a whole-context copy (a glob matching nothing is a hard build error).
#
# TWO REASONS THE PYTHON FILES ARE NAMED `*.py.txt`
# -------------------------------------------------
#   1. Endpoint DLP (Esafenet, on the authoring workstation) transparently encrypts every
#      file whose name ends in `.py`. Python, git and cat see plaintext; a container
#      runtime reading the build context over virtiofs sees CIPHERTEXT, and the build dies
#      with `SyntaxError: source code string cannot contain null bytes`. A non-`.py` name
#      sidesteps the policy; the RUN below renames the files into place inside the image.
#   2. It makes the staging directory unimportable by accident.
# The `py_compile` check at the end turns any recurrence into an obvious BUILD failure
# rather than a mysterious runtime one.
#
# TWO BUILD MODES, ONE FILE
# -------------------------
#   1. Standalone (the default): BASE_IMAGE=python:3.12.7-slim-bookworm. Everything is
#      installed here. The pinned-wheel layer is context-independent, so Docker's layer
#      cache shares it across every task image; only the small staged layer (which carries
#      truth.json) is per-task. "Hundreds of images" is hundreds of image *names* over one
#      shared stack of layers plus a few kB each.
#   2. Layered: the builder rewrites the BASE_IMAGE default to an already-built verifier
#      image. The pip layer then resolves as a no-op and `stage/package/` holds only .keep.
#
# NOTE ON `harbor check`: the rubric criteria `tests_or_solution_in_image` and
# `test_deps_in_image` are deliberately not satisfied here — see the "Deliberate deviations"
# section of verify.py's module docstring. Harbor forces the first (skip_tests_upload) and
# `network_mode = "no-network"` forces the second.

ARG BASE_IMAGE=python:3.12.7-slim-bookworm
FROM ${BASE_IMAGE}

LABEL org.opencontainers.image.title="dmaic-bench-verifier" \
      org.opencontainers.image.description="DMAIC-Bench separate verifier: truth + oracle" \
      org.opencontainers.image.licenses="Apache-2.0"

# NO_PROXY=* : container runtimes inject http_proxy/https_proxy pointing at a host-side
# forwarder (podman sets http://host.containers.internal:10808). urllib honours those, so an
# otherwise-harmless local call fails with "Temporary failure in name resolution" and reads
# as a dead service. The verifier is no-network by design and never makes an HTTP call, but
# a stdlib default must not be able to turn into a hang. verify.py additionally strips these
# from os.environ at start-up, and test.sh unsets them before exec'ing python.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/opt/dmaic/pkg:/opt/dmaic \
    NO_PROXY=* \
    no_proxy=*

# --------------------------------------------------------------------------------------
# Layer 1 — pinned Python dependencies.
#
# EXACT pins, no ranges, and IDENTICAL to the agent image's pins -- both derive from the one
# authoritative set, `ANALYSIS_PINS` in dmaic_harbor/spec.py. A Dockerfile cannot import
# it, so `test_dependency_pins_are_single_sourced` holds this block to it and fails the
# moment it drifts. Change spec.py, then here. The bench derives ground
# truth with these libraries; a truth value produced under one SciPy and checked under
# another is a reproducibility hole (e.g. `scipy.stats.anderson` changes behaviour in SciPy
# 1.19, and both dmaic_bench/truth/verifiers.py and cases/adb_c02/generator.py call
# it). Transitive dependencies are pinned too so the closure is fully reproducible. This
# layer depends on nothing from the build context, so it is shared by every task image.
#
# Scoring itself needs only pyyaml (taxonomy.yaml) + jsonschema (trace schema validation);
# numpy/scipy/statsmodels/pandas are here so the verifier can re-derive or re-check an
# oracle value in place, under `no-network`, without a second image.
# --------------------------------------------------------------------------------------
RUN pip install --no-cache-dir --retries 5 --timeout 180 \
      numpy==2.1.3 \
      scipy==1.14.1 \
      statsmodels==0.14.4 \
      pandas==2.2.3 \
      patsy==1.0.1 \
      python-dateutil==2.9.0.post0 \
      pytz==2024.2 \
      tzdata==2024.2 \
      six==1.16.0 \
      packaging==24.1 \
      PyYAML==6.0.2 \
      jsonschema==4.23.0 \
      jsonschema-specifications==2024.10.1 \
      referencing==0.35.1 \
      rpds-py==0.20.1 \
      attrs==24.2.0

# --------------------------------------------------------------------------------------
# Layer 2 — the staged material: verifier code, the bench package, and the truth package.
# Named sources only; nothing else from the context enters the image.
# --------------------------------------------------------------------------------------
COPY stage/verify.py.txt /opt/dmaic/stage/verify.py.txt
COPY stage/spec.py.txt   /opt/dmaic/stage/spec.py.txt
COPY stage/test.sh       /opt/dmaic/stage/test.sh
COPY stage/truth.json    /opt/dmaic/stage/truth.json
COPY stage/package       /opt/dmaic/stage/package

# The dmaic_bench package: wheel > source tree with pyproject > plain source tree.
# Installed with --no-deps: the pinned closure above is authoritative, and resolving the
# package's own (unpinned, `scipy>=1.10`) ranges would defeat the pinning.
#
# THE TRUTH PACKAGE is moved to /opt/dmaic/verifier/truth.json. That is the only copy of
# the oracle anywhere in the trial: never in the agent image, never in an artifact, never on
# a network the agent can reach. Mode 0444, not 0400 — the container boundary is the
# isolation, and `[verifier].user` may not be root.
#
# /tests/test.sh MUST live in the image: Harbor passes skip_tests_upload=True in separate
# mode and will not copy it in.
RUN set -eu; \
    stage=/opt/dmaic/stage; \
    mkdir -p /tests /opt/dmaic/pkg /opt/dmaic/verifier; \
    if ls "$stage"/package/*.whl >/dev/null 2>&1; then \
        pip install --no-cache-dir --retries 5 --timeout 180 --no-deps "$stage"/package/*.whl; \
    elif [ -f "$stage/package/pyproject.toml" ] && [ -d "$stage/package/dmaic_bench" ]; then \
        pip install --no-cache-dir --retries 5 --timeout 180 --no-deps "$stage/package"; \
    elif [ -d "$stage/package/dmaic_bench" ]; then \
        cp -a "$stage/package/dmaic_bench" /opt/dmaic/pkg/; \
    fi; \
    mv "$stage/verify.py.txt" /opt/dmaic/verify.py; \
    mv "$stage/spec.py.txt"   /opt/dmaic/spec.py; \
    mv "$stage/test.sh"       /tests/test.sh; \
    chmod 0755 /tests/test.sh; \
    mv "$stage/truth.json"    /opt/dmaic/verifier/truth.json; \
    chmod 0444 /opt/dmaic/verifier/truth.json; \
    rm -rf "$stage"

# Byte-compile the verifier so a syntax error — or DLP ciphertext in the context — fails the
# BUILD, not the trial.
RUN python -m py_compile /opt/dmaic/verify.py /opt/dmaic/spec.py

WORKDIR /
# Harbor overrides the command with `sleep infinity` and execs /tests/test.sh itself; this
# default only makes the image runnable by hand.
CMD ["/tests/test.sh"]
