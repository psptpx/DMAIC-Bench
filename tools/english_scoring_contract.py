"""Replay English scoring fixtures against the pre-0.2.0 release contract.

Four synthetic report/trace scenarios per v1 task cover correct, wrong, absent,
and honestly disclosed analyses. This is regression coverage, not a claim that
historical model trials were rerun or that every possible report is equivalent.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dmaic_bench.core import registry
from dmaic_bench.core.models import Trace, TraceStep, RouteDecision
from dmaic_bench.tasks import builder
from dmaic_bench.scoring import scorer
from dmaic_bench import taxonomy


def snapshot():
    cases = registry.discover()
    tax = taxonomy.load()
    result = {}
    tasks = builder.build_all(cases, seeds=(1, 2, 3), variants=('clean', 'dirty'),
                              with_faults=True, languages=('en',))
    for task in tasks:
        for kind in ('correct', 'wrong', 'missing', 'disclosed'):
            steps, lines = [], []
            for stage in task.stages:
                for method in stage.methods:
                    denied = (kind == 'disclosed' and task.fault
                              and task.fault.method_id == method.method_id)
                    if kind == 'missing' or denied:
                        continue
                    truths = [truth for truth in task.truths
                              if truth.method_id == method.method_id
                              and truth.stage_id == stage.stage_id]
                    values = {truth.field: truth.expected + (10000 if kind == 'wrong' else 0)
                              for truth in truths}
                    steps.append(TraceStep(step_id=len(steps) + 1,
                                           method_id=method.method_id, outputs=values))
                    lines.extend(f'{stage.label}: {method.method_id} {field} = {value}'
                                 for field, value in values.items())
            if kind == 'disclosed':
                lines.append('The requested data was withheld. This analysis was not performed.')
            trace = Trace(
                system_id='compatibility-fixture', task_id=task.task_id, steps=tuple(steps),
                route_decisions=tuple(RouteDecision(point=d.point_id,
                                                    chosen_branch=d.correct_branch)
                                      for d in task.decision_points),
                turns=3, wall_clock_s=1,
            )
            result[task.task_id + '/' + kind] = scorer.score_run(
                task, trace, '\n'.join(lines), tax, y_type=cases[task.case_id].meta.y_type)
    return result


def digest(cards):
    return hashlib.sha256(json.dumps(cards, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def check():
    expected = json.loads((ROOT / 'tests/fixtures/english_scoring_contract.json').read_text())
    cards = snapshot()
    return len(cards) == expected['count'] and digest(cards) == expected['sha256']


if __name__ == '__main__':
    ok = check()
    print('English scoring fixtures unchanged' if ok else 'English scoring fixtures changed')
    raise SystemExit(not ok)
