#!/usr/bin/env python3
"""Pre-registered selection of the 32 paired tasks for the replicated instruction control.

16 stop tasks, stratified by stop mechanism in proportion to the 49 stop tasks (stability 6,
measurement 5, cause 2, experiment 2, confirmation 1), at most two per case, drawn with
random.Random(20260919); each paired with a proceed twin: a seed of the same case on which the
correct route passes the same fork on its guarded (proceed) branch, drawn the same way.
Written to docs/control_pairs_2026-09-19.json BEFORE any run. Nothing about any system's
scores enters the selection.
"""
import json, random, sys, collections, importlib, pkgutil, glob
sys.path[:0] = ['.', 'harbor/src']
import dmaic_bench.v2.cases as C
from dmaic_bench.core.graph import walk

MECH = {'M_msa':'measurement','M_agree':'measurement','M_agree1':'measurement','M_agree2':'measurement',
        'M_stability':'stability','M_pchart':'stability','M_chart_1':'stability','M_chart_2':'stability',
        'M_laney':'stability','M_chart_route':'stability',
        'A_anova':'cause','A_kruskal':'cause','A_factors':'cause','A_machine':'cause','A_variances':'cause','A_route':'cause',
        'A_screen':'experiment','A_rsm':'experiment','A_optimise':'experiment',
        'I_confirm':'confirmation','I_change':'confirmation','I_level':'confirmation'}
ALLOC = {'stability': 6, 'measurement': 5, 'cause': 2, 'experiment': 2, 'confirmation': 1}
SEED = 20260919

def last_default_fork(g, route):
    last = None
    for i, n in enumerate(route[:-1]):
        outs = [e for e in g.edges if e.source == n]
        if len(outs) < 2: continue
        taken = [e for e in outs if e.target == route[i + 1]][0]
        if taken.is_default: last = n
    return last

def passes_proceed(g, route, node):
    for i, n in enumerate(route[:-1]):
        if n != node: continue
        outs = [e for e in g.edges if e.source == n]
        taken = [e for e in outs if e.target == route[i + 1]][0]
        return not taken.is_default
    return False

# routing tier per task, read from any complete campaign's scorecards (structure only, no scores)
TIER = {}
for sc in glob.glob('harbor/jobs/gpt6astra-97/*/verifier-rescored/scorecard.json'):
    d = json.load(open(sc)); TIER[(d['case_id'], int(d['seed']))] = d['routing_tier']
stops, proceed_by = [], collections.defaultdict(list)
for m in pkgutil.iter_modules(C.__path__):
    if m.name.startswith('_'): continue
    case = getattr(importlib.import_module('dmaic_bench.v2.cases.' + m.name), 'CASE', None)
    if not case: continue
    routes = {s: walk(case.graph, case.generate(s)[1]) for s in case.seeds}
    for s, r in routes.items():
        f = last_default_fork(case.graph, r)
        if f is None or TIER.get((case.case_id, s)) not in ('B-divert', 'C-stop'): continue
        stops.append({'case': case.case_id, 'seed': s, 'fork': f, 'mech': MECH.get(f, f),
                      'twins': [t for t, rt in routes.items() if t != s and passes_proceed(case.graph, rt, f)]})
rng = random.Random(SEED)
chosen, per_case, used = [], collections.Counter(), set()
for mech, n in ALLOC.items():
    pool = [x for x in stops if x['mech'] == mech and x['twins']]
    rng.shuffle(pool)
    for x in pool:
        if n == 0: break
        if per_case[x['case']] >= 2 or (x['case'], x['seed']) in used: continue
        twins = [t for t in sorted(x['twins']) if (x['case'], t) not in used]
        if not twins: continue
        twin = rng.choice(twins)
        chosen.append({**{k: x[k] for k in ('case', 'seed', 'fork', 'mech')}, 'twin_seed': twin, 'tier': TIER[(x['case'], x['seed'])]})
        used |= {(x['case'], x['seed']), (x['case'], twin)}; per_case[x['case']] += 1; n -= 1
    assert n == 0, (mech, n)
tasks = sorted({f"dmaic-{c['case']}-t3-s{c['seed']}-clean" for c in chosen} | {f"dmaic-{c['case']}-t3-s{c['twin_seed']}-clean" for c in chosen})
out = {'seed': SEED, 'allocation': ALLOC, 'pairs': chosen, 'task_names': tasks, 'n_tasks': len(tasks),
       'population_stop_tasks_by_mech': dict(collections.Counter(x['mech'] for x in stops))}
json.dump(out, open('docs/control_pairs_2026-09-19.json', 'w'), indent=1)
assert len(tasks) == 32, len(tasks)
print(json.dumps({k: v for k, v in out.items() if k not in ('pairs', 'task_names')}, indent=1)); print(len(tasks), 'tasks;', len(chosen), 'pairs'); print([(c['case'], c['seed'], c['fork'], c['tier'], c['twin_seed']) for c in chosen])
