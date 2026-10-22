#!/usr/bin/env bash
#
# End-to-end proof of the Harbor port, without Harbor's runtime.
#
# Harbor's docker provider shells out to the literal `docker` binary
# (harbor/environments/docker/docker.py: shutil.which("docker")), and this workstation has
# podman only. So this script performs Harbor's own sequence by hand, in the same order and
# with the same isolation, and checks the same artifact Harbor would read:
#
#   1. build the agent image      from <task>/environment/   (Harbor: the agent env)
#   2. build the verifier image   from <task>/tests/         (Harbor: _verifier_env_build_context)
#   3. run the agent  --network none, mounting solution/ at /solution   (Harbor: OracleAgent)
#   4. collect the [[artifacts]] declared in task.toml       (Harbor: _collect_artifacts)
#   5. run the verifier --network none with them re-materialised at their SOURCE paths,
#      which is what Harbor does                             (Harbor: _run_separate_verifier)
#   6. read /logs/verifier/reward.json                       (Harbor: _parse_reward_json)
#
# It also asserts the property the whole design exists for: **no truth value is reachable
# inside the agent image**, while the verifier image holds the truth package.
#
# CAVEAT, stated because it bit us: this script tests our READING of Harbor. It caught three
# real breaks, but it cannot replace `harbor run` -- an earlier version mounted the artifacts
# under /logs/artifacts, scored 1.000, and hid a defect that made a genuine `harbor run` score
# 0.000. Run both.
#
# Usage:  scripts/e2e.sh <task-dir>            # a directory produced by dmaic_harbor.build
#
set -euo pipefail

TASK="${1:?usage: e2e.sh <task-dir>}"
TASK="$(cd "$TASK" && pwd)"
NAME="$(basename "$TASK")"
RUN="$(mktemp -d)"
AGENT_IMG="adm-agent:e2e"
VERIFIER_IMG="adm-verifier:e2e"

command -v podman >/dev/null || { echo "podman not found"; exit 2; }
trap 'echo; echo "artifacts + verifier output kept at: $RUN"' EXIT

say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }

say "task: $NAME"
mkdir -p "$RUN/artifacts" "$RUN/verifier"

say "1/6  build agent image  <- environment/"
podman build -q -t "$AGENT_IMG" "$TASK/environment" >/dev/null

say "2/6  build verifier image  <- tests/"
podman build -q -t "$VERIFIER_IMG" "$TASK/tests" >/dev/null

say "3/6+4/6  run the oracle agent (--network none) and collect artifacts"
# solution/ is mounted, never built into the image: Harbor's OracleAgent uploads it at run
# time and the rubric's tests_or_solution_in_image forbids baking it in.
podman run --rm --network none \
    -v "$TASK/solution:/solution:ro" -v "$RUN/artifacts:/out:z" \
    "$AGENT_IMG" /usr/local/bin/entrypoint.sh bash -lc '
        bash /solution/solve.sh >/tmp/solve.log 2>&1 || echo "solve.sh exit=$?"
        for f in trace.json report.md; do
            [ -f "/workspace/$f" ] && cp "/workspace/$f" /out/
        done
        [ -f /workspace/.steward/audit.jsonl ] && \
            cp /workspace/.steward/audit.jsonl /out/steward-audit.jsonl
        tail -2 /tmp/solve.log
    '
echo "collected: $(ls -1 "$RUN/artifacts" | tr '\n' ' ')"

say "5/6+6/6  run the separate verifier (--network none) and read the reward"
# Harbor re-materialises each [[artifacts]] entry at its ORIGINAL `source` path, NOT under
# /logs/artifacts ("Every entry is uploaded to its original source path" --
# harbor/trial/artifact_handler.py::upload_artifacts). Mount them the way Harbor does, or this
# script tests our assumption instead of the framework's behaviour -- which is exactly how a
# task that scored 1.000 here scored 0.000 under a real `harbor run`.
mkdir -p "$RUN/workspace/.steward"
cp "$RUN/artifacts/trace.json"          "$RUN/workspace/trace.json"          2>/dev/null || true
cp "$RUN/artifacts/report.md"           "$RUN/workspace/report.md"           2>/dev/null || true
cp "$RUN/artifacts/steward-audit.jsonl" "$RUN/workspace/.steward/audit.jsonl" 2>/dev/null || true

podman run --rm --network none \
    -v "$RUN/workspace:/workspace:ro,z" -v "$RUN/verifier:/logs/verifier:z" \
    "$VERIFIER_IMG" bash /tests/test.sh >/dev/null 2>&1 || true

test -s "$RUN/verifier/reward.json" || { echo "FAIL: no reward.json"; exit 1; }
python3 -m json.tool < "$RUN/verifier/reward.json"

say "isolation check: is any truth value reachable inside the AGENT image?"
# Only values that are actually EVIDENCE of a leak are probed. A truth of 0.0 or 1.0 is a
# substring of half the decimals in any JSON file, so grepping for it reports a leak on every
# task and the check stops meaning anything -- it fired on TASK.md, blocks.json and a .pyc the
# first time this ran. A value is probeable when it carries >= 3 significant digits; the rest
# are counted and named, never silently dropped, because "not probeable" and "absent" are
# different claims and only one of them is reassuring.
python3 - "$TASK" "$RUN/truthvals.txt" "$RUN/unprobeable.txt" <<'PY'
import json, sys, pathlib
t = json.loads((pathlib.Path(sys.argv[1]) / "tests" / "stage" / "truth.json").read_text())
probeable, weak = set(), set()
for e in t.get("truths", []):
    v = e.get("expected")
    if not isinstance(v, (int, float)):
        continue
    s = f"{round(float(v), 6):g}"
    digits = sum(c.isdigit() for c in s.lstrip("-0.").rstrip("0"))
    (probeable if digits >= 3 else weak).add(s)
pathlib.Path(sys.argv[2]).write_text("\n".join(sorted(probeable)))
pathlib.Path(sys.argv[3]).write_text("\n".join(sorted(weak)))
PY
echo "probeable truth values: $(tr '\n' ' ' < "$RUN/truthvals.txt")"
if [ -s "$RUN/unprobeable.txt" ]; then
    echo "not probeable (too few digits to be evidence): $(tr '\n' ' ' < "$RUN/unprobeable.txt")"
fi
if [ ! -s "$RUN/truthvals.txt" ]; then
    echo "  NOTE: no truth here is distinctive enough to grep for. Isolation is asserted for"
    echo "        this task by construction (build.py never writes truth into the agent"
    echo "        context) and by the build test suite -- not by the probe below."
fi

podman run --rm -v "$RUN/truthvals.txt:/tv.txt:ro" "$AGENT_IMG" bash -lc '
    hits=0
    while read -r v; do
        [ -z "$v" ] && continue
        found=$(grep -rlF --exclude-dir=__pycache__ -- "$v" \
                    /opt/dmaic /workspace /usr/local/bin 2>/dev/null | head -3)
        if [ -n "$found" ]; then echo "  *** LEAK  $v  in: $found"; hits=$((hits+1)); fi
    done < /tv.txt
    echo "  truth values reachable in the agent image: $hits"
    echo "  payload the agent can read: $(ls -1 /opt/dmaic/task/ | tr "\n" " ")"
    [ "$hits" -eq 0 ] || exit 1
'

say "control: the VERIFIER image does hold the truth"
podman run --rm "$VERIFIER_IMG" python3 -c '
import json
d = json.load(open("/opt/dmaic/verifier/truth.json"))
print("  truths:", len(d.get("truths", [])), "| task:", d.get("task_id"))
'

say "PASS"
