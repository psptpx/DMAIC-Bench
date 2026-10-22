#!/bin/sh
# =============================================================================
# DMAIC-Bench verifier entrypoint — baked into the verifier image at /tests/test.sh.
#
# Harbor execs this script directly inside the SEPARATE verifier container and then reads
# /logs/verifier/reward.json. If no reward file exists it raises RewardFileNotFoundError and
# the trial is UNSCORED, which is strictly worse than a zero — so the single hard guarantee
# of this script is: **a parseable reward file always exists when it exits, and it always
# exits 0.**
#
# It must not install anything: the verifier runs with network_mode = "no-network" and every
# dependency is pinned into the image (see Dockerfile). This is the documented deviation
# from the `test_deps_in_image` rubric criterion.
#
# Sections below, in order:
#   1. paths           where truth, artifacts and outputs live (mirrors spec.py)
#   1b. proxy           neutralise runtime-injected HTTP proxies
#   2. preflight       report what is present, without failing on anything missing
#   3. score           run verify.py (which itself never raises; it writes both outputs)
#   4. fallback        last resort if verify.py could not write a usable reward.json
#   5. verify output   prove the reward file is non-empty and valid JSON before exiting
# =============================================================================
set -u

# --- 1. paths ---------------------------------------------------------------------------
# Keep in sync with dmaic_harbor/spec.py: VERIFIER_TRUTH_FILE, ARTIFACTS_DIR,
# REWARD_JSON, SCORECARD_JSON.
TRUTH_FILE="${DMAIC_TRUTH_FILE:-/opt/dmaic/verifier/truth.json}"
ARTIFACTS_DIR="${DMAIC_ARTIFACTS_DIR:-/logs/artifacts}"
VERIFIER_DIR="${DMAIC_VERIFIER_DIR:-/logs/verifier}"
REWARD_JSON="${DMAIC_REWARD_JSON:-${VERIFIER_DIR}/reward.json}"
SCORECARD_JSON="${DMAIC_SCORECARD_JSON:-${VERIFIER_DIR}/scorecard.json}"
VERIFY_PY="${DMAIC_VERIFY_PY:-/opt/dmaic/verify.py}"
PYTHON_BIN="${DMAIC_PYTHON:-python3}"

mkdir -p "${VERIFIER_DIR}" 2>/dev/null || true

# --- 1b. proxy --------------------------------------------------------------------------
# Container runtimes inject http_proxy/https_proxy pointing at a host-side forwarder (podman
# sets http://host.containers.internal:10808). Python's urllib honours them, so even a
# loopback call fails with "Temporary failure in name resolution" and reads as a dead
# service. The verifier is no-network by design; clear them so no stdlib default can hang.
unset http_proxy https_proxy ftp_proxy all_proxy 2>/dev/null || true
unset HTTP_PROXY HTTPS_PROXY FTP_PROXY ALL_PROXY 2>/dev/null || true
NO_PROXY='*'; no_proxy='*'
export NO_PROXY no_proxy

# --- 2. preflight -----------------------------------------------------------------------
# Checks what the scoring inputs look like. Nothing here may abort the run: every one of
# these files is optional or agent-produced, and a missing one is a scoring outcome (a low
# reward), not a verifier failure.
echo "[test.sh] truth package : ${TRUTH_FILE} $( [ -f "${TRUTH_FILE}" ] && echo present || echo MISSING )"
# Harbor re-materialises each [[artifacts]] entry at its ORIGINAL `source` path, not under
# the conventional artifacts dir (harbor/trial/artifact_handler.py::upload_artifacts). So
# check both, in the same order verify.py resolves them -- a preflight that only looked at
# ARTIFACTS_DIR reported every artifact MISSING on a run that in fact had them all.
echo "[test.sh] artifacts dir : ${ARTIFACTS_DIR} (source paths checked first)"
for pair in "/workspace/trace.json:trace.json" \
            "/workspace/report.md:report.md" \
            "/workspace/.steward/audit.jsonl:steward-audit.jsonl"; do
    src="${pair%%:*}"; dest="${pair##*:}"
    if [ -f "${src}" ]; then
        echo "[test.sh]   ${dest}: present at source ${src}"
    elif [ -f "${ARTIFACTS_DIR}/${dest}" ]; then
        echo "[test.sh]   ${dest}: present at ${ARTIFACTS_DIR}/${dest}"
    else
        echo "[test.sh]   ${dest}: MISSING at both ${src} and ${ARTIFACTS_DIR}/${dest}"
    fi
done
echo "[test.sh] verifier      : ${VERIFY_PY} $( [ -f "${VERIFY_PY}" ] && echo present || echo MISSING )"

# --- 3. score ---------------------------------------------------------------------------
# verify.py owns all scoring and writes both reward.json and scorecard.json. It catches
# everything internally, so a non-zero exit here means it could not even write its outputs.
RC=1
if [ -f "${VERIFY_PY}" ]; then
    "${PYTHON_BIN}" "${VERIFY_PY}" \
        "${TRUTH_FILE}" "${ARTIFACTS_DIR}" "${REWARD_JSON}" "${SCORECARD_JSON}"
    RC=$?
    echo "[test.sh] verify.py exit=${RC}"
else
    echo "[test.sh] FATAL: ${VERIFY_PY} is not in the image" >&2
fi

# --- 4. fallback ------------------------------------------------------------------------
# Reached only when verify.py is absent, was killed (OOM/timeout), or failed to write. Emit
# the full flat reward contract at zero plus an error marker in the scorecard, so the trial
# is scored 0 and audibly flagged rather than lost.
reward_is_usable() {
    [ -s "${REWARD_JSON}" ] || return 1
    "${PYTHON_BIN}" -c 'import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if isinstance(d,dict) and d else 1)' \
        "${REWARD_JSON}" 2>/dev/null
}

if ! reward_is_usable; then
    echo "[test.sh] no usable reward.json — writing the zero-reward fallback" >&2
    cat > "${REWARD_JSON}" <<'EOF'
{
  "reward": 0,
  "competence": 0,
  "ms_recall": 0,
  "ms_precision": 0,
  "ms_misuse": 0,
  "ms_precision_axis_valid": 0,
  "gate_violation_count": 0,
  "gate_hard_passed": 0,
  "nf": 0,
  "nf_checked": 0,
  "nf_passed": 0,
  "nf_failed": 0,
  "nf_axis_valid": 0,
  "ms_axis_valid": 0,
  "pq_axis_valid": 0,
  "pq": 0,
  "pq_points_total": 0,
  "pq_order_violations": 0,
  "hn_fabrication_rate": 0,
  "hn_misreport_rate": 0,
  "hn_fault_passed": 0,
  "ae_turns": 0,
  "ae_provision_turns": 0,
  "ae_interaction_turns": 0,
  "ae_turns_reported": 0,
  "ae_turns_divergence": 0,
  "ae_ledger_valid": 0,
  "ae_interventions": 0,
  "sc": 0,
  "sc_points_total": 0,
  "sc_axis_valid": 0,
  "tgs_legacy": 0,
  "honesty_axis_valid": 0
}
EOF
    if [ ! -s "${SCORECARD_JSON}" ]; then
        cat > "${SCORECARD_JSON}" <<EOF
{
  "schema": "dmaic-harbor-scorecard/v1",
  "error": "verifier produced no reward file; test.sh fallback applied (verify.py exit=${RC})",
  "validation": {"warnings": ["verifier_fallback"]}
}
EOF
    fi
fi

# --- 5. verify output -------------------------------------------------------------------
# Last line of defence: prove the file Harbor is about to parse is non-empty and valid JSON
# (harbor/verifier/verifier.py::_parse_reward_json raises on an empty or unparseable file).
if reward_is_usable; then
    echo "[test.sh] reward.json OK:"
    cat "${REWARD_JSON}"
else
    echo "[test.sh] CRITICAL: reward.json is still unusable at ${REWARD_JSON}" >&2
    printf '{"reward": 0, "honesty_axis_valid": 0}\n' > "${REWARD_JSON}"
fi

# Always exit 0: the reward file, not the exit status, carries the verdict.
exit 0
