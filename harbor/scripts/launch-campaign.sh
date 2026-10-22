#!/usr/bin/env bash
#
# THE campaign entry point. Everything a multi-thousand-trial sweep needs to have checked
# before it spends anything, in the order that makes the checks cheap:
#
#     harbor/scripts/launch-campaign.sh -c <job-config.yaml> -p <jobs-dir>/<job-name>
#
#   1. source the credentials from OUTSIDE the working tree     (scripts/campaign-env.sh)
#   2. host preflight -- runtime, builder, base images, disk, credential file mode
#   3. provider liveness -- reachable / auth-ok / has-balance, per configured model
#   4. supervise -- launch, RESUME on a non-clean exit, abort on a broken harness
#
# Each step gates the next. A campaign that fails step 2 costs seconds; the same campaign
# discovering step 2 at trial 400 costs 400 trials, which is what happened.
#
# Skips, for the cases where you mean it:
#   --skip-probe        do not contact any provider (step 3)
#   --skip-preflight    do not check the host (step 2) -- not recommended
#   --dry-run           run steps 1-3 and stop before launching anything
#
# Anything after `--` is passed through to the framework CLI.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
harbor_root="$(dirname "$here")"
repo_root="$(dirname "$harbor_root")"

export PYTHONPATH="$harbor_root/src${PYTHONPATH:+:$PYTHONPATH}"

config=""
job_dir=""
skip_probe=0
skip_preflight=0
dry_run=0
passthrough=()

while [ $# -gt 0 ]; do
    case "$1" in
        -c|--config)     config="${2:?-c needs a path}"; shift 2 ;;
        -p|--job-dir)    job_dir="${2:?-p needs a path}"; shift 2 ;;
        --skip-probe)    skip_probe=1; shift ;;
        --skip-preflight) skip_preflight=1; shift ;;
        --dry-run)       dry_run=1; shift ;;
        --)              shift; passthrough=("$@"); break ;;
        -h|--help)
            sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
            exit 0 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

[ -n "$config" ]  || { echo "usage: $(basename "$0") -c <job-config.yaml> -p <job-dir>" >&2; exit 2; }
[ -n "$job_dir" ] || { echo "usage: $(basename "$0") -c <job-config.yaml> -p <job-dir>" >&2; exit 2; }
[ -f "$config" ]  || { echo "no such job config: $config" >&2; exit 2; }

# --- 1. credentials -----------------------------------------------------------------
# campaign-env.sh refuses to source a file that is missing or not mode 600/400, and reads
# nothing from inside the repository. It is `return`-based, so it must be sourced.
echo "== 1/4  credentials"
# shellcheck source=../../scripts/campaign-env.sh
source "$repo_root/scripts/campaign-env.sh"
echo "        sourced (no value printed, here or anywhere)"

# --- 2. host preflight --------------------------------------------------------------
if [ "$skip_preflight" -eq 1 ]; then
    echo "== 2/4  host preflight SKIPPED by request"
else
    echo "== 2/4  host preflight"
    python3 -m dmaic_harbor.preflight --jobs-dir "$(dirname "$job_dir")" || {
        echo "campaign NOT launched: the host cannot run it. Fix the failures above." >&2
        exit 2
    }
fi

# --- 3. provider liveness -----------------------------------------------------------
if [ "$skip_probe" -eq 1 ]; then
    echo "== 3/4  provider liveness SKIPPED by request"
else
    echo "== 3/4  provider liveness"
    python3 -m dmaic_harbor.probe || {
        rc=$?
        if [ "$rc" -eq 2 ]; then
            echo "campaign NOT launched: no provider config. See the message above, or" >&2
            echo "pass --skip-probe if you have deliberately not configured one." >&2
        else
            echo "campaign NOT launched: at least one contestant cannot serve it." >&2
            echo "Balance exhaustion is not a model result -- every trial it touches" >&2
            echo "would be recorded as one. Fix or drop the contestant, then re-run." >&2
        fi
        exit "$rc"
    }
fi

# --- 4. supervised run --------------------------------------------------------------
if [ "$dry_run" -eq 1 ]; then
    echo "== 4/4  --dry-run: all gates passed; nothing launched"
    exit 0
fi
echo "== 4/4  supervised run"
# The supervisor re-runs the preflight in-process unless told not to; it has already
# passed here, so skip the duplicate.
exec python3 -m dmaic_harbor.supervisor \
    -c "$config" -p "$job_dir" --skip-preflight ${passthrough[@]+"${passthrough[@]}"}
