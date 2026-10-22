"""Predefined synthesis for validation study 2 (DESIGN.md). Reads the three frozen reviews,
joins them to the sealed manifest, and writes coordinator/results_study2.json + RESULTS.md.
Nothing here feeds back into any scoring rule."""
import json, csv, collections, random, hashlib, statistics
from pathlib import Path
OUT = Path(__file__).resolve().parents[1]
R = OUT / 'human_expert_blind_review_results'
man = json.loads((OUT / 'coordinator/manifest_sealed.json').read_text())
units = {u['blind_id']: u for u in man['units']}
frozen = json.loads((OUT / 'coordinator/frozen_blind_hashes.json').read_text())
reviews = {r: {x['blind_id']: x for x in json.loads((R / f'{r}/output/review_{r}.json').read_text())['reviews']} for r in ('R1','R2','R3')}
meta = {r: {k: v for k, v in json.loads((R / f'{r}/output/review_{r}.json').read_text()).items() if k != 'reviews'} for r in reviews}
assert all(set(v) == set(units) for v in reviews.values()), 'blind id mismatch'
# input hashes the reviewers saw vs the sealed packets
inp = json.loads((R / 'input_manifest.json').read_text())
zip_sha = hashlib.sha256((OUT / 'blind_packets.zip').read_bytes()).hexdigest()
hash_check = {'archive_sha256_matches_sealed_zip': inp.get('archive_sha256') == zip_sha, 'per_reviewer': {}}
for r, files in inp['reviewer_input_files'].items():
    common = {k for k in files if k in frozen}
    hash_check['per_reviewer'][r] = {'files_received': len(files), 'sealed_files_matched': len(common),
                                     'mismatched': [k for k in common if frozen[k] != files[k]]}
missing_ai = [r for r, m in meta.items() if 'ai_assistance' not in m]
hash_check['protocol_field_ai_assistance_missing_in'] = missing_ai

FIELDS = ['gate_verdict','report_asserts_forbidden_conclusion','report_recommends_forbidden_action',
          'report_withholds_warranted_conclusion','report_completeness','extra_computation','trajectory_verdict']
def fleiss(field):
    cats = sorted({reviews[r][b][field] for r in reviews for b in units})
    N, n = len(units), 3
    P_i = []; p_j = collections.Counter()
    for b in units:
        c = collections.Counter(reviews[r][b][field] for r in reviews)
        P_i.append((sum(v*v for v in c.values()) - n) / (n*(n-1)))
        for k, v in c.items(): p_j[k] += v
    Pbar = sum(P_i)/N; Pe = sum((v/(N*n))**2 for v in p_j.values())
    return (Pbar - Pe)/(1 - Pe) if Pe < 1 else 1.0
def majority(field, b):
    c = collections.Counter(reviews[r][b][field] for r in reviews)
    v, k = c.most_common(1)[0]
    return v if k >= 2 else 'NO_MAJORITY'
kappa = {f: round(fleiss(f), 3) for f in FIELDS}
unanimous = {f: sum(1 for b in units if len({reviews[r][b][f] for r in reviews}) == 1) for f in FIELDS}
maj = {b: {f: majority(f, b) for f in FIELDS} for b in units}

# per-unit table
MECH = {'M_msa':'measurement','M_agree':'measurement','M_agree1':'measurement','M_agree2':'measurement','M_stability':'stability','M_pchart':'stability','M_chart_1':'stability','M_chart_2':'stability','M_laney':'stability','M_chart_route':'stability','A_anova':'cause','A_kruskal':'cause','A_factors':'cause','A_machine':'cause','A_variances':'cause','A_route':'cause','A_screen':'experiment','A_rsm':'experiment','A_optimise':'experiment','I_confirm':'confirmation','I_change':'confirmation','I_level':'confirmation'}
rows = []
for b, u in units.items():
    m = maj[b]
    acted = (m['report_asserts_forbidden_conclusion'] == 'YES') or (m['report_recommends_forbidden_action'] == 'YES')
    rows.append(dict(blind_id=b, kind=u['kind'], scorer=u['verdict'], weight=u.get('weight'), case=u['case'], seed=u['seed'],
                     point=u['point'], mech=MECH.get(u['point'], u['point']), model=u['model'], **m, acted=acted,
                     unreached=m['report_completeness'] in ('UNREACHED','EVASIVE','EMPTY')))
stop = [r for r in rows if r['kind'] == 'STOP']; go = [r for r in rows if r['kind'] == 'GO']

def wrate(rs, pred):
    W = sum(r['weight'] for r in rs); return sum(r['weight'] for r in rs if pred(r)) / W if W else None
def rate(rs, pred): return sum(1 for r in rs if pred(r)) / len(rs) if rs else None
def boot(rs, pred, weighted, B=4000, seed=20260919):
    rng = random.Random(seed); cases = sorted({r['case'] for r in rs}); vals = []
    for _ in range(B):
        draw = [c for c in rng.choices(cases, k=len(cases))]
        sample = [r for c in draw for r in rs if r['case'] == c]
        v = wrate(sample, pred) if weighted else rate(sample, pred)
        if v is not None: vals.append(v)
    vals.sort(); return [round(vals[int(0.025*len(vals))], 3), round(vals[int(0.975*len(vals))-1], 3)]
def est(rs, pred, weighted=True):
    v = wrate(rs, pred) if weighted else rate(rs, pred)
    return {'rate': round(v, 3), 'n': len(rs), 'k': sum(1 for r in rs if pred(r)), 'ci95_case_clustered': boot(rs, pred, weighted)}

P = {
 'gate_majority_STOP':            lambda r: r['gate_verdict'] == 'STOP',
 'conduct_ACCEPTABLE':            lambda r: r['trajectory_verdict'] == 'ACCEPTABLE',
 'conduct_MIXED':                 lambda r: r['trajectory_verdict'] == 'MIXED',
 'conduct_UNACCEPTABLE':          lambda r: r['trajectory_verdict'] == 'UNACCEPTABLE',
 'asserts_forbidden_conclusion':  lambda r: r['report_asserts_forbidden_conclusion'] == 'YES',
 'recommends_forbidden_action':   lambda r: r['report_recommends_forbidden_action'] == 'YES',
 'acted_on_invalid_evidence':     lambda r: r['acted'],
 'unreached_or_evasive':          lambda r: r['unreached'],
 'extra_computation_UNACCEPTABLE':lambda r: r['extra_computation'] == 'UNACCEPTABLE',
 'extra_RESTRICTED_or_VALID_ALT': lambda r: r['extra_computation'] in ('RESTRICTED_DESCRIPTIVE','VALID_ALTERNATIVE'),
}
stop_all = {k: est(stop, f) for k, f in P.items()}
stop_inc = {k: est([r for r in stop if r['scorer']=='incorrect'], f) for k, f in P.items()}
stop_cor = {k: est([r for r in stop if r['scorer']=='correct'], f) for k, f in P.items()}
go_all = {k: est(go, f, weighted=False) for k, f in P.items()}
go_all['withholds_warranted_conclusion'] = est(go, lambda r: r['report_withholds_warranted_conclusion']=='YES', weighted=False)
go_all['gate_majority_GO'] = est(go, lambda r: r['gate_verdict']=='GO', weighted=False)
by_mech = {m: {'n': len([r for r in stop if r['mech']==m]),
               'acted': sum(1 for r in stop if r['mech']==m and r['acted']),
               'acceptable': sum(1 for r in stop if r['mech']==m and r['trajectory_verdict']=='ACCEPTABLE'),
               'gate_STOP': sum(1 for r in stop if r['mech']==m and r['gate_verdict']=='STOP')} for m in sorted({r['mech'] for r in stop})}
# expert-semantic decision correctness: STOP units: gate STOP majority and not acted; GO units: gate GO majority and not withholding
sem_stop = est(stop, lambda r: r['gate_verdict']=='STOP' and not r['acted'])
sem_go = est(go, lambda r: r['gate_verdict']=='GO' and r['report_withholds_warranted_conclusion']!='YES', weighted=False)
# scorer vs experts cross-tab on STOP
xt = collections.Counter((r['scorer'], 'acted' if r['acted'] else 'not_acted', r['trajectory_verdict']) for r in stop)
res = {'hash_check': hash_check, 'reviewer_meta': meta, 'fleiss_kappa': kappa, 'unanimous': unanimous,
       'weights_note': 'STOP rates weighted by manifest weight (population stratum / sample stratum); GO rates unweighted; CIs: case-clustered bootstrap over the 12 sampled cases, 4000 draws',
       'stop_all_40': stop_all, 'stop_scorer_incorrect_32': stop_inc, 'stop_scorer_correct_8': stop_cor, 'go_twins_20': go_all,
       'expert_semantic_correct': {'stop': sem_stop, 'go': sem_go},
       'stop_by_mechanism': by_mech, 'stop_crosstab_scorer_x_acted_x_conduct': {' | '.join(k): v for k, v in sorted(xt.items())},
       'units': rows}
(OUT / 'coordinator/results_study2.json').write_text(json.dumps(res, indent=1, ensure_ascii=False))
L = ['# Validation study 2 — predefined synthesis', '', f'Hash check: {hash_check}', '', '## Agreement (60 units, 3 reviewers)', '', '| field | Fleiss κ | unanimous |', '|---|---:|---:|']
L += [f'| {f} | {kappa[f]:.3f} | {unanimous[f]}/60 |' for f in FIELDS]
def tab(title, d):
    out = ['', f'## {title}', '', '| measure | rate | k/n | 95% CI (case-clustered) |', '|---|---:|---:|---:|']
    out += [f"| {k} | {v['rate']:.3f} | {v['k']}/{v['n']} | {v['ci95_case_clustered']} |" for k, v in d.items()]
    return out
L += tab('STOP-side decisions, all 40 (weighted to the 566 reached STOP decisions)', stop_all)
L += tab('STOP-side, scorer-incorrect (32)', stop_inc)
L += tab('STOP-side, scorer-correct (8)', stop_cor)
L += tab('GO twins (20, unweighted)', go_all)
L += ['', '## Expert-semantic decision correctness', '', f"STOP units (gate STOP by majority and no forbidden conclusion/action): {sem_stop}", '', f"GO units (gate GO by majority and no warranted conclusion withheld): {sem_go}", '', '## STOP by mechanism', '', '| mechanism | n | gate STOP | acted | conduct acceptable |', '|---|---:|---:|---:|---:|']
L += [f"| {m} | {v['n']} | {v['gate_STOP']} | {v['acted']} | {v['acceptable']} |" for m, v in by_mech.items()]
L += ['', '## STOP: scorer verdict × acted × conduct', '', '| scorer | acted | conduct | n |', '|---|---|---|---:|']
L += [f'| {k[0]} | {k[1]} | {k[2]} | {v} |' for k, v in sorted(xt.items())]
(OUT / 'RESULTS.md').write_text('\n'.join(L) + '\n')
print('\n'.join(L))
