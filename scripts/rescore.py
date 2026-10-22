#!/usr/bin/env python3
"""Re-score finished trials from their retained artifacts, with no model calls.

WHY THIS EXISTS
---------------
A scorer fix makes every number measured before it incomparable with every number measured
after. That is not hypothetical: `basic.normality` was evidence of a branch until 2026-09-13,
and removing it moves decision-point verdicts. Running a second contestant against the fixed
scorer while the first one's numbers stand under the old one produces a ranking that is partly
an artefact of WHEN each was run.

Harbor keeps `trace.json`, `report.md` and `steward-audit.jsonl` for every trial, and those
are the only channel by which agent output reaches the verifier. So the verdict is a pure
function of (retained artifacts, truth package, scorer) and can be recomputed for free.

WHAT IT DOES NOT DO
-------------------
It never overwrites `verifier/`. That directory is the record of what was actually reported at
the time, and a re-score that destroys it also destroys the evidence that the numbers changed.
Results land in `verifier-rescored/` beside it.

    scripts/rescore.py harbor/jobs/<job> [<job> ...] [--dataset DIR] [--apply]

Without `--apply` it reports the delta and writes nothing.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from dmaic_harbor import verify as VF                       # noqa: E402

DEFAULT_DATASET = _ROOT / "harbor" / "datasets" / "dmaic-bench"


def truth_for(task_dir_name: str, dataset: Path) -> Path | None:
    p = dataset / task_dir_name / "tests" / "stage" / "truth.json"
    return p if p.is_file() else None


def rescore_trial(trial: Path, dataset: Path):
    """``(old_reward, new_reward, card)`` or None when the trial cannot be re-scored."""
    artifacts = trial / "artifacts"
    old_path = trial / "verifier" / "reward.json"
    if not artifacts.is_dir() or not old_path.is_file():
        return None
    # The trial directory is `<task-dir-name>__<suffix>`.
    truth = truth_for(trial.name.rsplit("__", 1)[0], dataset)
    if truth is None:
        return None
    try:
        old = float((json.loads(old_path.read_text(encoding="utf-8")) or {}).get("reward"))
    except (ValueError, TypeError, OSError):
        return None
    reward, card = VF.score(str(truth), str(artifacts))
    return old, float(reward.get("reward") or 0.0), (reward, card)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("jobs", nargs="+")
    ap.add_argument("--dataset", default=str(DEFAULT_DATASET))
    ap.add_argument("--apply", action="store_true",
                    help="write verifier-rescored/ beside verifier/ (never over it)")
    args = ap.parse_args(argv)
    dataset = Path(args.dataset)

    moved, same, skipped = [], 0, 0
    for job in args.jobs:
        for trial in sorted(Path(job).iterdir()):
            if not trial.is_dir():
                continue
            got = rescore_trial(trial, dataset)
            if got is None:
                skipped += 1
                continue
            old, new, (reward, card) = got
            if abs(old - new) > 1e-9:
                moved.append((trial.name, round(old, 4), round(new, 4)))
            else:
                same += 1
            if args.apply:
                out = trial / "verifier-rescored"
                out.mkdir(exist_ok=True)
                (out / "reward.json").write_text(
                    json.dumps(reward, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                (out / "scorecard.json").write_text(
                    json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"re-scored: {same + len(moved)}   unchanged: {same}   MOVED: {len(moved)}   "
          f"skipped: {skipped}")
    for name, old, new in sorted(moved, key=lambda r: abs(r[2] - r[1]), reverse=True)[:25]:
        print(f"   {name[:44]:44} {old:.4f} -> {new:.4f}  ({new - old:+.4f})")
    if not args.apply:
        print("\n(dry run; pass --apply to write verifier-rescored/)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
