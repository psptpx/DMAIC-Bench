"""Validate frozen independent reviews and unblind descriptively; no automatic relabeling."""
import json, collections, hashlib, csv, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ids = [f'B{i:03}' for i in range(1,31)]
manifest=json.loads((ROOT/'coordinator/manifest_sealed.json').read_text())['units']
by_id={d['blind_id']:d for d in manifest}
required={'blind_id','gate_verdict','stop_scope','trajectory_verdict','actual_alternative_route',
          'allowed_alternatives','evidence','rationale','confidence','numerical_check','evidence_problem'}
choices={'gate_verdict':{'STOP','GO','UNDETERMINED'},
         'trajectory_verdict':{'ACCEPTABLE','UNACCEPTABLE','MIXED','INSUFFICIENT'},
         'actual_alternative_route':{'VALID','CONDITIONALLY_VALID','INVALID','NONE','UNDETERMINED'}}
reviewers={}
for rid in ['R1','R2','R3']:
    path=ROOT/f'reviews/{rid}.json'
    if not path.exists(): raise FileNotFoundError(f'Independent review pending: {path}')
    r=json.loads(path.read_text())
    assert r['reviewer_id']==rid
    assert r['reviewer_type']=='Human'
    assert sorted(x['blind_id'] for x in r['reviews'])==ids
    for x in r['reviews']:
        assert required<=x.keys(), (rid,x['blind_id'],required-x.keys())
        for field,cats in choices.items(): assert x[field] in cats,(rid,x['blind_id'],field,x[field])
        assert isinstance(x['confidence'],int) and 1<=x['confidence']<=5
    reviewers[rid]={x['blind_id']:x for x in r['reviews']}

def majority(values):
    k,n=collections.Counter(values).most_common(1)[0]
    return k if n>=2 else 'NO_MAJORITY'

def agreement(subids, field):
    cats=sorted(choices[field]);tot=collections.Counter();pairs=[];unanimous=0
    for i in subids:
        c=collections.Counter(reviewers[r][i][field] for r in reviewers);tot.update(c)
        pairs.append(sum(n*(n-1) for n in c.values())/6)
        unanimous+=max(c.values())==3
    observed=sum(pairs)/len(pairs);chance=sum((tot[c]/(3*len(subids)))**2 for c in cats)
    return {'n_units':len(subids),'unanimous_n':unanimous,'unanimous_rate':unanimous/len(subids),
            'pairwise_agreement':observed,'fleiss_kappa':(observed-chance)/(1-chance) if chance<1 else None,
            'vote_counts':dict(tot)}

units=[]
for i in ids:
    d=by_id[i];rr=[reviewers[r][i] for r in reviewers]
    gate=majority([x['gate_verdict'] for x in rr]);conduct=majority([x['trajectory_verdict'] for x in rr])
    alt_n=sum(x['actual_alternative_route'] in {'VALID','CONDITIONALLY_VALID'} for x in rr)
    units.append({'blind_id':i,'case':d['case'],'seed':d['seed'],'system':d['model'],
                  'point':d['point'],'stratum':d['stratum'],'benchmark_label':d['kind'],
                  'benchmark_verdict':d['verdict'],'source_path':d['source_path'],
                  'reviewer_type':'Human','review_language':'English',
                  'source_review_metadata':d['source_review_metadata'],
                  'gate_votes':[x['gate_verdict'] for x in rr],
                  'trajectory_votes':[x['trajectory_verdict'] for x in rr],
                  'alternative_votes':[x['actual_alternative_route'] for x in rr],
                  'majority_gate':gate,'majority_trajectory':conduct,
                  'label_matches_majority':gate==d['kind'],
                  'at_least_two_allow_actual_alternative':alt_n>=2,
                  'candidate_scoring_overpenalty':d['verdict']=='incorrect' and conduct=='ACCEPTABLE',
                  'candidate_scoring_underpenalty':d['verdict']=='correct' and conduct=='UNACCEPTABLE',
                  'review_details':{r:reviewers[r][i] for r in reviewers}})

def subset_summary(us):
    subids=[u['blind_id'] for u in us]
    return {'n':len(us),'gate_agreement':agreement(subids,'gate_verdict'),
            'trajectory_agreement':agreement(subids,'trajectory_verdict'),
            'majority_gate_counts':dict(collections.Counter(u['majority_gate'] for u in us)),
            'majority_conduct_counts':dict(collections.Counter(u['majority_trajectory'] for u in us)),
            'majority_matches_benchmark':sum(u['label_matches_majority'] for u in us),
            'benchmark_stop':{'n':sum(u['benchmark_label']=='STOP' for u in us),
                              'majority_support':sum(u['benchmark_label']==u['majority_gate']=='STOP' for u in us)},
            'benchmark_go':{'n':sum(u['benchmark_label']=='GO' for u in us),
                            'majority_support':sum(u['benchmark_label']==u['majority_gate']=='GO' for u in us)},
            'candidate_scoring_overpenalty':[u['blind_id'] for u in us if u['candidate_scoring_overpenalty']],
            'candidate_scoring_underpenalty':[u['blind_id'] for u in us if u['candidate_scoring_underpenalty']],
            'alternative_supported_by_two':[u['blind_id'] for u in us if u['at_least_two_allow_actual_alternative']]}

frozen=json.loads((ROOT/'coordinator/frozen_blind_hashes.json').read_text())
changed=[f for f,h in frozen['files'].items() if hashlib.sha256((ROOT/'blind'/f).read_bytes()).hexdigest()!=h]
assert not changed,changed
output={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'reviewer_type':'Human',
        'review_method':'Independent review by three human experts using Black Belt methods',
        'language':'English',
        'source_evidence_index':'coordinator/source_evidence.json',
        'editorial_revision':frozen['editorial_revision'],
        'limitations':['Shared materials and rubric may lead to correlated reviewer judgments',
                       'Procedural, not technically enforced, blinding','Enriched stratified sample; no population error-rate estimate',
                       '30 trajectories but only 26 case-seed instances across 15 cases',
                       'Focal professional validity and literal routing conformance are different estimands'],
        'packet_integrity':'All current English packet hashes verified; original dispatch hashes retained separately',
        'review_sha256':{r:hashlib.sha256((ROOT/f'reviews/{r}.json').read_bytes()).hexdigest() for r in reviewers},
        'summary':{name:subset_summary(us) for name,us in [
            ('all',units),('core',[u for u in units if u['stratum'].startswith('core_')]),
            ('boundary',[u for u in units if u['stratum'].startswith('boundary_')])]},
        'units':units}
(ROOT/'results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
fields=['blind_id','case','seed','system','point','stratum','benchmark_label','benchmark_verdict','gate_votes',
        'trajectory_votes','alternative_votes','majority_gate','majority_trajectory','label_matches_majority',
        'at_least_two_allow_actual_alternative','candidate_scoring_overpenalty','candidate_scoring_underpenalty']
with (ROOT/'item_results.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for u in units:w.writerow({k:' / '.join(u[k]) if isinstance(u[k],list) else u[k] for k in fields})
print(json.dumps(output['summary'],indent=2,ensure_ascii=False))
print('DISCREPANCIES')
for u in units:
    if not u['label_matches_majority'] or u['candidate_scoring_overpenalty'] or u['candidate_scoring_underpenalty']:
        print({k:u[k] for k in fields})
