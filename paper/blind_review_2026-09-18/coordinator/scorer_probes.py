"""Counterfactual diagnostics of scorer scope; never changes saved scores or trajectories."""
import json, importlib.util
from pathlib import Path
from types import SimpleNamespace as NS

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('frozen_pq',ROOT/'coordinator/pq_snapshot.py')
pq=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pq)
_judge_point=pq._judge_point

refs=json.loads((ROOT/'coordinator/original_reference_points.json').read_text())
out={}
for ident,remove,equivalent in [
    ('B011',{'basic.one_sample_t'},set()),
    ('B018',{'capability.normal'},{'regression.ols'}),
    ('B002',{'power.two_proportions'},{'capability.binomial'}),
]:
    t=json.loads((ROOT/'blind/cases'/ident/'trace.json').read_text())
    p=NS(**refs[ident]);tr=NS(route_decisions=[NS(**d) for d in t.get('route_decisions',[])])
    successful={s['method_id'] for s in t['steps'] if s['status']=='success'}
    out[ident]={
        'actual_verdict':_judge_point(p,tr,successful,{}),
        'removed_methods_from_different_stage':sorted(remove),
        'scope_probe':_judge_point(p,tr,successful-remove,{}),
        'hypothetical_equivalent_source_methods_added':sorted(equivalent),
        'scope_plus_equivalence_probe':_judge_point(p,tr,(successful-remove)|equivalent,{}),
        'note':'Diagnostic counterfactual of method-presence scoring only. No source artifacts or production labels were changed; added source methods are hypothetical representations of already-computed related tests, not new executions. Statistical equivalence must be assessed at the specific decision: a target proportion test and binomial capability are different outputs even when both establish the target relationship.',
    }
(ROOT/'coordinator/scorer_probes.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,indent=2,ensure_ascii=False))
