# Study disposition: withhold compound-response conclusions

## Executive conclusion
The retained libraries meet the facility's replication requirement, but they **cannot support a compound-versus-vehicle conclusion**: treatment and preparation batch are completely confounded after library QC. This is not evidence of no biological response. It is an inability to distinguish a compound effect from a preparation-batch effect. No gene list should be issued.

## What was computed
The facility's read-depth and mapping-rate rules were applied jointly to every library. Of **12** libraries, **4** failed and **8** remained usable. There were **2** read-depth failures and **2** mapping-rate failures. The retained counts were **4 control** and **4 treated**, so the minimum usable replication was **4** and the replication gate passed.

The usable sample sheet gives the following batch composition:

| Preparation batch | Control | Treated |
|---|---:|---:|
| L1 | 4 | 0 |
| L2 | 0 | 4 |

Across **2** retained batches, the intercept-plus-batch-plus-treatment design has **3** columns but rank **2**. The batch-only design also has rank **2**: treatment adds no independently estimable information. The required batch-adjusted treatment contrast therefore cannot be fitted uniquely.

These results are recorded in the QC and design outputs of `trace.json`; `analyze.py` and `design.py` preserve the calculations from the released JSON records.

## Cause and evidence boundary
The failed control libraries were the controls prepared in the otherwise treated batch; the failed treated libraries were the treated samples prepared in the otherwise control batch. Their exclusion removed the design's cross-arm batch overlap. Adequate arm totals alone do not preserve an identifiable comparison. The archive does not establish why those libraries had low depth or poor mapping, so their underlying technical causes remain unverified.

The steward **locked** the gene-level counts after the confounding declaration. This is a precondition failure, not a statement that the counts do not exist. No differential-expression model, fold-change estimate, adjusted significance result, batch-variance estimate, or enrichment analysis was computed. The downstream qPCR and gene-set batches remain locked behind earlier analyses; their contents were not inspected. Thus the conclusion stops at the design assessment: responding genes cannot be determined, and validation support for a candidate list cannot be assessed. No downstream result has been replaced with a guessed value or a claim of no significant genes.

## Actions and control plan
**What changed:** the analytical set was restricted to libraries passing both facility QC criteria, and the computed replication and confounding verdicts were declared to the steward. **What this achieved:** unusable libraries were excluded and a misleading compound-response claim was prevented. No wet-lab remediation or successful validation has yet occurred.

The facility should investigate the low-depth controls and poorly mapping treated libraries, including library integrity, sample identity, alignment diagnostics, and preparation records. Additional sequencing might rescue low depth where library quality permits; it should not be assumed to repair poor mapping. Evaluate whether failed libraries can be validly rescued or re-prepared while preserving interpretable batch overlap. Otherwise repeat preparation with both arms represented within preparation batches, randomized processing, and independent biological replication. Simply adding more libraries to the same arm-specific batches will not solve confounding; neither will omitting batch or applying an unsupported batch correction.

Before resuming gene calls, recompute QC and replication on the actual usable libraries and recheck design rank. Proceed only with an estimable treatment contrast and the required batch term, using the prespecified multiple-testing and effect-size criteria. Then obtain independent qPCR confirmation of the nominated candidates and apply the standing concordance rule before issuing any list. Consider gene-set interpretation only on a defensible analysis route.

Hold the process through a versioned sample sheet, recorded QC exclusions, batch-by-arm review after exclusions, and a mandatory estimability sign-off before differential expression. Assign laboratory follow-up to the facility lead and statistical release approval to the analysis lead. Preserve the raw records, scripts, and validation decisions so a repaired study can be audited rather than silently substituted for this blocked analysis.
