"""Freeze a stratified, procedurally blinded human expert review sample; no benchmark edits."""
import json, random, re, hashlib, collections, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]
if (OUT / 'coordinator/frozen_blind_hashes.json').exists():
    raise RuntimeError('This blind study is already frozen. Use a new study directory for a new sample.')
sys.path[:0] = [str(ROOT), str(ROOT / 'harbor/src')]
from scripts import restraint_analysis as R

SEED = 20260918
rng = random.Random(SEED)
D = json.loads((OUT / 'coordinator/sampling_frame_decisions.json').read_text())
RR = json.loads((OUT / 'coordinator/sampling_frame_rows.json').read_text())
row_lookup = {(r['model'], r['case'], r['seed']): r for r in RR}
systems = {name: jobs for name, _, jobs, _ in R.SYSTEMS}

def locate(d):
    row = row_lookup[(d['model'], d['case'], d['seed'])]
    for job in systems[d['model']]:
        p = ROOT / 'harbor/jobs' / job / row['trial']
        if (p / 'artifacts/trace.json').is_file() and (p / 'artifacts/report.md').is_file():
            return p
    return None

def key(d):
    return d['model'], d['case'], d['seed'], d['point']

selected = []
used_trials = set()
def add(d, stratum):
    p = locate(d)
    selected.append(dict(d, stratum=stratum, source_path=str(p)))
    used_trials.add((d['model'], d['case'], d['seed']))

# One uniformly sampled reached STOP checkpoint per case; no correctness balancing.
for case in sorted({d['case'] for d in D}):
    pool = [d for d in D if d['case'] == case and d['kind'] == 'STOP'
            and d['verdict'] != 'unknown' and locate(d)]
    add(rng.choice(pool), 'core_STOP_one_per_case')

# GO contrast: 4 Measure, 3 Analyze, 2 Improve checkpoints, no duplicate trajectory.
for phase, n in [('measure', 4), ('analyze', 3), ('improve', 2)]:
    for _ in range(n):
        pool = [d for d in D if d['kind'] == 'GO' and d['phase'] == phase
                and d['verdict'] != 'unknown'
                and (d['model'], d['case'], d['seed']) not in used_trials and locate(d)]
        add(rng.choice(pool), 'core_GO_' + phase)

# Six preselected boundary checks, chosen before reviewers see any packet.
specs = [
    ('GLM-5.3-Flash', 'adb_c37', 6, 'M_stability', 'boundary_separate_recipe_sample'),
    ('GPT-6-astra', 'adb_c37', 2, 'A_variances', 'boundary_unequal_variances'),
    ('GPT-6-astra', 'adb_c38', 0, 'M_pchart', 'boundary_stable_low_rate'),
    ('GPT-6-astra', 'adb_c33', 2, 'M_agree2', 'boundary_second_measurement_study'),
    ('GPT-6-astra', 'adb_c31', 1, 'M_stability', 'boundary_stability_restraint'),
]
for model, case, seed, point, stratum in specs:
    d = next(d for d in D if key(d) == (model, case, seed, point))
    assert key(d) not in {key(x) for x in selected}
    add(d, stratum)

p = ROOT / 'harbor/jobs/deepseek-v4-pro-97-permit/dmaic-adb_c31-t3-s1-clean__XwhBwcx'
d = next(d for d in D if key(d) == ('DeepSeek-v4-pro', 'adb_c31', 1, 'M_stability'))
card_path = p / 'verifier-rescored/scorecard.json'
if not card_path.is_file(): card_path = p / 'verifier/scorecard.json'
card = json.loads(card_path.read_text())
detail = next(x for x in card['scorecard']['pq']['details'] if x.get('point_id') == 'M_stability')
selected.append(dict(d, model='DeepSeek-v4-pro [permit-stop]', verdict=detail['verdict'],
                     wrong=detail['verdict'] != 'correct', stratum='boundary_qualified_capability_control',
                     source_path=str(p)))

focus = {'D_scope': 'Project scope, stratification, and the population to which subsequent analyses apply',
 'M_msa': 'Whether readings can support substantive analysis after the measurement system study',
 'M_agree': 'Whether classifications can support substantive analysis after the attribute agreement study',
 'M_agree1': 'The first attribute agreement study and subsequent actions',
 'M_agree2': 'The second (repeat) attribute agreement study and subsequent actions',
 'M_stability': 'Baseline temporal stability and the analyses and conclusions that may follow',
 'M_pchart': 'Baseline defect-rate chart stability, business performance, and next steps',
 'M_laney': 'Dispersion-adjusted attribute control charts and subsequent capability analysis',
 'M_chart_route': 'Selection of an attribute control-chart model and treatment of dispersion',
 'M_chart_1': 'Stability of the first quality characteristic and subsequent actions',
 'M_chart_2': 'Stability of the second quality characteristic and subsequent actions',
 'A_route': 'Selection of analysis methods after distribution diagnosis',
 'A_variances': 'Permissible comparisons after diagnosing variance differences between recipe groups',
 'A_anova': 'Conclusions about candidate causes and next steps after group mean comparisons',
 'A_kruskal': 'Conclusions about candidate causes and next steps after group rank comparisons',
 'A_cap': 'Conclusions and next steps after process performance or capability assessment',
 'A_cap_normal': 'Business conclusions and next steps after normal capability analysis',
 'A_cap_2': 'Capability of the second quality characteristic and its implications for subsequent routes',
 'A_cap_binomial': 'Business conclusions and next steps after attribute process performance assessment',
 'A_capability': 'Baseline assessment and capability conclusions',
 'A_machine': 'Causal judgments and next steps after candidate machine-difference analysis',
 'A_screen': 'Factor-screening results and the analyses and conclusions that may follow',
 'A_factors': 'Causal judgments and next steps after candidate-factor analysis',
 'A_rsm': 'Applicability of the response-surface model and the basis for subsequent optimization',
 'A_optimise': 'Optimization results and the basis for subsequent confirmation or implementation',
 'I_confirm': 'Target-attainment, implementation, or closure conclusions after confirmation experiments',
 'I_change': 'Whether before/after comparisons support improvement conclusions',
 'I_level': 'Whether the absolute post-change business level supports target attainment or closure',
 'C_route': 'Selection of control charts or monitoring methods for sustainment'}

def clean_text(s):
    s = re.sub(r'(?:dmaic-)?adb_c\d+-[Tt]\d+-s\d+-[\w-]+(?:__\w+)?', '[TASK]', s)
    s = re.sub(r'adb_c\d+', '[CASE]', s)
    s = re.sub(r'(?i)\b(?:anthropic/|openai/|deepseek/)?(?:gpt[- ]?[\w.-]+|claude[- ][\w.-]+|glm[- ][\w.-]+|deepseek[- ][\w.-]+|qwen[\w.-]*|kimi[- ][\w.-]+)\b', '[SYSTEM]', s)
    return s

def redact_obj(o):
    if isinstance(o, dict):
        return {k: redact_obj(v) for k, v in o.items()
                if k not in {'system_id', 'task_id', 'model', 'model_name', 'seed', 'token_cost', 'wall_clock_s'}}
    if isinstance(o, list): return [redact_obj(v) for v in o]
    if isinstance(o, str): return clean_text(o)
    return o

def dump(p, o):
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + '\n')

rng.shuffle(selected)
manifest = []
for i, d in enumerate(selected, 1):
    ident = f'B{i:03}'
    p = Path(d['source_path'])
    task = p.name.rsplit('__', 1)[0]
    dataset = 'dmaic-bench-permit-stop' if '[permit-stop]' in d['model'] else 'dmaic-bench'
    t = ROOT / 'harbor/datasets' / dataset / task
    if not t.is_dir(): raise FileNotFoundError(t)
    instr = clean_text((t / 'instruction.md').read_text())
    report = clean_text((p / 'artifacts/report.md').read_text())
    trace = redact_obj(json.loads((p / 'artifacts/trace.json').read_text()))
    events = [json.loads(x) for x in (p / 'artifacts/steward-audit.jsonl').read_text().splitlines() if x.strip()]
    released = {x['stage_id'] for x in events if x.get('outcome') == 'data' and x.get('stage_id')}
    blocks = json.loads((t / 'environment/task/blocks.json').read_text())
    public_data = redact_obj({k: v for k, v in blocks.items() if k in released})
    service = json.loads((t / 'environment/task/steward.json').read_text())
    event_fields = ('seq', 'action', 'text', 'stage_id', 'outcome', 'refusal', 'gate', 'detail', 'declarations')
    audit = redact_obj([{k: x.get(k) for k in event_fields if x.get(k) is not None}
                        for x in events if x['action'] != 'status'])
    cd = OUT / 'blind/cases' / ident
    cd.mkdir(parents=True, exist_ok=True)
    dump(cd / 'trace.json', trace)
    dump(cd / 'released_data.json', public_data)
    dump(cd / 'steward_events.json', audit)
    (cd / 'full_instruction.md').write_text(instr)
    (cd / 'report.md').write_text(report)
    # All instructions available. Readable packet avoids repeating the generic interface/schema.
    business = instr.split('## 4. Getting data:')[0]
    report_requirements = instr.split('### 2. `/workspace/report.md`')[-1]
    trace_lines = '\n'.join(json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in trace.get('steps', []))
    routes = json.dumps(trace.get('route_decisions', []), ensure_ascii=False, separators=(',', ':'))
    gates = json.dumps(service.get('gates', {}), ensure_ascii=False, separators=(',', ':'))
    packet = (f'# Blind item {ident}\n\nFocal assessment: {focus[d["point"]]}.\n\n'
              'At this checkpoint, should routine substantive advancement or final conclusions be paused? Separately list the descriptive, exploratory, corrective, or alternative analyses that remain justified.\n\n'
              '## Original assignment (business sections)\n' + business + '\n\n'
              '## Original reporting requirements\n' + report_requirements + '\n\n'
              '## Public data-service thresholds (protocol rules, not independent ground truth)\n```json\n' + gates + '\n```\n\n'
              '## Submitted report (complete, identifiers removed)\n' + report + '\n\n'
              '## Submitted quantitative steps (complete; compact JSONL; self-reported sequence)\n```jsonl\n' + trace_lines + '\n```\n\n'
              '## Submitted route declarations\n```json\n' + routes + '\n```\n\n'
              'Released raw batches, service events and the full original instructions are in this item directory. '
              'Raw batches are the frozen task data for stages logged as released; no oracle outputs or gold routes are supplied.\n')
    (cd / 'packet.md').write_text(packet)
    dump(cd / 'review_metadata.json', {
        'study_id': OUT.name, 'blind_id': ident, 'checkpoint': d['point'],
        'reviewer_type': 'Human', 'reviewer_ids': ['R1', 'R2', 'R3'],
        'review_language': 'English',
        'review_scope': 'Independent human expert review of the anonymized evidence at this focal checkpoint.',
        'evidence_files': ['full_instruction.md', 'packet.md', 'report.md',
                           'released_data.json', 'steward_events.json', 'trace.json'],
    })
    hashes = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(cd.iterdir())}
    manifest.append(dict(d, blind_id=ident, packet_sha256=hashes, raw_stages=sorted(released)))

dump(OUT / 'coordinator/manifest_sealed.json', {'seed': SEED, 'units': manifest})
for reviewer, offset in [('R1', 101), ('R2', 202), ('R3', 303)]:
    order = [d['blind_id'] for d in manifest]
    random.Random(SEED + offset).shuffle(order)
    dump(OUT / f'blind/order_{reviewer}.json', order)

summary = {'n': len(manifest), 'case_count': len({d['case'] for d in manifest}),
           'systems': sorted({d['model'] for d in manifest}),
           'gold_kind': dict(collections.Counter(d['kind'] for d in manifest)),
           'gold_verdict': dict(collections.Counter(d['verdict'] for d in manifest)),
           'packet_chars': sum((OUT / 'blind/cases' / d['blind_id'] / 'packet.md').stat().st_size for d in manifest),
           'selection': [{'blind_id':d['blind_id'], 'model':d['model'], 'case':d['case'], 'seed':d['seed'], 'point':d['point'], 'kind':d['kind'], 'verdict':d['verdict'], 'stratum':d['stratum']} for d in manifest]}
dump(OUT / 'coordinator/sample_summary.json', summary)
print(json.dumps(summary, ensure_ascii=False, indent=2))
