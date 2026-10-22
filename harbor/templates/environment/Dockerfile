# DMAIC-Bench — the AGENT environment image.
#
# Contract (see dmaic_harbor/spec.py):
#   * This image holds DATA + PUBLIC GATE THRESHOLDS and nothing else. Truth and the oracle
#     live only in the verifier image. Do NOT add the bench package, the method taxonomy,
#     the case definitions, or anything naming an expected method — the steward fails closed
#     on such payloads, but the image must not carry them in the first place.
#   * Nothing under the operator-only adapter directory may enter this image: the excluded
#     contestant is not redistributable and the images must not name it. See
#     dmaic_harbor/policy.py (host-side; it does not ship).
#   * The agent runs with network_mode = "no-network"; the steward binds loopback only and
#     reaches nothing.
#
# REQUIRED BUILD CONTEXT LAYOUT (produced per task by build.py):
#   Dockerfile
#   entrypoint.sh
#   dmaic_harbor/spec.py
#   dmaic_harbor/steward_service.py
#   dmaic_harbor/steward_cli.py
#   task/blocks.json          -> /opt/dmaic/task/blocks.json   (spec.AGENT_BLOCKS_FILE)
#   task/steward.json         -> /opt/dmaic/task/steward.json  (spec.AGENT_STEWARD_CFG)
#   task/TASK.md   (optional) -> /workspace/TASK.md                (spec.TASK_MD)
FROM python:3.12.7-slim-bookworm

# Analysis tooling the agent needs to be able to do the work at all. Pinned; wheels only.
#
# THESE VERSIONS ARE NOT AUTHORITATIVE HERE. The one authoritative set is
# `ANALYSIS_PINS` in dmaic_harbor/spec.py; a Dockerfile cannot import it, so
# `test_dependency_pins_are_single_sourced` asserts this block still matches it and
# fails the build's test suite the moment it drifts. Change spec.py, then here.
# The verifier image installs the SAME set: truth derived under one SciPy and checked
# under another is exactly the hole `environment_mode = "separate"` opens.
RUN pip install --no-cache-dir --only-binary=:all: \
        numpy==2.1.3 \
        scipy==1.14.1 \
        pandas==2.2.3 \
        statsmodels==0.14.4 \
 && find /usr/local/lib/python3.12 -name '__pycache__' -type d -prune -exec rm -rf {} + \
 && find /usr/local/lib/python3.12 -name 'tests' -type d -prune -exec rm -rf {} +

# Terminal plumbing for harness agents that drive the container through a recorded tmux
# session (Harbor's terminus-2 is the reference case). The agent container runs
# `network_mode = "no-network"`, so an agent that tries to install these at setup time fails
# with "Failed to start tmux session" and the trial is lost before the model is ever called --
# measured, not anticipated. Build time is the only moment a network exists, so they go here.
#
# These are TOOLING, not payload: they carry no task data, no truth and no method name, and
# the hygiene tests still assert the image holds only data + public gate thresholds.
RUN apt-get update \
 && apt-get install -y --no-install-recommends tmux ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir asciinema \
 && tmux -V && asciinema --version

# Toolchains other than Python, so the score measures statistics rather than Python fluency.
#
# The task contract is already language-neutral -- `trace.json` is `method_id` + `outputs`, and
# the instruction names no language -- but the IMAGE was Python-only, so a model that would
# rather work in R or on the JVM simply could not. That is the same class of confound as an
# all-Chinese corpus measuring reading ability, and it is not hypothetical: R's
# `prop.test()` applies Yates' continuity correction by default where statsmodels does not, so
# the two give different (both correct) answers, and the corpus now DECLARES which convention a
# truth used rather than silently rewarding one toolchain.
#
# Everything is installed at BUILD time because the agent container runs `no-network` -- stricter
# than the harness this dataset targets, which allows internet and lists that under its own
# limitations. The price is that a gap in this list is a benchmark defect rather than an agent
# failure, so the capability manifest below ships with the dataset and is asserted by tests.
#
# Octave is deliberately absent: Debian bookworm has no `octave-cli`, so it drags the full Qt/GL
# stack for the smallest constituency of the three. Julia is absent for the same reason -- not in
# Debian at all, and a tarball plus a precompiled depot costs more than R and the JVM together.
# Both are revisitable; neither is worth ~600 MB today.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        r-base-core r-cran-e1071 r-cran-nortest r-cran-jsonlite r-cran-boot r-cran-mass \
        openjdk-17-jre-headless libcommons-math3-java \
 && rm -rf /var/lib/apt/lists/* \
 && Rscript -e 'stopifnot(requireNamespace("e1071"), requireNamespace("nortest"), requireNamespace("jsonlite"))' \
 && java -version

#: What an agent may assume is present. Published so a missing tool is reported rather than
#: silently scored as incompetence.
COPY toolchains.json /opt/dmaic/toolchains.json

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/dmaic/lib \
    DMAIC_BLOCKS_FILE=/opt/dmaic/task/blocks.json \
    DMAIC_STEWARD_CFG=/opt/dmaic/task/steward.json \
    DMAIC_STEWARD_AUDIT=/workspace/.steward/audit.jsonl \
    DMAIC_STEWARD_DATA_DIR=/workspace/data \
    DMAIC_STEWARD_HOST=127.0.0.1 \
    DMAIC_STEWARD_PORT=8731 \
    DMAIC_STEWARD_BASE=http://127.0.0.1:8731 \
    NO_PROXY=* \
    no_proxy=*

# The steward service + CLI (spec.py is the shared contract they build against).
#
# Staged with a `.txt` suffix and renamed below, exactly as the verifier image does. Some
# endpoint-DLP products wrap `*.py` at rest keyed on the WRITING PROCESS, not the directory:
# the host toolchain reads plaintext through the driver while the container runtime reads the
# wrapper off disk and every module arrives full of NUL bytes. Measured here: a module the
# host reads as 43 527 clean bytes is 47 623 bytes with 2 671 NULs inside the container.
# A non-`.py` name is not wrapped, so the bytes survive; the rename happens after the copy.
COPY dmaic_harbor/spec.py.txt            /opt/dmaic/stage/spec.py.txt
COPY dmaic_harbor/steward_service.py.txt /opt/dmaic/stage/steward_service.py.txt
COPY dmaic_harbor/steward_cli.py.txt     /opt/dmaic/stage/steward_cli.py.txt
RUN set -eu; \
    pkg=/opt/dmaic/lib/dmaic_harbor; \
    mkdir -p "$pkg"; \
    for m in spec steward_service steward_cli; do \
        mv "/opt/dmaic/stage/$m.py.txt" "$pkg/$m.py"; \
    done; \
    rmdir /opt/dmaic/stage; \
    # A re-wrapped module must fail the BUILD, loudly, not the run hours later.
    python3 -m py_compile "$pkg/spec.py" "$pkg/steward_service.py" "$pkg/steward_cli.py"

# `steward` on PATH at spec.STEWARD_CLI — the agent's only channel to project data.
RUN printf '#!/bin/sh\nexec python3 -m dmaic_harbor.steward_cli "$@"\n' \
        > /usr/local/bin/steward \
 && chmod 0755 /usr/local/bin/steward

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod 0755 /usr/local/bin/entrypoint.sh

# Per-task payload: data blocks + public gate policy. NO truths, NO methods.
COPY task/ /opt/dmaic/task/
RUN mkdir -p /workspace/.steward /workspace/data \
 && if [ -f /opt/dmaic/task/TASK.md ]; then \
        cp /opt/dmaic/task/TASK.md /workspace/TASK.md; \
    fi \
 && python3 -m dmaic_harbor.steward_service --check

WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"]
