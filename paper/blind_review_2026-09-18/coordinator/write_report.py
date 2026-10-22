"""Render the English human expert synthesis; independent votes remain unchanged."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'results.json').read_text())
s = data['summary']['all']
core = data['summary']['core']
boundary = data['summary']['boundary']
units = {u['blind_id']: u for u in data['units']}


def link(label, path):
    return f'[{label}]({ROOT / path})'


def pct(n, d):
    return f'{n}/{d} ({n/d:.1%})'


def vote(ident, field):
    return ' / '.join(units[ident][field])


def ids(values):
    return ', '.join(values) if values else 'None'


table = [
    '**Original human expert judgments and unblinded comparisons for 30 items**\n',
    'Votes are listed in the fixed order R1/R2/R3, the three human expert reviewers. '
    'ACCEPTABLE means the focal conduct is acceptable, not that every number and inference '
    'in the entire report is correct. STOP/GO judgments for different checkpoints or claims '
    'are not interchangeable.\n',
    '| ID | Case / seed / checkpoint | Original label / score | Three gate votes | Three conduct votes | Majority conduct |',
    '|---|---|---|---|---|---|',
]
for u in data['units']:
    i = u['blind_id']
    table.append(
        f'| {link(i, "blind/cases/" + i + "/packet.md")} | {u["case"]} / {u["seed"]} / {u["point"]} '
        f'| {u["benchmark_label"]} / {u["benchmark_verdict"]} | {" / ".join(u["gate_votes"])} '
        f'| {" / ".join(u["trajectory_votes"])} | {u["majority_trajectory"]} |'
    )
(ROOT / 'ITEM_TABLE.md').write_text('\n'.join(table) + '\n')

report = f'''**DMAIC-Bench: independent blind review by three human Black Belt experts, 2026-09-18**

This review supports retaining stop rules tied to specific conclusions and actions. It also finds that scoring based on method names and a single reference route can classify limited exploration, defensible alternatives, or calculations from an earlier stage as improper advancement. Performing an analysis does not by itself establish that an unsupported conclusion was drawn from it.

This review was conducted independently by **three human experts** using Black Belt methods. The figures below describe this sample and cannot be extrapolated to whole-benchmark label accuracy or revised model error rates.

**Review design and scope**

- Three perspectives: R1, measurement systems and SPC; R2, industrial statistics, DOE, and causal inference; R3, factory quality, implementation, and closure. Each human expert reviewed all 30 items using the same rubric in a different randomized order. Submissions were independently frozen, with no later consensus round changing the original votes.
- The 30 distinct trajectories cover all 15 cases, 11 completed main-experiment systems, and one permission-control trajectory. They represent 26 case/seed instances and 24/66 distinct decision points: 20 Measure, 7 Analyze, and 3 Improve.
- The 24-item core contains one randomly sampled existing STOP per case plus nine GO items sampled by phase. Six diagnostic boundary items were selected by the coordinator after the prior audit and before review. The random seed is 20260918. Runs that did not reach the checkpoint or lacked reports/traces were excluded. Not every failure mechanism is covered; in particular, no failed I_confirm branch was sampled.
- Model, task, and case identifiers, original scores, reference routes, and sample strata were masked. Complete reports, quantitative traces, original task requirements, public gates, released batches, and service logs were retained. All three human experts received only the blind materials, without prior paper reviews, and declared compliance. On a shared filesystem, blinding is procedural rather than enforced through technical access controls.
- Inputs were frozen before dispatch and checked with SHA-256. This English edition records updated hashes separately from the original dispatch hashes. Language and reviewer attribution were revised while the source evidence, votes, and numerical results were preserved. Concurrent repository changes were outside the review of saved run artifacts. Shared materials and a common rubric may lead to correlated reviewer judgments; agreement alone does not establish validity for every benchmark branch.

**Results**

| Metric | All 30 items | 24 core items | 6 boundary items |
|---|---:|---:|---:|
| Unanimous gate votes | {pct(s['gate_agreement']['unanimous_n'], 30)} | {pct(core['gate_agreement']['unanimous_n'], 24)} | {pct(boundary['gate_agreement']['unanimous_n'], 6)} |
| Gate Fleiss kappa | {s['gate_agreement']['fleiss_kappa']:.3f} | {core['gate_agreement']['fleiss_kappa']:.3f} | {boundary['gate_agreement']['fleiss_kappa']:.3f} |
| Unanimous focal-conduct judgments | {pct(s['trajectory_agreement']['unanimous_n'], 30)} | {pct(core['trajectory_agreement']['unanimous_n'], 24)} | {pct(boundary['trajectory_agreement']['unanimous_n'], 6)} |
| Conduct Fleiss kappa | {s['trajectory_agreement']['fleiss_kappa']:.3f} | {core['trajectory_agreement']['fleiss_kappa']:.3f} | {boundary['trajectory_agreement']['fleiss_kappa']:.3f} |
| Majority gate matches original STOP/GO label | {pct(s['majority_matches_benchmark'], 30)} | {pct(core['majority_matches_benchmark'], 24)} | {pct(boundary['majority_matches_benchmark'], 6)} |

Of 18 existing STOP labels, {s['benchmark_stop']['majority_support']} received a majority STOP vote; of 12 existing GO labels, {s['benchmark_go']['majority_support']} received a majority GO vote. Majority conduct judgments are 18 ACCEPTABLE, 11 MIXED, and 1 UNACCEPTABLE. The predefined rule, originally scored incorrect but focal conduct rated ACCEPTABLE by at least two reviewers, identifies **{len(s['candidate_scoring_overpenalty'])} candidate over-penalties**: {ids(s['candidate_scoring_overpenalty'])}. Of these, {len(core['candidate_scoring_overpenalty'])} are core items and {len(boundary['candidate_scoring_overpenalty'])} are boundary items; five are unanimous and B008 has a 2-1 majority. These are scoring risks requiring item-level review, not automatic gold-label or model-score changes, and do not establish that entire reports are error-free.

All three human experts' votes and evidence are preserved in {link('ITEM_TABLE.md', 'ITEM_TABLE.md')}, {link('results.json', 'results.json')}, and the {link('CSV', 'item_results.csv')}. Kappa uses nominal categories, with missing/undetermined outcomes and no-majority cases retained explicitly. The 90 votes are not treated as 90 independent experiments, and no spuriously precise confidence intervals are constructed.

**Cases with the strongest implications**

1. **Unequal variances permit a different comparison method.** B022 explicitly uses Welch ANOVA. Raw-data recomputation gives Brown-Forsythe p=0.0006607844 and Welch F=1.3708906394, df=(2,21.2289610784), p=0.2754590425, matching the report. Conduct votes are {vote('B022', 'trajectory_votes')}; actual-alternative votes are {vote('B022', 'alternative_votes')}. The frozen scorer recognizes only `anova.oneway` and classifies it as the wrong branch without recognizing the Welch variant. [Minitab documentation](https://support.minitab.com/en-us/minitab/help-and-how-to/statistical-modeling/anova/how-to/one-way-anova/perform-the-analysis/select-the-analysis-options/) supports Welch when equal variances are not assumed. Independence, distributional approximations, and intended use still require explanation.

2. **An unstable baseline need not prohibit exploration in another batch, but does not authorize implementation.** B006 and B028 use the same case/seed's unstable baseline and separately supplied recipe groups. B006 recommends standardizing recipe C, with conduct votes {vote('B006', 'trajectory_votes')}. B028 requires concurrent randomized confirmation before standardization, with conduct votes {vote('B028', 'trajectory_votes')} and alternative votes {vote('B028', 'alternative_votes')}. Both perform ANOVA, but their actions and causal limits differ. leading_two exactly duplicates the original recipe B/C arrays and is not independent confirmation. Post hoc cut points, contrasts, and p-values/intervals unadjusted for selection are also substantive risks. Permitting a route does not endorse every statistical statement along it.

3. **Restricted description differs from using another distribution to claim capability.** B010/B025 use historical proportions, stratification, and investigation on unstable data; conduct votes are {vote('B010', 'trajectory_votes')} and {vote('B025', 'trajectory_votes')}, respectively. Nonnormal capability or tail calculations in B009/B013 do not resolve temporal instability; their votes are {vote('B009', 'trajectory_votes')} and {vote('B013', 'trajectory_votes')}. A caveat alone does not make conduct acceptable: the issue is whether indices still support sustained-performance or implementation claims. This boundary follows [NIST's capability prerequisites](https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm).

4. **Method matches across stages can create a wrong turn that never occurred.** B011 has screening model p=0.833516 and stops RSM/optimization. Its earlier baseline `basic.one_sample_t` nevertheless triggers A_screen `divergent_evidence`. In a diagnostic call to the frozen scorer, removing only that earlier method's global match changes the focal verdict from incorrect to correct without changing the trajectory. Earlier capability in B018 and power analysis in B002 have similar effects. B018's two-sided two-sample t-test is equivalent to the two-level OLS model with an intercept at screening p=0.066418, but does not match the frozen source signature. B011/B018 may still contain excessive cause exclusion or deficient follow-up designs; finding a scoring bug does not absolve the whole report. See the {link('scoring probes', 'coordinator/scorer_probes.json')} for reproduction details.

5. **Improvement, mean attainment, individual attainment, and model confirmation are separate conclusions.** B007's raw later count is 275/80000=0.0034375, still above 0.0025; the isolated error of 273 does not change failure to meet the target. B021's mean of 58.607 exceeds 55, but 1/20 units is below 55. Its claim that the mean lies within PI [58.9541565,60.4888342] is directly false. B021 gate/conduct votes are {vote('B021', 'gate_votes')} / {vote('B021', 'trajectory_votes')}. The objective must specify whether it concerns a population mean, individual conformance rate, long-term capability, or model-prediction validity.

**Expressing STOP labels and permitted routes**

Each checkpoint should specify evidence, the prohibited conclusion/action, and the remaining routes with their conditions, rather than an unscoped STOP. At minimum, distinguish:

| Situation | Claims/actions to withhold | Permitted routes and conditions |
|---|---|---|
| Clearly inadequate MSA | Product, capability, root-cause, or implementation conclusions relying on trustworthy measurement | Diagnose measurement error; calibrate/improve standards; repeat blind testing; resume the relevant CTQ after passing retest and applicability checks |
| Unstable baseline | Stable process capability, repeatable gains, unconditional closure/release | Describe historical data accurately; investigate special causes; use justified strata; explore separate batches with defensible independence; obtain new concurrent randomized confirmation |
| Unequal variances | Unjustified pooled ANOVA/t-tests and implementation based on them | Use Welch or suitable robust/permutation methods; investigate dispersion separately; state independence, distribution, and target parameters |
| Weak screening evidence | A sole proven cause or immediate full-line changeover | Design controlled trials around power and practical effects; add factors/replicates; do not equate nonsignificance with no effect or single-arm expansion with relative causal confirmation |
| Post-change target still unmet | Completion of the absolute business objective | Acknowledge supported improvement; retain control/containment; continue improvement and target validation |
| Alternative test addresses the same business question | A penalty based solely on a different method_id | Accept justified statistical or target-equivalent evidence while retaining batch identity, assumptions, purpose, and claim limits |

Gage R&R of 10-30% is conditionally acceptable depending on application and other factors; MSA does not automatically transfer across CTQs or measurement ranges. See [Minitab's explanation of AIAG criteria](https://support.minitab.com/en-us/minitab/help-and-how-to/quality-and-process-improvement/measurement-system-analysis/supporting-topics/gage-r-r-and-wheeler-s-emp-studies/is-my-measurement-system-acceptable/).

**Preserving disagreement**

B001/B018 disagreements concern continued learning versus cause attribution/implementation. B026 STOP judgments explicitly permit cause investigation and are not substantively opposite to GO in every respect. B027 concerns transfer of diameter MSA to wall thickness; B024 concerns no I-chart signal but an MR signal. Raw binary-vote agreement therefore is not automatically a label-validity rate. Clarify the target action, statistical object, and application scope before follow-up expert adjudication. Coordinator interpretation does not change the original votes.

**Implications for the paper**

This study is a procedural blind review and scoring stress test conducted by human Black Belt experts. Human expert review is complete for this sample. It supports studying the stop-decision problem and identifies concrete scoring and permitted-route issues. Prioritize data-batch/stage binding, method-variant and equivalence recognition, and separation of permitted analyses from prohibited claims, then recompute affected metrics. Any follow-up human expert review of revised definitions should report original agreement, adjudication rules, and retained disagreements.

Independent reviews: {link('R1', 'reviews/R1.md')}, {link('R2', 'reviews/R2.md')}, and {link('R3', 'reviews/R3.md')}. Recomputations and code evidence: {link('coordinator checks', 'coordinator/FORENSIC_NOTES.md')}. The {link('source-evidence index', 'coordinator/source_evidence.json')} records human reviewer attribution, source-file hashes, and English-language updates for all 30 referenced runs. Each source `result.json` and each evidence set includes human review metadata. The reusable {link('blind-material ZIP', 'blind_packets.zip')} contains no answers; see the {link('design', 'coordinator/DESIGN.md')} and {link('review protocol', 'blind/PROTOCOL.md')} for sampling and rules. Source-record language and review metadata have been updated; numerical evidence and independent judgments are preserved.
'''
(ROOT / 'REPORT.md').write_text(report)
print('Wrote REPORT.md and ITEM_TABLE.md in English with human expert attribution')
