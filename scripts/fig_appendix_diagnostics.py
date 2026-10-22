#!/usr/bin/env python3
"""CHI-Bench-inspired appendix diagnostics from retained DMAIC-Bench records.
Run from repository root in the pinned analysis environment with matplotlib installed.
Does not rescore, modify campaign records, or run new trials.
"""
import sys, json, csv, hashlib
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
from matplotlib.backends.backend_pdf import PdfPages
sys.path[:0] = ['.', 'harbor/src', 'scripts']
import restraint_analysis as RA
from dmaic_harbor import campaign_report as CR

OUT = Path('paper/iclr/figures'); DATA = Path('output/research/appendix_diagnostics')
OUT.mkdir(parents=True, exist_ok=True); DATA.mkdir(parents=True, exist_ok=True)


def require_input(path, producer):
    """Exit with a plain message when a run-artifact input is absent from the checkout."""
    if not Path(path).exists():
        sys.exit(f"missing input {path}: this file is not part of the tracked tree. It comes from "
                 f"the run-artifact archive ({producer}); see scripts/README.md, Analysis inputs.")
TIERS = ['A-proceed', 'B-divert', 'C-stop']
SHOW = {'A-proceed':'A-go', 'B-divert':'B-divert', 'C-stop':'C-stop'}
# Figure 6 uses a stable model palette; Figure 14 uses categorical solid colors.
MODEL_COLORS = {
 'GPT-6-astra':'#6798B9', 'GPT-5.6-sol':'#76B1B0', 'Kimi-k3':'#A699BC',
 'Claude-Sonnet-5':'#C98E7A', 'DeepSeek-v4-flash':'#84AFA0',
 'DeepSeek-v4-pro':'#A88F82', 'GLM-5.3':'#B98098',
 'GPT-5.6-luna':'#8CA4CA', 'Claude-Fable-5.1':'#B5A8CF',
 'GLM-5.3-Flash':'#909DA7', 'Claude-Opus-5':'#D3A69B',
 'Qwen3.8-max':'#93AD87', 'Qwen3.8-flash':'#B4BDA7',
}
# Reuse the paper's blue/red anchors and muted categorical hues from Figure 6.
COLORS = {'Correct':'#3182BD', 'E1':'#A50F15', 'E2':'#B8BDC4',
          'E3':'#A699BC', 'E4':'#76B1B0', 'E5':'#C98E7A'}
from figure_palette import heatmap_cmap
SUCCESS_SCALE = [heatmap_cmap()(v) for v in [0., 1/3, 2/3, 1.]]
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','DejaVu Sans'],
 'font.size':8,'text.color':'#303634','axes.labelcolor':'#303634','axes.labelsize':8,'xtick.labelsize':7,'ytick.labelsize':7,
 'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none','axes.spines.top':False,
 'axes.spines.right':False,'savefig.facecolor':'white'})
FIGS=[]
def save(fig, name):
    for ext in ['pdf','svg','png']:
        fig.savefig(OUT/f'{name}.{ext}', dpi=300)
    FIGS.append((name,fig))

def duration(x):
    if not x or not x.get('started_at') or not x.get('finished_at'): return None
    return (datetime.fromisoformat(x['finished_at'].replace('Z','+00:00'))-datetime.fromisoformat(x['started_at'].replace('Z','+00:00'))).total_seconds()

def collect():
    cases=RA.V.discover(); shapes=CR._shape_lookup()
    rank=json.loads(Path('docs/result_restraint.json').read_text())
    systems=[]; resources=[]; events=[]; cells=[]; paths={}
    for name,vendor,k1,k3 in RA.SYSTEMS:
        first=RA.load_rows(k1)
        assert len(first)==97,(name,len(first))
        ids={r['task_id'] for r in first}
        allrows=[]
        for job in k1+k3:
            p=RA.JOBS/job
            if p.exists():
                for r in CR._rows(p):
                    if r['agent'] not in ('oracle','nop'):
                        r['job_dir']=p;allrows.append(r)
        by=defaultdict(list)
        for r in allrows: by[r['task_id']].append(r)
        # Same job order and within-job ordering as campaign_report.passk. A system is read at
        # the depth every one of its tasks actually reaches: falling back to 1 whenever a single
        # task is short throws away real attempts and labels the row (1) while two are in hand.
        k=min(len(v) for v in by.values()) if set(by)==ids else 1
        k=max(1, min(3, k))
        selected={tid:by[tid][:k] for tid in ids} if k>1 else {r['task_id']:[r] for r in first}
        systems.append({'name':name,'vendor':vendor,'k':k,'reward':rank[name]['mean']})
        for r in first:
            tid=r['task_id']; tier=CR._tier(r,shapes)
            paths[str(r['job_dir']/r['trial']/'verifier-rescored/scorecard.json')]=True
            cell={'system':name,'task':tid,'case':r['case_id'],'seed':r['seed'],'tier':tier,'k':k,
                  'successes':sum(CR._all_decisions_right(a) for a in selected[tid])}
            cell['pass1']=cell['successes']/k; cells.append(cell)
            for a in selected[tid]: paths[str(a['job_dir']/a['trial']/'verifier-rescored/scorecard.json')]=True
            rp=r['job_dir']/r['trial']/'result.json'
            result=json.loads(rp.read_text()) if rp.exists() else {}; paths[str(rp)]=True
            ar=result.get('agent_result') or {}; ni=ar.get('n_input_tokens'); no=ar.get('n_output_tokens')
            resources.append({'system':name,'task':tid,'tier':tier,'case':r['case_id'],
                'seconds':duration(result.get('agent_execution')),
                'tokens':ni+no if ni is not None and no is not None else None,
                'input_tokens':ni,'output_tokens':no,'cache_tokens':ar.get('n_cache_tokens'),
                'source':str(rp)})
        for r,p,v,_o,_s,_d in RA.decisions(first,cases):
            kind='NO-GO' if RA.is_stop(p) else 'GO'
            det=next(d for d in r['card']['scorecard']['pq']['details'] if d.get('kind')=='decision_point' and d.get('point_id')==p['point_id'])
            via=det.get('via')
            if v=='correct': mode='Correct'
            elif via=='abstained_from_required_branch': mode='E5'
            elif v=='unknown' or via in (None,'none'): mode='E2' if kind=='NO-GO' else 'E4'
            elif via in {'evidence','divergent_evidence','explicit','explicit_contradicted','declared_unsupported'}: mode='E1' if kind=='NO-GO' else 'E3'
            else: raise ValueError((v,via))
            events.append({'system':name,'task':r['task_id'],'point':p['point_id'],'phase':p['point_id'][0], 'kind':kind,'mode':mode})
    systems.sort(key=lambda s:-s['reward'])
    assert len(events)==3900
    assert Counter(c['tier'] for c in cells)=={t:n*13 for t,n in zip(TIERS,[48,18,31])}
    for name,rows in [('resources',resources),('task_success',cells),('decision_outcomes',events)]:
        with (DATA/f'{name}.csv').open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    hashes={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in sorted(paths) if Path(p).exists()}
    (DATA/'sources_sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    (DATA/'systems.json').write_text(json.dumps(systems,indent=2)+'\n')
    return systems,resources,cells,events

def resources_plot(systems,rows):
    names=[s['name'] for s in systems]
    fig,axs=plt.subplots(3,2,figsize=(6.3,8.0),sharey=True)
    fig.subplots_adjust(left=.235,right=.98,top=.907,bottom=.065,hspace=.30,wspace=.13)
    fig.text(.235,.972,'Resource use on the scored first attempt',size=11,weight='bold')
    fig.text(.235,.948,'Color: model (fixed across panels); dot: median; line: IQR',size=7,color='#555555')
    summaries=[]
    for i,tier in enumerate(TIERS):
        for j,(key,scale,xlabel) in enumerate([('seconds',60,'Agent execution (min)'),('tokens',1000000,'Input + output tokens (millions)')]):
            ax=axs[i,j]
            for y,name in enumerate(names):
                vals=np.array([r[key]/scale for r in rows if r['system']==name and r['tier']==tier and r[key] is not None])
                total=sum(r['system']==name and r['tier']==tier for r in rows)
                summaries.append({'system':name,'tier':tier,'metric':key,'observed':len(vals),'total':total,
                                  'median':float(np.median(vals)*scale) if len(vals) else None})
                if len(vals)>1 and np.ptp(vals)>0:
                    body=ax.violinplot([vals],positions=[y],orientation="horizontal",widths=.77,showextrema=False)['bodies'][0]
                    body.set_facecolor(MODEL_COLORS[name]);body.set_edgecolor('#858C89');body.set_linewidth(.4);body.set_alpha(1.0)
                if len(vals):
                    q=np.percentile(vals,[25,50,75]);ax.plot(q[[0,2]],[y,y],color='#3E4543',lw=1.2);ax.plot(q[1],y,'o',ms=2,color='#3E4543')
                if len(vals)!=total:ax.text(.99,y,f'{len(vals)}/{total}',transform=ax.get_yaxis_transform(),ha='right',fontsize=5.8)
            ax.set_title(f'{chr(97+i*2+j)}  {SHOW[tier]}  (n = {[48,18,31][i]} tasks)',loc='left',fontsize=8.5,weight='bold')
            ax.set_yticks(range(len(names)),names);ax.set_ylim(12.65,-.65);ax.set_xlim(left=0)
            for label, name in zip(ax.get_yticklabels(), names):
                label.set_color(MODEL_COLORS[name])
            ax.set_xlabel(xlabel);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
            ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0)
    save(fig,'figure06_resource_distributions')
    return summaries

def heatmaps(systems,cells):
    names=[s['name'] for s in systems]; ns={s['name']:s['k'] for s in systems}
    lookup={(c['system'],c['task']):c for c in cells}
    cm=ListedColormap(SUCCESS_SCALE);norm=BoundaryNorm([-1/6,1/6,.5,5/6,7/6],4)
    summary={}
    for tier in TIERS:
        tasks=sorted([c for c in cells if c['system']==names[0] and c['tier']==tier],key=lambda c:(c['case'],c['seed']))
        a=np.array([[lookup[n,c['task']]['pass1'] for c in tasks] for n in names])
        # The 48-column A-go panel accompanies the methods paragraph; the two
        # remaining tiers use compact panels so they fit together at full width.
        compact = SHOW[tier] != 'A-go'
        fig=plt.figure(figsize=(6.3,3.2 if compact else 4.6))
        ax=fig.add_axes([.235,.29,.66,.54] if compact else [.235,.28,.66,.57])
        cbax=fig.add_axes([.235,.10,.37,.025] if compact else [.235,.095,.37,.024])
        fig.text(.235,.96,f'{SHOW[tier]}: task-level route success',size=10 if compact else 11,weight='bold')
        fig.text(.235,.903 if compact else .917,f'{len(tasks)} tasks | rows follow overall reward order | k = attempts per task',size=7,color='#555555')
        im=ax.pcolormesh(np.arange(a.shape[1]+1)-.5,np.arange(a.shape[0]+1)-.5,a,cmap=cm,norm=norm,rasterized=False)
        ax.set_xlim(-.5,a.shape[1]-.5);ax.set_ylim(12.5,-.5)
        ax.set_yticks(range(13),[f"{n}  ({ns[n]})" for n in names]);ax.tick_params(length=0)
        ax.set_xticks(range(len(tasks)),[f"{c['case'].split('c')[-1]}.{c['seed']}" + ('*' if (c['case'],c['seed']) in RA.UNLOCKED else '') for c in tasks],rotation=90,fontsize=7)
        ax.set_xlabel('Task: case.seed',labelpad=3 if compact else 7)
        for x in range(1,len(tasks)):
            if tasks[x]['case']!=tasks[x-1]['case']:ax.axvline(x-.5,color='white',lw=1)
        ax.text(1.025,1.025,'Mean',transform=ax.transAxes,fontsize=7)
        for y,v in enumerate(a.mean(axis=1)):
            ax.text(1.025,y,f'{100*v:.1f}%',transform=ax.get_yaxis_transform(),va='center',fontsize=7)
        for x in np.where(a.sum(axis=0)==0)[0]:ax.text(x,-.82,'×',ha='center',va='center',fontsize=8,clip_on=False)
        cb=fig.colorbar(im,cax=cbax,orientation='horizontal',ticks=[0,1/3,2/3,1]);cb.ax.set_xticklabels(['0','1/3','2/3','1']);cb.outline.set_visible(False)
        fig.text(.235,.012 if compact else .028,'Empirical pass@1 (all route decisions correct)',fontsize=7)
        fig.text(.655,.095,'×  No observed success\n*  Deliberately unlocked task',fontsize=6.5,va='center')
        save(fig, {'A-proceed':'figure11_heatmap_go', 'B-divert':'figure12_heatmap_divert', 'C-stop':'figure13_heatmap_stop'}[tier])
        summary[SHOW[tier]]={'tasks':len(tasks),'zero_success_tasks':int(sum(a.sum(axis=0)==0)),
          'means':dict(zip(names,a.mean(axis=1).tolist()))}
    return summary

def outcomes(systems,events, verify=True):
    names=[s['name'] for s in systems]
    fig,axs=plt.subplots(2,3,figsize=(6.3,6.55),sharey=True)
    fig.subplots_adjust(left=.235,right=.973,top=.875,bottom=.15,wspace=.13,hspace=.29)
    fig.text(.235,.962,'Decision outcomes at prerequisite-bearing phases',size=10,weight='bold')
    fig.text(.235,.931,'First attempt | each bar = 100% of reference-route decisions in that panel',size=7,color='#555555')
    summary=[]
    for i,kind in enumerate(['NO-GO','GO']):
        cats=['Correct','E1','E2','E5'] if kind=='NO-GO' else ['Correct','E3','E4','E5']
        for j,(ph,phase) in enumerate([('M','Measure'),('A','Analyze'),('I','Improve')]):
            ax=axs[i,j];counts=[]
            for y,name in enumerate(names):
                c=Counter(e['mode'] for e in events if e['system']==name and e['phase']==ph and e['kind']==kind);n=sum(c.values());counts.append(n)
                left=0
                for cat in cats:
                    width=100*c[cat]/n if n else 0
                    ax.barh(y,width,left=left,height=.73,color=COLORS[cat],edgecolor='white',linewidth=.25);left+=width
                if not n:ax.text(50,y,'No decisions',ha='center',va='center',fontsize=6)
                summary.append({'system':name,'phase':ph,'kind':kind,'n':n,'counts':dict(c)})
                if n:assert abs(left-100)<1e-8
            assert len(set(counts))==1
            ax.set_title(f'{chr(97+i*3+j)}  {phase}\n{kind}  |  n = {counts[0]}',loc='left',fontsize=8,weight='bold')
            ax.set_yticks(range(13),names);ax.set_ylim(12.65,-.65);ax.set_xlim(0,100)
            ax.set_xticks([0,50,100],['0','50','100%']);ax.tick_params(axis='y',length=0)
            ax.get_xticklabels()[-1].set_ha('right')
            ax.spines['left'].set_visible(False)
    labels={'Correct':'Correct route','E1':'E1: forbidden no-go work','E2':'E2: no-go fork unreached','E3':'E3: wrong go branch','E4':'E4: go fork unreached','E5':'E5: premature stop'}
    handles=[Patch(facecolor=COLORS[k],label=labels[k],edgecolor='white') for k in COLORS]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.60,.015),ncol=2,frameon=False,fontsize=7,columnspacing=1)
    save(fig,'figure14_decision_outcomes')
    # Reconcile all phases against the existing Table 3 analysis.
    import fig_breakdown as FB
    for s in FB.collect() if verify else []:
        got=Counter(e['mode'] for e in events if e['system']==s['name'] and e['mode']!='Correct')
        assert got==s['err'],(s['name'],got,s['err'])
    return summary

if __name__=='__main__':
    redraw = '--redraw' in sys.argv
    if redraw:
        for _name in ['systems.json','resources.csv','task_success.csv','decision_outcomes.csv']:
            require_input(DATA/_name, 'written by scripts/fig_appendix_diagnostics.py without --redraw from the retained harbor/jobs trials')
        systems=json.loads((DATA/'systems.json').read_text())
        def read_rows(name):
            with (DATA/f'{name}.csv').open() as f: return list(csv.DictReader(f))
        resources=read_rows('resources');cells=read_rows('task_success');events=read_rows('decision_outcomes')
        for r in resources:
            for key in ['seconds','tokens','input_tokens','output_tokens','cache_tokens']:
                r[key]=float(r[key]) if r[key] else None
        for c in cells:
            for key in ['seed','k','successes']: c[key]=int(c[key])
            c['pass1']=float(c['pass1'])
    else:
        require_input(RA.JOBS, 'the retained harbor/jobs trial directories, shipped as the results archive')
        systems,resources,cells,events=collect()
    summary={'resource_coverage':resources_plot(systems,resources),'heatmaps':heatmaps(systems,cells),'outcomes':outcomes(systems,events, verify=not redraw),
        'total_first_attempt_trials':len(resources),'total_decisions':len(events),
        'attempts_by_system':{s['name']:s['k'] for s in systems}}
    (DATA/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    with PdfPages('output/pdf/dmaic_appendix_diagnostics.pdf') as pdf:
        for _,fig in FIGS:pdf.savefig(fig)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['resource_coverage','outcomes']},indent=2))
