# Study status: hold biological conclusions pending library recovery

## Executive conclusion
The current libraries cannot support gene calls under the facility's standing rules. Of **12 libraries**, **4 fail QC**, all in the treated arm. The usable set retains **6 control** and **2 treated** biological replicates. The minimum retained replication is therefore **2**, below the required **3 per arm**. This is an insufficient-evidence result, not evidence that the compound has no effect.

## What was computed
I applied both usability criteria to every library in the released sequencing-metrics batch: assigned reads must be at least **5,000,000** and mapping rate at least **0.70**. A library failing either criterion was excluded from the usable set. **2 libraries fail assigned-read depth**, and **2 fail mapping rate**. These counts and the retained arm totals are recorded in the QC step of `trace.json`; the script is retained as `analyze.py`.

The observed immediate constraint is loss of treated-arm replication through both low depth and poor mapping. The underlying technical cause has not been established. These metrics alone cannot distinguish preparation failure, input quality, contamination, or other alignment problems.

## Limits of the conclusion
The computed replication verdict was declared to the steward. The sample sheet was then **locked by the replication gate**. It was not denied as nonexistent. Consequently, I could not assess treatment–preparation-batch confounding or determine whether the intended contrast is estimable independently of batch. No design verdict was fabricated, and no gene-level analysis was run. Differential-expression effect sizes, adjusted significance values, and the number of responding genes are **not computed**. There is no supported gene list.

A request for remediation QC returned the original metrics, not a new post-change batch. A question to the study lead about completed remediation was unroutable, with no matching process fact. Thus no completed corrective action or improvement is demonstrated by the available evidence.

## Recommended action and release controls
- Hold the current biological interpretation and gene calls; preserve the original metrics and exclusion audit.
- Investigate low-depth and low-mapping treated libraries separately. Review input quality, preparation records, read quality, contamination, and alignment diagnostics before deciding which libraries can be recovered by deeper sequencing and which require re-preparation.
- Re-sequence first as required by the facility policy, with re-preparation where the diagnostic review warrants it. Additional reads are not automatically a remedy for poor mapping. Technical reruns must not be counted as new biological replicates.
- Recompute both QC criteria after recovery. Resume only when each arm retains at least **3 usable biological replicates**; preferably recover the planned biological set rather than merely meeting the minimum.
- Once QC permits release, audit the sample sheet for a treatment contrast separable from preparation batch. If treatment and batch cannot be separated, obtain a balanced follow-up design rather than attempting to correct an unidentifiable contrast computationally. Include batch in the expression model whenever multiple batches are present.
- Only then analyze released gene counts and apply the brief's effect-size and multiple-testing criteria. Retain an explicit QC and design sign-off with each future analysis release.

The change made here was an **analytical hold**, not an experimental intervention. It prevented unsupported inference; no measured recovery or biological outcome has yet been achieved. The facility should hold that boundary through a documented QC gate, a subsequent design gate, and an auditable rerun after remediation.
