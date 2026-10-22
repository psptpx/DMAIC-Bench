# Study disposition: hold compound-response conclusions

## Executive assessment
The current libraries cannot support a facility-compliant compound-versus-vehicle conclusion. Of **12 libraries**, **4 fail** the facility's usability rules, leaving **8 usable libraries**: **6 control** and **2 treated**. The minimum retained arm size is therefore **2**, below the required **3**. Do not issue gene-response calls from this release. This is insufficient evidence, not evidence that the compound has no effect.

## What was measured
I applied the facility's joint library rule to every released sequencing record: assigned reads must be at least **5,000,000**, and mapping rate must be at least **0.70**. A failure of either criterion excludes the library. There are **2 low-read failures** and **2 low-mapping failures**. All failed libraries belong to the treated arm. The quantitative results and thresholds are recorded in `trace.json`, under `qc.sample_qc`; the reproducible calculation is in `analyze.py`.

The immediate reason for the study hold is loss of treated-arm replication. The metrics identify read yield and mapping performance as the failure modes; they do not establish whether preparation, sample quality, contamination, sequencing, or reference/processing choices caused those failures. These possibilities require investigation, not attribution from these data alone.

## Design and gene-level conclusions
The steward withheld the arm/preparation-batch sample sheet because the computed replication requirement was not met. This was a **locked prerequisite**, not a claim that the sample sheet does not exist. Gene-level counts remain downstream of that locked stage. Thus treatment–batch identifiability, batch effects, differential-expression estimates, and adjusted significance could not be computed. No assertion of confounding or of an unconfounded design is justified. No responding-gene list can be provided; this must not be interpreted as an empty list of significant genes.

A request for remediation follow-up returned the original metrics, not a new post-remediation dataset. No verified improvement or rescue has been demonstrated in the supplied records.

## Action for the facility
- Hold inferential reporting and preserve the failing libraries' QC flags. Excluding them from the usable set is the analytical disposition already made; no wet-lab correction was performed in this analysis.
- Investigate low yield separately from poor mapping. Assess whether additional sequencing can rescue low-yield libraries. For poor mapping, review raw-read quality, sample identity, contamination, reference suitability, and preparation records before committing more sequencing; reprepare where warranted.
- Resequence or replace affected treated libraries so that both arms meet the usable biological-replicate requirement. Additional reads from the same biological sample are not additional biological replicates.
- Once the replication gate passes, obtain the sample sheet and test whether the compound contrast is separately estimable from preparation batch. If treatment and batch are inseparable, redesign with arms represented across batches; statistical adjustment cannot recover a missing contrast.
- Only after those gates pass, obtain counts, use an appropriate count-based model including preparation batch when applicable, and apply the brief's effect-size and multiplicity-adjusted calling rules.

## Sustain and verify
Assign the sequencing/QC lead responsibility for documenting the failure investigation and rescue records, and the analysis lead responsibility for independently rechecking retention and design estimability before releasing results. Keep the same usability criteria rather than relaxing them after observing failures. Archive original and replacement metrics, biological sample identities, preparation batches, model specifications, and a fresh analysis trace. Resume conclusions only after documented QC and design sign-off; report the actual post-remediation outcome rather than assuming the intervention worked.
