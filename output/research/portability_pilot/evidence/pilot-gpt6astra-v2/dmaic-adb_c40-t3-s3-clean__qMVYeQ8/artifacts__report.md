# Compound-expression study: hold pending library recovery

## Executive decision
The current libraries cannot support a compound-response conclusion under the facility's standing rules. Do not issue a candidate list. This is a failure of study readiness, not evidence that the compound has no effect.

## Computed library QC
I applied both QC requirements to each released library: at least **5,000,000 assigned reads** and mapping rate at least **0.70**. Of **12 libraries**, **4 failed**: **2** on assigned-read depth and **2** on mapping rate. These were distinct failures in the treated arm. There are **6 usable control replicates** but only **2 usable treated replicates**, below the required **3 per arm**.

The complete computation is reproducible in `analyze.py` from `data/library_qc.json`; its scalar results are recorded in the `qc.sample_qc` entry of `trace.json`.

## Where inference stops
After computing QC, I declared the observed minimum usable replicate count to the steward. The sample sheet was **locked by the replicate-sufficiency gate**, not denied as nonexistent. I did not bypass that gate or relabel failed libraries as usable.

Consequently, preparation-batch metadata were not released, and whether the treatment contrast is estimable independently of batch **could not be computed**. Confounding is neither established nor ruled out. Gene-level expression effects, adjusted significance, responding-gene identities, and gene-set enrichment were not computed. Independent qPCR concordance was not computed either. There is therefore no validated list to issue; a missing analysis must not be interpreted as an empty significant-gene list or failed biological validation.

## Cause, action, and control
The demonstrated bottleneck is insufficient usable treated replication, driven by low assigned-read yield and poor mapping. The underlying laboratory cause is not established by these metrics alone. Investigate library yield, read quality, contamination, reference compatibility, and preparation records before deciding which libraries can be recovered by additional sequencing and which need re-preparation.

No experimental change or resequencing was performed in this analysis. The action actually taken was to screen libraries and hold inference; its achieved result is prevention of an unsupported candidate release, not an improvement in library quality.

The facility should resequence or replace failed treated libraries while preserving independent biological replication. Repeat QC and retain the exclusion audit. Once each arm satisfies the replicate requirement, obtain the sample sheet and verify treatment is separable from preparation batch among usable libraries. If not, collect a balanced design rather than trying to remove complete confounding statistically. With an estimable design, include preparation batch in the expression model when applicable, apply the brief's effect-size and multiplicity rules, and then assess independent directional qPCR confirmation before any list is issued.

Hold the release through explicit QC, design-estimability, and validation checkpoints. Archive metrics, exclusions, model specifications, and validation decisions, and require review before releasing findings. No recovery outcome can yet be claimed.
