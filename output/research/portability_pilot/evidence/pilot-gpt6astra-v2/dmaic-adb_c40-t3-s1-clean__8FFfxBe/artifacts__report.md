# Compound-expression study: conclusion withheld

## Executive decision
The libraries pass the facility's usability and replication requirements, but the experimental design cannot support a compound-specific expression conclusion. Treatment is completely confounded with preparation batch. Withhold any candidate list; this is an unidentifiable comparison, not evidence that the compound has no effect.

## Computed findings
Using the complete released sequencing metrics, I applied both facility usability criteria to every library and counted retained libraries by arm. All **12 libraries** are usable; **0 failed**. The control and treated arms each retain **6 usable biological replicates**, so inadequate sequencing quality or replication is not the current bottleneck.

I then joined the usable library identifiers to the sample sheet and constructed an additive design with an intercept, preparation-batch indicator, and treatment indicator. There are **2 batches**. The first contains **6 controls and 0 treated libraries**; the second contains **0 controls and 6 treated libraries**. There are **0 mixed-arm batches**. The design has **3 columns but rank 2**; the batch-only design also has **rank 2**. Adding treatment supplies no independent information. A separate treatment coefficient therefore cannot be estimated.

These results are recorded in `trace.json`; the computations are retained in `analyze.py` and `design.py`. The analysis used only released records and excluded no libraries.

## What cannot be concluded
The steward locked gene-level counts after the computed confounding verdict was declared. This was a prerequisite failure, not a denial that the data exist. Differential expression, adjusted significance, compound-specific fold changes, and a responding-gene count were **not computed**. There is no defensible nominated list from this analysis.

Independent qPCR data and gene-set annotations remain downstream of the blocked analysis and were not obtained or analysed. Validation concordance and enrichment therefore cannot be reported, and validation cannot be claimed to support issuing a list. The conclusion stops at the design failure. Neither an unadjusted arm comparison nor software batch correction can recover information absent from this design; either would risk attributing preparation differences to the compound. The magnitude of any actual batch effect is also unknown.

## Action for the facility
**Immediate containment:** flag the study as design-confounded and suspend compound-specific gene calls and candidate-list release. Preserve the existing libraries and raw records as technical evidence, not as proof of treatment response. The action taken here was analytical containment and declaration of the failed design prerequisite; no wet-lab correction has been performed or evaluated.

**Corrective work:** plan a balanced, randomized preparation in which both arms are represented within preparation batches, with adequate biological replication after QC. Where original biological material can be re-prepared, assess its suitability and retain biological-sample identity so repeated preparations are not counted as independent biological replicates. Otherwise repeat the experiment with new biological replicates. Merely sequencing the same confounded libraries more deeply will not solve this problem.

**Release and sustain:** require sample-sheet approval and an explicit design-rank check before preparation, repeat usability and identifiability checks after exclusions, then fit the prespecified batch-adjusted expression model. Apply the facility's multiplicity and effect-size rules, and require independent qPCR concordance before issuing candidates. Keep allocation, exclusions, model specification, and release decisions in a versioned audit trail. No improvement in biological inference can be claimed until the redesigned study passes these gates.
