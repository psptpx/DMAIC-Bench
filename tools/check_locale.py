"""Validate canonical English cases, generated blocks, routing and disclosure surfaces.

Run ``python3 tools/check_locale.py [case_id ...]`` before publishing a corpus.
The historical command name is retained; no translation overlays are loaded.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

_BENCH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BENCH)
sys.path.insert(0, os.path.join(_BENCH, "harbor", "src"))

from dmaic_bench.core import i18n, registry            # noqa: E402
from dmaic_bench.tasks import builder                  # noqa: E402
from dmaic_harbor import build as harbor_build         # noqa: E402
from dmaic_harbor import steward_service               # noqa: E402


def romanised_identities() -> list:
    """Latin identity strings from the developer-only map, which never ships."""
    path = os.path.join(_BENCH, "dmaic_bench", "cases", "_identity_map.json")
    if not os.path.exists(path):
        return []
    out = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if (isinstance(v, str)
                        and k in ("title", "internal_title", "former_case_id",
                                  "legacy_source_id", "source")
                        and len(v.strip()) >= 3 and v.strip().isascii()):
                    out.add(v.strip().lower())
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    with open(path, encoding="utf-8") as fh:
        walk(json.load(fh))
    return sorted(out)


def check_case(case, lang: str) -> list:
    problems = []
    try:
        localized = i18n.localize_case(case, lang)
    except i18n.OverlayError as exc:
        return [f"language: {exc}"]

    meta = localized.meta
    stage_dicts = [{"stage_id": s.stage_id, "topics": list(s.topics), "label": s.label}
                   for s in meta.stages]
    problems += [f"topics: {p}" for p in steward_service.topic_problems(stage_dicts)]
    for sid, hits in sorted(harbor_build.steward_label_leaks(stage_dicts).items()):
        problems.append(f"labels: {sid} names method(s) {hits}")

    for field in ("title", "context", "goal"):
        text = getattr(meta, field)
        if i18n.has_cjk(text):
            problems.append(f"residual: `{field}` still carries source-language text")
    for s in meta.stages:
        for field in ("label", "summary_fact"):
            if i18n.has_cjk(getattr(s, field) or ""):
                problems.append(f"residual: {s.stage_id}.{field} still carries source text")
        for t in s.topics:
            if i18n.has_cjk(t):
                problems.append(f"residual: {s.stage_id} topic {t!r} is source-language")

    data = localized.generate(1)
    for path, text in i18n.residual_source_strings(data.blocks)[:40]:
        problems.append(f"blocks: {path} = {text!r} is not English")

    surfaces = [meta.title, meta.context, meta.goal]
    surfaces += [s.label for s in meta.stages]
    surfaces += [t for s in meta.stages for t in s.topics]
    surfaces += [str(v) for _, v in i18n.residual_source_strings(data.blocks)]
    blob = "\n".join(surfaces).lower()
    for name in romanised_identities():
        if re.search(r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])", blob):
            problems.append(
                f"identity: the text contains {name!r}, which is an organisation identity in "
                "cases/_identity_map.json — no CJK-keyed hygiene guard can see it in Latin")

    tasks = builder.build_tasks(case, seeds=(1,), variants=("clean",),
                               tiers=("T1", "T2", "T3"), with_faults=True, languages=(lang,))
    for task in tasks:
        try:
            harbor_build.build_instruction(task)
        except harbor_build.MethodLeak as exc:
            problems.append(f"context: {exc}")
            break
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cases", nargs="*", help="case ids; default every canonical case")
    ap.add_argument("--lang", default="en", choices=i18n.LANGUAGES)
    args = ap.parse_args(argv)

    all_cases = registry.discover()
    wanted = args.cases or [cid for cid, c in sorted(all_cases.items())
                            if args.lang in i18n.languages_for(c.meta)]
    bad = 0
    for case_id in wanted:
        case = all_cases.get(case_id)
        if case is None:
            print(f"{case_id}: UNKNOWN CASE")
            bad += 1
            continue
        problems = check_case(case, args.lang)
        if problems:
            bad += 1
            print(f"{case_id}: {len(problems)} problem(s)")
            for p in problems:
                print(f"    {p}")
        else:
            print(f"{case_id}: ok")
    print(f"\n{len(wanted) - bad}/{len(wanted)} clean")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
