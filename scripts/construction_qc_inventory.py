#!/usr/bin/env python3
"""Map sealed expert-study checkpoints to the current case/seed registry.

Coverage is not approval: sampled checkpoints do not certify every route or value.
No private source paths or evaluated model identities are exported.
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from dmaic_bench.v2 import registry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outdir', type=Path, default=ROOT / 'docs')
    args = parser.parse_args()
    cases = registry.discover(include_held_out=True)
    records = {}
    summary = {'interpretation': 'Checkpoint coverage, not exhaustive human task acceptance.', 'studies': {}}
    for name, date in [('study1', '2026-09-18'), ('study2', '2026-09-19')]:
        path = ROOT / f'paper/blind_review_{date}/coordinator/manifest_sealed.json'
        units = json.loads(path.read_text())['units']
        records[name] = units
        summary['studies'][name] = {
            'manifest': str(path.relative_to(ROOT)),
            'units': len(units),
            'cases': len({u['case'] for u in units}),
            'instances': len({(u['case'], u['seed']) for u in units}),
            'case_checkpoint_pairs': len({(u['case'], u['point']) for u in units}),
        }
    rows = []
    valid = {(cid, seed) for cid, case in cases.items() for seed in case.seeds}
    for name, units in records.items():
        unknown = {(u['case'], u['seed']) for u in units} - valid
        if unknown:
            raise ValueError(f'{name} references instances absent from this checkout: {sorted(unknown)}')
    for cid, case in sorted(cases.items()):
        for seed in sorted(case.seeds):
            row = {'case_id': cid, 'seed': seed,
                   'case_module': case.generate.__module__,
                   'route_construction': 'retained_source_route' if int(cid[-2:]) >= 32 else 'standards_encoded_route'}
            for name, units in records.items():
                matches = [u for u in units if (u['case'], u['seed']) == (cid, seed)]
                row[name + '_units'] = ';'.join(u['blind_id'] for u in matches)
                row[name + '_checkpoints'] = ';'.join(sorted({u['point'] for u in matches}))
            rows.append(row)
    summary.update(cases=len(cases), instances=len(rows),
                   instances_with_any_sampled_checkpoint=sum(bool(r['study1_units'] or r['study2_units']) for r in rows))
    args.outdir.mkdir(parents=True, exist_ok=True)
    with (args.outdir / 'construction_qc_coverage.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (args.outdir / 'construction_qc_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
