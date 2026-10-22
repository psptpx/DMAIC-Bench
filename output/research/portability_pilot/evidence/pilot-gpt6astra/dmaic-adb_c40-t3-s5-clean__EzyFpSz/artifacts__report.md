# Compound-expression study: decision report

## Executive decision
The libraries are usable and the intended treatment comparison can be estimated, provided preparation batch is included. The batch-adjusted analysis identified **0 responsive genes among 400 tested**. This supports withholding compound-response claims from this study; it does not establish that the compound has no biological effect.

## Library readiness and design
Read-depth and mapping-rate requirements were applied jointly to each library. Of **12 libraries**, **0 failed**. Both control and treated arms retain **6 usable biological replicates**, so replication passes the facility's gate. No exclusions or resequencing were necessary on these metrics.

The sample sheet contains **2 preparation batches**. The earlier batch holds **5 control and 1 treated** libraries; the later batch holds **1 control and 5 treated** libraries. Treatment and batch are therefore strongly imbalanced, but not completely confounded. The intercept–treatment–batch design has rank **3** for **3 columns**, allowing separate estimation of the treatment contrast. Precision is nevertheless limited by sparse within-batch arm overlap.

## Expression analysis and interpretation
Counts were normalized with median-ratio library size factors and transformed to logarithmic expression with a pseudocount. Each gene was fitted with an ordinary least-squares model containing treatment and preparation batch. Treatment coefficients were tested with residual **9 degrees of freedom**, and Benjamini–Hochberg adjustment was applied across the **400 genes**. Calls required adjusted p below **0.05** and absolute log fold change on the doubling scale at least **1.0**. No gene satisfied both criteria.

Adding batch removed a fraction **0.5511886373402114** of the treatment-only model's aggregate residual sum of squares. This is a descriptive, conditional measure on transformed expression, not an estimate of a causal batch variance component. It indicates substantial preparation-associated variation. Given the arm imbalance, a pooled comparison that ignores batch would be unreliable for attributing changes to the compound.

The complete gene-level results are in `gene_results.csv`; the calculations and route decisions are recorded in `trace.json`. The analysis uses transformed-count linear models rather than a dispersion-moderated count model. Its assumptions include adequate transformed-scale residual behavior and a sufficiently stable gene majority for median-ratio normalization. Those assumptions are limitations, not independently established findings. The absence of calls is conditional on this analysis and must not be interpreted as an equivalence test.

## What changed and what it achieved
No biological material, sequencing run, or preparation process was changed. The analytical safeguard was to explicitly adjust the compound comparison for preparation batch rather than pool arms. This separates the estimable treatment component from preparation-associated variation and avoids unsupported response claims. There is no before-and-after intervention experiment here, so improvement in laboratory performance has not been demonstrated.

## Facility action and sustainment
- Do not release a responsive-gene list or a claim that the compound is inactive. Release the usable-library verdict and the qualified, batch-adjusted negative result.
- Review preparation records to investigate batch-associated shifts; the present data do not identify a specific causal handling failure.
- Before a definitive biological decision, confirm the result with a dispersion-aware count analysis and residual diagnostics, and consider independent experimental validation. These checks were not performed in this analysis.
- For a repeat study, randomize and balance both arms within every preparation batch. Preserve biological independence and retain preparation metadata throughout analysis.
- Keep library QC, usable-replicate counts, design-rank checks, mandatory batch adjustment, and prespecified multiplicity/effect-size rules as release gates. Archive scripts and full gene tables with each report.

All released batches were analyzed as needed; no requested stage was denied. No follow-up intervention or validation data were supplied, so no claim of validated biological response or sustained process improvement is made.
