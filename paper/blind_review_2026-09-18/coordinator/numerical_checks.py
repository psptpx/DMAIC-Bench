"""Supplemental coordinator computations on released raw data; not reviewer votes."""
import json, math
from pathlib import Path
from itertools import combinations
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.oneway import anova_oneway

ROOT = Path(__file__).resolve().parents[1]
out = {}
for p in sorted((ROOT / 'blind/cases').iterdir()):
    data = json.loads((p / 'released_data.json').read_text())
    checks = {}
    for name, b in data.items():
        if not isinstance(b, dict): continue
        d = b.get('data')
        if isinstance(d, list) and len(d) > 2 and all(isinstance(x, (float, int)) for x in d):
            a = np.array(d); mr = np.abs(np.diff(a)); sigma = mr.mean() / 1.128
            lo, hi = a.mean() - 3*sigma, a.mean() + 3*sigma
            checks[name] = {'n':len(a),'mean':float(a.mean()),'sd':float(a.std(ddof=1)),
                            'imr_point_flags':int(((a<lo)|(a>hi)).sum()),
                            'imr_moving_range_flags':int((mr > 3.267*mr.mean()).sum()),
                            'imr_limits':[float(lo),float(hi)],
                            'method_note':'I-MR, MR(2), d2=1.128, D4=3.267; only point-beyond-limit rules'}
            if 'mu' in b:
                tt = stats.ttest_1samp(a,b['mu'],alternative='greater')
                checks[name].update(target=b['mu'], greater_t_p=float(tt.pvalue),
                                    lower_one_sided_95=float(a.mean()-stats.t.ppf(.95,len(a)-1)*stats.sem(a)),
                                    below_target_count=int((a<b['mu']).sum()))
        if 'defectCounts' in b and 'subgroupSizes' in b:
            k=np.array(b['defectCounts']);n=np.array(b['subgroupSizes']);pb=k.sum()/n.sum()
            hw=3*np.sqrt(pb*(1-pb)/n); lo=np.maximum(0,pb-hw);hi=np.minimum(1,pb+hw)
            target=b.get('required_share')
            q={'events':int(k.sum()),'n':int(n.sum()),'share':float(pb),
               'p_chart_point_flags':int(((k/n<lo)|(k/n>hi)).sum())}
            if target:
                q.update(target=target, exact_lower_tail_p=float(stats.binomtest(int(k.sum()),int(n.sum()),target,alternative='less').pvalue),
                         exact_upper_tail_p=float(stats.binomtest(int(k.sum()),int(n.sum()),target,alternative='greater').pvalue),
                         upper_one_sided_95=float(stats.beta.ppf(.95,k.sum()+1,n.sum()-k.sum())))
            checks[name]=q
        if 'groups' in b and isinstance(b['groups'],dict):
            g=list(b['groups'].values());welch=anova_oneway(g,use_var='unequal')
            checks[name]={'group_n':list(map(len,g)),
                          'group_means':[float(np.mean(x)) for x in g],
                          'group_variances':[float(np.var(x,ddof=1)) for x in g],
                          'levene_median_p':float(stats.levene(*g,center='median').pvalue),
                          'pooled_anova_p':float(stats.f_oneway(*g).pvalue),
                          'welch_anova_p':float(welch.pvalue),'welch_anova_F':float(welch.statistic),
                          'welch_df':list(map(float,welch.df)),
                          'kruskal_p':float(stats.kruskal(*g).pvalue)}
        if 'x' in b and 'y' in b:
            fit=sm.OLS(b['y'],sm.add_constant(b['x'])).fit()
            checks[name]={'n':len(b['y']),'ols_model_p':float(fit.f_pvalue),
                          'ols_r2':float(fit.rsquared),'coefficients':fit.params.tolist()}
        if 'runs' in b and 'columns' in b and 'y' in b['columns'] and name in ['screening_run','design']:
            names=[n for n in b['columns'] if n!='y']
            rows=b['runs']; base=np.array([[r[n] for n in names] for r in rows]); cols=[np.ones(len(rows))]
            terms=['intercept']
            for degree in range(1,len(names)+1):
                for inds in combinations(range(len(names)),degree):
                    cols.append(base[:,inds].prod(axis=1));terms.append('*'.join(names[i] for i in inds))
            fit=sm.OLS([r['y'] for r in rows],np.array(cols).T).fit()
            checks[name]={'n':len(rows),'full_factorial_model_p':float(fit.f_pvalue),
                          'r_squared':float(fit.rsquared),'terms':terms,
                          'term_p_values':fit.pvalues.tolist(),
                          'method_note':'Full factorial including all interactions; not causal without randomization assumptions'}
        if name=='logged_variables' and isinstance(d,dict) and 'y' in d:
            keys=[k for k in d if k!='y'];fit=sm.OLS(d['y'],sm.add_constant(np.array([d[k] for k in keys]).T)).fit()
            checks[name]={'main_effect_model_p':float(fit.f_pvalue),'r_squared':float(fit.rsquared),'n':len(d['y'])}
    if 'recipes' in data and 'leading_two' in data:
        g=data['recipes']['groups'];b=data['leading_two']
        checks['leading_two_reuses_recipe_rows']=[any(b[k]==v for v in g.values()) for k in ['group1','group2']]
    if p.name=='B021':
        trace=json.loads((p/'trace.json').read_text())
        pred=next(x['outputs'] for x in trace['steps'] if x.get('step_id')==26)
        confirm=np.array(data['confirmation_runs']['data'])
        lo,hi=pred['piLower'],pred['piUpper']
        checks['reported_prediction_interval_check']={
            'interval':[lo,hi], 'observed_mean':float(confirm.mean()),
            'mean_inside_interval':bool(lo<=confirm.mean()<=hi),
            'observations_outside_interval':int(((confirm<lo)|(confirm>hi)).sum()),
            'note':'This direct arithmetic check does not endorse using a single-observation PI to assess a sample mean.'}
    out[p.name]=checks

(ROOT/'coordinator/numerical_checks.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
for k in ['B001','B002','B007','B009','B011','B018','B020','B021','B022','B028']:
    print(k,json.dumps(out[k],ensure_ascii=False))
