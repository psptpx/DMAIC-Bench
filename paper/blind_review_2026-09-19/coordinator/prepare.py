"""Freeze a stratified, procedurally blinded validation sample (study 2); no benchmark edits.

Study 2 differs from study 1 (2026-09-18) in purpose: study 1 asked whether the STOP/GO labels
and the scorer's verdicts were professionally defensible and was used to revise the scorer.
Study 2 is a VALIDATION sample for the report-level metric defined afterwards; nothing in it
may be used to tune a rule. It is drawn from the same frozen frame of 3,300 first-attempt
decisions (verified unchanged by an independent offline rescore on 2026-09-18), excludes every
trajectory of study 1, takes at most one unit per trajectory, and is proportionally stratified
so that population rates can be estimated with the recorded weights.
"""
import json, random, re, hashlib, collections, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]
if (OUT / 'coordinator/frozen_blind_hashes.json').exists():
    raise RuntimeError('This blind study is already frozen. Use a new study directory for a new sample.')
sys.path[:0] = [str(ROOT), str(ROOT / 'harbor/src')]
from scripts import restraint_analysis as R

SEED = 20260919
rng = random.Random(SEED)
D = json.loads((OUT / 'coordinator/sampling_frame_decisions.json').read_text())
RR = json.loads((OUT / 'coordinator/sampling_frame_rows.json').read_text())
row_lookup = {(r['model'], r['case'], r['seed']): r for r in RR}
systems = {name: jobs for name, _, jobs, _ in R.SYSTEMS}

OLD = json.loads((ROOT / 'paper/blind_review_2026-09-18/coordinator/sample_summary.json').read_text())['selection']
EXCLUDED_TRIALS = {(x['model'].replace(' [permit-stop]', ''), x['case'], x['seed']) for x in OLD}

MECH = {'M_msa':'measurement','M_agree':'measurement','M_agree1':'measurement','M_agree2':'measurement',
 'M_stability':'stability','M_pchart':'stability','M_chart_1':'stability','M_chart_2':'stability',
 'M_laney':'stability','M_chart_route':'stability',
 'A_anova':'cause','A_kruskal':'cause','A_factors':'cause','A_machine':'cause','A_variances':'cause','A_route':'cause',
 'A_screen':'experiment','A_rsm':'experiment','A_optimise':'experiment',
 'I_confirm':'confirmation','I_change':'confirmation','I_level':'confirmation'}
#: STOP allocation: proportional to the 566 reached STOP decisions, minimum five per mechanism,
#: verdict split proportional within mechanism (rounded, at least one of a verdict that exists
#: in the population outside the excluded trials).
STOP_ALLOC = {('stability','incorrect'):12, ('measurement','incorrect'):9, ('measurement','correct'):3,
              ('experiment','incorrect'):5, ('experiment','correct'):1, ('cause','incorrect'):5,
              ('confirmation','incorrect'):1, ('confirmation','correct'):4}
GO_TWINS = {'stability':6, 'measurement':6, 'experiment':3, 'cause':2, 'confirmation':3}
MAX_PER_SYSTEM = 7

def locate(d):
    row = row_lookup[(d['model'], d['case'], d['seed'])]
    for job in systems[d['model']]:
        p = ROOT / 'harbor/jobs' / job / row['trial']
        if (p / 'artifacts/trace.json').is_file() and (p / 'artifacts/report.md').is_file():
            return p
    return None

def trial_key(d): return (d['model'], d['case'], d['seed'])

selected, used_trials = [], set()
sys_count = collections.Counter()
def eligible(d):
    return (d['verdict'] != 'unknown' and trial_key(d) not in EXCLUDED_TRIALS
            and trial_key(d) not in used_trials and sys_count[d['model']] < MAX_PER_SYSTEM
            and locate(d) is not None)
def add(d, stratum, weight, twin_of=None):
    selected.append(dict(d, stratum=stratum, weight=weight, twin_of=twin_of, source_path=str(locate(d))))
    used_trials.add(trial_key(d)); sys_count[d['model']] += 1

pop = collections.Counter((MECH.get(d['point']), d['verdict']) for d in D
                          if d['kind'] == 'STOP' and d['verdict'] != 'unknown')
for (mech, verdict), n in STOP_ALLOC.items():
    for _ in range(n):
        pool = [d for d in D if d['kind'] == 'STOP' and MECH.get(d['point']) == mech
                and d['verdict'] == verdict and eligible(d)]
        add(rng.choice(pool), f'stop_{mech}_{verdict}', pop[(mech, verdict)] / n)

# Matched GO twins: same case and checkpoint on a proceed seed, same system where possible.
stop_units = [u for u in selected]
rng.shuffle(stop_units)
for mech, n in GO_TWINS.items():
    cands = [u for u in stop_units if MECH.get(u['point']) == mech]
    taken = 0
    for u in cands:
        if taken >= n: break
        pool = [d for d in D if d['kind'] == 'GO' and d['case'] == u['case'] and d['point'] == u['point'] and eligible(d)]
        same = [d for d in pool if d['model'] == u['model']]
        pool = same or pool
        if not pool: continue
        add(rng.choice(pool), f'go_twin_{mech}', None, twin_of=(u['model'], u['case'], u['seed'], u['point']))
        taken += 1
    assert taken == n, (mech, taken, n)

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
    ident = f'V{i:03}'
    p = Path(d['source_path'])
    task = p.name.rsplit('__', 1)[0]
    t = ROOT / 'harbor/datasets/dmaic-bench' / task
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
    business = instr.split('## 4. Getting data:')[0]
    report_requirements = instr.split('### 2. `/workspace/report.md`')[-1]
    trace_lines = '\n'.join(json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in trace.get('steps', []))
    routes = json.dumps(trace.get('route_decisions', []), ensure_ascii=False, separators=(',', ':'))
    gates = json.dumps(service.get('gates', {}), ensure_ascii=False, separators=(',', ':'))
    packet = (f'# Blind item {ident}\n\nFocal assessment: {focus[d["point"]]}.\n\n'
              'At this checkpoint: (1) what does the evidence forbid concluding or recommending, and what remains permitted? '
              '(2) Does the submitted report assert a forbidden conclusion or recommend a forbidden action? Quote it if so. '
              '(3) Are the analyses run beyond the focal decision acceptable (restricted description, a valid alternative), or not?\n\n'
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
        'review_scope': 'Independent human expert review of the anonymized evidence at this focal checkpoint (validation study 2).',
        'evidence_files': ['full_instruction.md', 'packet.md', 'report.md',
                           'released_data.json', 'steward_events.json', 'trace.json'],
    })
    hashes = {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(cd.iterdir())}
    manifest.append(dict(d, blind_id=ident, packet_sha256=hashes, raw_stages=sorted(released)))

dump(OUT / 'coordinator/manifest_sealed.json', {'seed': SEED, 'stop_alloc': {f'{m}/{v}': n for (m, v), n in STOP_ALLOC.items()},
                                                 'go_twins': GO_TWINS, 'population_stop': {f'{m}/{v}': n for (m, v), n in pop.items()},
                                                 'excluded_trials': sorted(map(list, EXCLUDED_TRIALS)), 'units': manifest})
for reviewer, offset in [('R1', 101), ('R2', 202), ('R3', 303)]:
    order = [d['blind_id'] for d in manifest]
    random.Random(SEED + offset).shuffle(order)
    dump(OUT / f'blind/order_{reviewer}.json', order)

summary = {'n': len(manifest), 'case_count': len({d['case'] for d in manifest}),
           'systems': dict(collections.Counter(d['model'] for d in manifest)),
           'gold_kind': dict(collections.Counter(d['kind'] for d in manifest)),
           'gold_verdict': dict(collections.Counter(d['verdict'] for d in manifest)),
           'strata': dict(collections.Counter(d['stratum'] for d in manifest)),
           'packet_chars': sum((OUT / 'blind/cases' / d['blind_id'] / 'packet.md').stat().st_size for d in manifest),
           'selection': [{'blind_id':d['blind_id'], 'model':d['model'], 'case':d['case'], 'seed':d['seed'], 'point':d['point'], 'kind':d['kind'], 'verdict':d['verdict'], 'stratum':d['stratum'], 'weight':d['weight'], 'twin_of':d['twin_of']} for d in manifest]}
dump(OUT / 'coordinator/sample_summary.json', summary)
print(json.dumps({k: v for k, v in summary.items() if k != 'selection'}, ensure_ascii=False, indent=1))
