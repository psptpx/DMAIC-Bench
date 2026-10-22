# Compound-expression study status

## Executive conclusion

The libraries cannot currently support the planned conclusion. QC evaluated **12** libraries and failed **4**. The control arm retained **6** usable libraries, while the treated arm retained **2**; the cross-arm minimum is therefore **2**, below the required **3**. The replicate-sufficiency result is false, so the facility's standing rule requires re-sequencing before any gene is called.

The intended treatment comparison also cannot yet be judged estimable separately from preparation batch. The sample sheet was locked after the replicate gate failed, so batch confounding was not computable. Gene-level counts were consequently also locked. There is therefore no defensible list of responding genes, rather than a result of no responding genes.

## What is causing the stop

Application of both library usability rules found **2** read-depth failures and **2** mapping-rate failures. Together these leave the treated arm below the required replication level. This is the immediate cause of the analysis stop.

## What was changed and what it achieved

No study data were altered and no failed library was substituted. The QC rules were applied to the released sequencing metrics, and the computed minimum usable replication was declared to the steward. That declaration correctly held the downstream sample-sheet and count batches behind the failed gate. A request for a remediation fact found no recorded process fact, so no post-remediation metrics could be computed.

## Required next action and hold plan

Re-sequence or replace enough failed treated libraries to bring the treated arm to at least **3** usable libraries under the same read-depth and mapping criteria. Then rerun library QC and retain the release gate: downstream work proceeds only when every arm meets the required usable replication.

After that gate passes, release the sample sheet and test whether treatment is separable from preparation batch. If it is separable, release the count matrix and fit the prescribed batch-adjusted expression model; only then apply the facility's adjusted-significance and fold-change rules. If treatment and batch are confounded, do not call genes; redesign or generate balanced libraries first.

## Evidence limitations

There is no released sample-sheet data for the design check and no released count data for differential expression. Consequently, batch effects, treatment estimability, fold changes, adjusted significance, and the number or identities of responding genes could not be computed. The conclusion stops at library QC.
