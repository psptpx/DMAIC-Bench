"""Fingerprint published English task inputs and numerical grading contracts.

Run with --check to verify the pre-migration snapshot (seeds 1-3, clean/dirty/fault
v1 tasks and all declared public v2 seeds). The snapshot is a compatibility fixture,
not historical model output. Update it only for a deliberately versioned task change.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'harbor/src')]
from dmaic_bench.core import registry
from dmaic_bench.tasks import builder
from dmaic_harbor import build as harbor_build, v2_tasks

FIXTURE = ROOT / 'tests/fixtures/english_release_contract.json'


def normalize(value):
    if dataclasses.is_dataclass(value):
        return normalize(dataclasses.asdict(value))
    if isinstance(value, dict):
        return {str(k): normalize(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [normalize(v) for v in value]
    if hasattr(value, 'tolist'):
        return value.tolist()
    return value


def fingerprint(surfaces):
    surfaces = normalize(surfaces)
    # Derivation prose was translated; metric cues dropped source-language alternatives.
    # Their English behavior is checked separately by scoring regression tests.
    surfaces['truths'] = [
        {k: v for k, v in t.items() if k not in ('derivation', 'metric_cue')}
        for t in surfaces['truths']]
    return hashlib.sha256(json.dumps(surfaces, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def snapshot():
    tasks = builder.build_all(registry.discover(), seeds=(1, 2, 3),
                              variants=('clean', 'dirty'), with_faults=True)
    for case in harbor_build.v2_cases().values():
        for seed in case.seeds:
            tasks.append(v2_tasks.build_task(case, seed))
            if v2_tasks.safe_fault_target(case, seed) is not None:
                tasks.append(v2_tasks.build_task(case, seed, with_fault=True))
    result = {}
    for task in tasks:
        if task.task_id in result:
            raise ValueError(f'duplicate task ID: {task.task_id}')
        result[task.task_id] = fingerprint({
            'instruction': harbor_build.build_instruction(task),
            'blocks': task.data.blocks,
            'steward': harbor_build.build_steward_config(task),
            'oracle': harbor_build.build_oracle_plan(task),
            'truths': task.truths,
        })
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare against the recorded release')
    args = parser.parse_args()
    actual = snapshot()
    if args.check:
        expected = json.loads(FIXTURE.read_text())['tasks']
        changed = sorted(k for k in expected.keys() | actual.keys()
                         if expected.get(k) != actual.get(k))
        if changed:
            print('Changed task contracts:\n' + '\n'.join(changed))
            return 1
        print(f'{len(actual)} English task contracts unchanged')
    else:
        print(json.dumps(actual, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
