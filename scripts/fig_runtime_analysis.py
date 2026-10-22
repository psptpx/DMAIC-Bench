#!/usr/bin/env python3
"""Descriptive runtime analysis of the exact scored first attempts used in Figure 6.

Reconciles cached telemetry with raw result timestamps and rescored route verdicts.
Does not rerun agents or infer unobserved retry costs.
"""
import csv, json, re, hashlib
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import FixedLocator, FuncFormatter
from figure_palette import heatmap_cmap, HEAT_BLUE, HEAT_RED

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'output/research/appendix_diagnostics'
OUT=ROOT/'paper/iclr/figures'


def require_input(path, producer):
    """Exit with a plain message when a run-artifact input is absent from the checkout."""
    if not Path(path).exists():
        sys.exit(f"missing input {path}: this file is not part of the tracked tree. It comes from "
                 f"the run-artifact archive ({producer}); see scripts/README.md, Analysis inputs.")

for _name in ['systems.json','resources.csv','decision_outcomes.csv']:
    require_input(DATA/_name, 'written by scripts/fig_appendix_diagnostics.py from the retained harbor/jobs trials')
require_input(ROOT/'harbor/jobs', 'the retained harbor/jobs trial directories, shipped as the results archive')
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','DejaVu Sans'],
 'font.size':8,'axes.labelsize':8,'xtick.labelsize':7,'ytick.labelsize':7,
 'text.color':'#303634','axes.labelcolor':'#303634','pdf.fonttype':42,
 'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,
 'savefig.facecolor':'white'})

def read_csv(name):
    with (DATA/name).open() as f:return list(csv.DictReader(f))

def export(fig,name):
    for ext in ['svg','pdf','png']:fig.savefig(OUT/f'{name}.{ext}',dpi=250)
    plt.close(fig)

names=[s['name'] for s in json.loads((DATA/'systems.json').read_text())]
rows=read_csv('resources.csv'); events=read_csv('decision_outcomes.csv')
event_map=defaultdict(list)
for e in events:event_map[e['system'],e['task']].append(e)
assert len(rows)==13*97 and len({(r['system'],r['task']) for r in rows})==len(rows)
for r in rows:
    path=ROOT/r['source']; raw=json.loads(path.read_text())
    card=json.loads((path.parent/'verifier-rescored/scorecard.json').read_text())
    times=raw['agent_execution'];elapsed=(datetime.fromisoformat(times['finished_at'].replace('Z','+00:00'))-datetime.fromisoformat(times['started_at'].replace('Z','+00:00'))).total_seconds()
    assert abs(elapsed-float(r['seconds']))<1e-5 and elapsed>0
    assert card['task_id']==r['task']
    r['seconds']=elapsed;r['minutes']=elapsed/60;r['tokens']=float(r['tokens'])
    ar=raw['agent_result'];assert r['tokens']==ar['n_input_tokens']+ar['n_output_tokens']
    r['timeout']=(raw.get('exception_info') or {}).get('exception_type')=='AgentTimeoutError'
    r['seed']=int(re.search(r'-s(\d+)-',r['task'])[1])
    r['correct']=card['scorecard']['pq']['score']==1
    es=event_map[r['system'],r['task']]
    r['e1']=any(e['mode']=='E1' for e in es)
    assert not(r['correct'] and r['e1'])
    r['group']='correct' if r['correct'] else 'e1' if r['e1'] else 'other'
assert all(1 <= r['minutes'] <= 180 for r in rows), 'Heatmap range would clip data'
lookup={(r['system'],r['task']):r for r in rows}
with (DATA/'runtime_run_metrics.csv').open('w') as f:
    fields=['system','task','case','tier','minutes','tokens','group','timeout']
    writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
summary=[]
for name in names:
    rr=[r for r in rows if r['system']==name];a=np.array([r['minutes'] for r in rr]);q=np.percentile(a,[25,50,75,90])
    summary.append(dict(system=name,n=len(a),q25=q[0],median=q[1],q75=q[2],p90=q[3],hours=a.sum()/60,timeouts=sum(r['timeout'] for r in rr)))

# Absolute model-by-task runtime heatmap. Shared log scale across all tiers.
fig,axs=plt.subplots(3,1,figsize=(6.3,7.6))
fig.subplots_adjust(left=.235,right=.97,top=.905,bottom=.115,hspace=.49)
fig.text(.235,.977,'Execution time by model and task',fontsize=11,weight='bold')
fig.text(.235,.951,'Scored first attempt | shared logarithmic color scale',fontsize=7,color='#555555')
for i,(tier,label) in enumerate([('A-proceed','A-go'),('B-divert','B-divert'),('C-stop','C-stop')]):
    ts=sorted([r for r in rows if r['system']==names[0] and r['tier']==tier],key=lambda r:(r['case'],r['seed']))
    a=np.array([[lookup[n,t['task']]['minutes'] for t in ts] for n in names]);ax=axs[i]
    im=ax.pcolormesh(np.arange(len(ts)+1)-.5,np.arange(14)-.5,a,cmap=heatmap_cmap(),norm=LogNorm(1,180),rasterized=False)
    ax.set(xlim=(-.5,len(ts)-.5),ylim=(12.5,-.5));ax.set_yticks(range(13),names)
    ax.set_xticks(range(len(ts)),[f"{t['case'].split('c')[-1]}.{t['seed']}" for t in ts],rotation=90,fontsize=7)
    ax.tick_params(length=0);ax.set_title(f'{chr(97+i)}  {label}  |  {len(ts)} tasks',loc='left',fontsize=8.5,weight='bold')
    for j in range(1,len(ts)):
        if ts[j]['case']!=ts[j-1]['case']:ax.axvline(j-.5,color='white',lw=.8)
    for y,n in enumerate(names):
        for x,t in enumerate(ts):
            if lookup[n,t['task']]['timeout']:ax.text(x,y,'×',ha='center',va='center',color='black',fontsize=8,weight='bold')
    ax.set_xlabel('Task: case.seed',labelpad=2)
cax=fig.add_axes([.235,.048,.49,.013]);cb=fig.colorbar(im,cax=cax,orientation='horizontal',ticks=[1,3,10,30,90,180]);cb.ax.set_xticklabels(['1','3','10','30','90','180']);cb.ax.minorticks_off();cb.outline.set_visible(False);cb.solids.set_rasterized(False)
fig.text(.235,.009,'Agent execution (min)',fontsize=7)
fig.text(.76,.042,'×  Timeout',fontsize=7)
export(fig,'figure07_runtime_by_task')

# Descriptive C-stop groups; explicitly expose the different sample counts.
stop=[r for r in rows if r['tier']=='C-stop'];counts=Counter(r['group'] for r in stop)
fig,axs=plt.subplots(1,2,figsize=(6.3,4.6))
fig.subplots_adjust(left=.235,right=.975,top=.85,bottom=.20,wspace=.20)
fig.text(.235,.975,'Resource use on tasks requiring a terminal stop',fontsize=10,weight='bold')
fig.text(.235,.942,'C-stop | first attempt | dot: median; line: IQR',fontsize=7,color='#555555')
fig.text(.235,.912,'Row counts: correct / E1; groups contain different tasks',fontsize=7,color='#555555')
for j,(field,scale,label) in enumerate([('minutes',1,'Agent execution (min)'),('tokens',1e6,'Input + output tokens (millions)')]):
    ax=axs[j]
    for y,n in enumerate(names):
        for group,col,offset in [('correct',HEAT_BLUE,-.14),('e1',HEAT_RED,.14)]:
            a=np.array([r[field]/scale for r in stop if r['system']==n and r['group']==group]);q=np.percentile(a,[25,50,75])
            ax.plot(q[[0,2]],[y+offset]*2,color=col,lw=1.6);ax.plot(q[1],y+offset,'o',color=col,ms=3)
    ax.set_xscale('log');ax.set_ylim(12.65,-.65);ax.set_xlabel(label);ax.grid(axis='x',alpha=.14);ax.set_axisbelow(True);ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0)
    ticks=[1,3,10,30,100] if j==0 else [.01,.03,.1,.3,1,3,10]
    ax.xaxis.set_major_locator(FixedLocator(ticks));ax.xaxis.set_major_formatter(FuncFormatter(lambda x,_:f'{x:g}'));ax.minorticks_off()
    ax.set_xlim((1,150) if j==0 else (.02,15))
    if j==0:
        ax.set_yticks(range(13),[f"{n}  ({sum(r['system']==n and r['group']=='correct' for r in stop)}/{sum(r['system']==n and r['group']=='e1' for r in stop)})" for n in names],fontsize=7)
    else:ax.set_yticks([])
    ax.set_title('a  Execution time' if j==0 else 'b  Token use',loc='left',weight='bold',fontsize=8.5)
from matplotlib.lines import Line2D
fig.legend(handles=[Line2D([0],[0],color=HEAT_BLUE,marker='o',ms=3,label='All route decisions correct'),Line2D([0],[0],color=HEAT_RED,marker='o',ms=3,label='Forbidden no-go work (E1)')],loc='lower center',bbox_to_anchor=(.59,.045),frameon=False,ncol=1,fontsize=7)
export(fig,'figure08_stop_task_resources')

# Same model and case: compare geometric means across seeds, not causal effects.
pairs=[]
for name in names:
    for case in sorted({r['case'] for r in stop}):
        groups={g:[r for r in stop if r['system']==name and r['case']==case and r['group']==g] for g in ['correct','e1']}
        if not all(groups.values()):continue
        item={'system':name,'case':case,'n_correct':len(groups['correct']),'n_e1':len(groups['e1'])}
        for field in ['minutes','tokens']:
            item[field+'_ratio']=float(np.exp(np.mean(np.log([r[field] for r in groups['e1']]))-np.mean(np.log([r[field] for r in groups['correct']]))))
        pairs.append(item)
paired={field:float(np.exp(np.mean(np.log([p[field+'_ratio'] for p in pairs])))) for field in ['minutes','tokens']}
faster=sum(np.median([r['minutes'] for r in stop if r['system']==n and r['group']=='correct'])<np.median([r['minutes'] for r in stop if r['system']==n and r['group']=='e1']) for n in names)
report={'n':len(rows),'n_tasks':97,'n_models':13,'summary':summary,'c_stop_counts':dict(counts),'correct_faster_models':int(faster),'within_model_case_groups':len(pairs),'within_model_case_cases':len({p['case'] for p in pairs}),'within_model_case_models':len({p['system'] for p in pairs}),'matched_geomean_ratios':paired,'pairs':pairs,'timeouts':[{k:r[k] for k in ['system','task','minutes','tier']} for r in rows if r['timeout']],'source_sha256':{n:hashlib.sha256((DATA/n).read_bytes()).hexdigest() for n in ['resources.csv','decision_outcomes.csv','systems.json']}}
(DATA/'runtime_analysis.json').write_text(json.dumps(report,indent=2)+'\n')
with (DATA/'runtime_summary.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
lines=[r'\begin{tabular}{@{}lrrrrr@{}}',r'\toprule',r'Agent & Median & IQR & P90 & Total (h) & TO \\',r'\midrule']
for s in summary:lines.append(f"{s['system']} & {s['median']:.1f} & {s['q25']:.1f}--{s['q75']:.1f} & {s['p90']:.1f} & {s['hours']:.1f} & {s['timeouts']} \\\\")
lines += [r'\bottomrule',r'\end{tabular}']
(ROOT/'paper/iclr/tab_runtime_summary.tex').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['summary','pairs','source_sha256']},indent=2))
