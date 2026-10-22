"""DMAIC-Bench command line.

  python3 -m dmaic_bench list
  python3 -m dmaic_bench validate <case_id|all>
  python3 -m dmaic_bench build [--seeds 1 2] [--variants clean dirty] [--tiers T1 T2 T3]
                                   [--faults] [--cases a b] [--out tasks_index.json]
  python3 -m dmaic_bench scaffold <task_id> --out DIR [--seeds ...] [--faults]
  python3 -m dmaic_bench score <task_id> --trace trace.json --report report.md
                                   [--system SYS] [--out card.json] [--seeds ...] [--faults]
  python3 -m dmaic_bench run-private-adapter <task_id> [--out DIR] [--seeds ...] [--faults]

`run-private-adapter` and `run-matrix` drive a private contestant through
`dmaic_bench.operator_adapters`. Operator-side adapters are not part of the public release,
so in a public checkout both commands exit with a one-line message instead of running.

Task instances are never stored: they rebuild deterministically from (case, tier, seed,
variant, fault), so a task_id alone pins the exact data bytes a contestant saw.
"""
from __future__ import annotations

import argparse
import json
import sys

from . import taxonomy as taxonomy_mod
from .core import registry, validation
from .core.models import to_json, trace_from_dict


_NO_ADAPTER = ("operator-side contestant adapters (dmaic_bench.operator_adapters) are not part "
               "of the public release; this command runs only where an operator has installed them")


def _private_adapter():
    """Import the operator-side adapter, or exit with a plain message when it is absent."""
    try:
        from .operator_adapters import PrivateContestantAdapter
    except ImportError:
        sys.exit(_NO_ADAPTER)
    return PrivateContestantAdapter


def _build_index(args):
    from .tasks.builder import build_all
    cases = registry.discover()
    if getattr(args, "cases", None):
        missing = set(args.cases) - set(cases)
        if missing:
            sys.exit(f"unknown cases: {sorted(missing)}")
        cases = {k: v for k, v in cases.items() if k in args.cases}
    tasks = build_all(cases, seeds=tuple(args.seeds), variants=tuple(args.variants),
                      tiers=tuple(args.tiers), with_faults=args.faults)
    return cases, {t.task_id: t for t in tasks}


def _find_task(args):
    cases, index = _build_index(args)
    task = index.get(args.task_id)
    if task is None:
        near = [tid for tid in index if args.task_id in tid][:10]
        sys.exit(f"task {args.task_id!r} not found. Closest task_ids: {near or list(index)[:10]}")
    return cases[task.case_id], task


def cmd_list(args):
    cases = registry.discover(include_legacy=not args.native_only)
    print(f"{'case_id':<22} {'tier':<4} {'prov':<14} {'y_type':<22} {'stages':>6} {'param':>5}  title")
    for cid, c in sorted(cases.items()):
        m = c.meta
        print(f"{cid:<22} {m.tier:<4} {m.provenance:<14} {m.y_type:<22} "
              f"{len(m.stages):>6} {str(m.parametric):>5}  {m.title}")
    print(f"\n{len(cases)} cases")


def cmd_validate(args):
    if args.case_id == "all":
        cases = registry.discover()
        bad = 0
        for cid, case in sorted(cases.items()):
            findings = validation.validate_case(case)
            errs = validation.errors(findings)
            print(f"{'FAIL' if errs else 'PASS'}  {cid}  ({len(errs)} errors, "
                  f"{len(findings) - len(errs)} warnings)")
            for f in findings:
                print(f"      {f}")
            bad += bool(errs)
        sys.exit(1 if bad else 0)
    import os
    case_dir = os.path.join(registry.CASES_DIR, args.case_id)
    if os.path.isdir(case_dir):
        findings = validation.validate_case_dir(case_dir)
    else:
        case = registry.discover().get(args.case_id)
        if case is None:
            sys.exit(f"unknown case {args.case_id!r}")
        findings = validation.validate_case(case)
    for f in findings:
        print(f)
    errs = validation.errors(findings)
    print("PASS - case may be onboarded" if not errs
          else f"FAIL - {len(errs)} error(s) must be fixed")
    sys.exit(1 if errs else 0)


def cmd_build(args):
    _, index = _build_index(args)
    by_tier = {}
    for t in index.values():
        by_tier.setdefault(t.tier, []).append(t)
    for tier in sorted(by_tier):
        print(f"{tier}: {len(by_tier[tier])} instances")
    print(f"total: {len(index)}")
    if args.out:
        rows = [{"task_id": t.task_id, "case_id": t.case_id, "tier": t.tier, "seed": t.seed,
                 "variant": t.variant, "phase": t.phase,
                 "fault": ({"stage_id": t.fault.stage_id, "method_id": t.fault.method_id}
                           if t.fault else None),
                 "required_methods": [m.method_id for m in t.required_methods()],
                 "truth_count": len(t.truths)}
                for t in index.values()]
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print(f"index -> {args.out}")


def cmd_scaffold(args):
    from .adapters import scaffold
    _, task = _find_task(args)
    out = scaffold.write_scaffold(task, args.out)
    print(f"scaffold -> {out}\nThe contestant must produce trace.json + report.md in that "
          f"directory, then run: "
          f"python3 -m dmaic_bench score {task.task_id} "
          f"--trace {out}/trace.json --report {out}/report.md")


def cmd_score(args):
    from .scoring import scorer
    case, task = _find_task(args)
    with open(args.trace, encoding="utf-8") as f:
        raw = json.load(f)
    raw.setdefault("system_id", args.system)
    raw.setdefault("task_id", task.task_id)
    trace = trace_from_dict(raw)
    with open(args.report, encoding="utf-8") as f:
        report = f.read()
    card = scorer.score_run(task, trace, report, taxonomy_mod.load(), y_type=case.meta.y_type)
    print(to_json(card))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(to_json(card))
        print(f"scorecard -> {args.out}", file=sys.stderr)


def cmd_run_private_adapter(args):
    PrivateContestantAdapter = _private_adapter()
    from .harness.steward import DataSteward
    from .scoring import scorer
    case, task = _find_task(args)
    adapter = PrivateContestantAdapter()
    result = adapter.run(task, DataSteward(task))
    card = scorer.score_run(task, result.trace, result.report, taxonomy_mod.load(),
                            y_type=case.meta.y_type)
    print(to_json(card))
    if args.out:
        import os
        os.makedirs(args.out, exist_ok=True)
        with open(f"{args.out}/trace.json", "w", encoding="utf-8") as f:
            f.write(to_json(result.trace))
        with open(f"{args.out}/report.md", "w", encoding="utf-8") as f:
            f.write(result.report)
        with open(f"{args.out}/scorecard.json", "w", encoding="utf-8") as f:
            f.write(to_json(card))
        print(f"artifacts -> {args.out}", file=sys.stderr)


def cmd_run_matrix(args):
    PrivateContestantAdapter = _private_adapter()
    from .run_matrix import run_matrix
    cases, index = _build_index(args)
    tasks = sorted(index.values(), key=lambda t: (t.tier, t.task_id))  # cheap T1 first
    if args.limit:
        tasks = tasks[:args.limit]
    run_matrix(cases, tasks, PrivateContestantAdapter, args.out, k=args.k, parallel=args.parallel)


def cmd_aggregate(args):
    from .run_matrix import load_cards
    from .scoring import scorer
    cards = []
    for path in args.cards:
        cards.extend(load_cards(path))
    if not cards:
        sys.exit("no ok cards found")
    agg = scorer.aggregate(cards)
    print(to_json(agg))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(to_json(agg))
        print(f"aggregate -> {args.out}", file=sys.stderr)


def _add_build_opts(p):
    p.add_argument("--seeds", nargs="+", type=int, default=[1])
    p.add_argument("--variants", nargs="+", default=["clean"], choices=["clean", "dirty"])
    p.add_argument("--tiers", nargs="+", default=["T1", "T2", "T3"])
    p.add_argument("--faults", action="store_true")
    p.add_argument("--cases", nargs="+")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="dmaic_bench")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="list the cases in the dataset")
    p.add_argument("--native-only", action="store_true")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("validate", help="run the onboarding gates for a case")
    p.add_argument("case_id")
    p.set_defaults(fn=cmd_validate)

    p = sub.add_parser("build", help="build the task-instance manifest")
    _add_build_opts(p)
    p.add_argument("--out")
    p.set_defaults(fn=cmd_build)

    p = sub.add_parser("scaffold", help="write a task scaffold for a framework-shaped system")
    p.add_argument("task_id")
    p.add_argument("--out", required=True)
    _add_build_opts(p)
    p.set_defaults(fn=cmd_scaffold)

    p = sub.add_parser("score", help="score one run")
    p.add_argument("task_id")
    p.add_argument("--trace", required=True)
    p.add_argument("--report", required=True)
    p.add_argument("--system", default="unknown")
    p.add_argument("--out")
    _add_build_opts(p)
    p.set_defaults(fn=cmd_score)

    p = sub.add_parser("run-private-adapter",
                       help="run one task through an operator-only contestant adapter "
                            "(local use only; requires that backend to be reachable)")
    p.add_argument("task_id")
    p.add_argument("--out")
    _add_build_opts(p)
    p.set_defaults(fn=cmd_run_private_adapter)

    p = sub.add_parser("run-matrix",
                       help="batch-run the matrix through an operator-only contestant adapter "
                            "(local use only; resumable, scorecards appended as JSONL)")
    _add_build_opts(p)
    p.add_argument("--k", type=int, default=3)
    p.add_argument("--parallel", type=int, default=1)
    p.add_argument("--limit", type=int, help="run only the first N tasks in sort order (pilot)")
    p.add_argument("--out", required=True, help="scorecard JSONL path (an existing file is resumed, not overwritten)")
    p.set_defaults(fn=cmd_run_matrix)

    p = sub.add_parser("aggregate", help="aggregate scorecard JSONL -> mean + bootstrap CI")
    p.add_argument("cards", nargs="+", help="one or more JSONL files")
    p.add_argument("--out")
    p.set_defaults(fn=cmd_aggregate)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
