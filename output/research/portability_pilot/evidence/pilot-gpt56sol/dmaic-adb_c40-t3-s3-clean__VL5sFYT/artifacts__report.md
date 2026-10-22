# Study status report

## Executive conclusion

The libraries cannot currently support the planned compound-versus-control conclusion. Library QC failed: **4 of 12** libraries were unusable, leaving **6** usable control libraries but only **2** usable treated libraries. The minimum arm count is therefore **2**, below the required **3**.

The sample sheet was consequently locked by the steward. Preparation-batch identifiability could not be assessed, including whether treatment is confounded with batch. Gene-level read counts were also unavailable behind the unmet gates. Therefore differential expression was not computed, and it is not valid to report either responding genes or an absence of responding genes. The gene-level conclusion stops here.

## What caused the stop

The usable-library rule required at least **5000000** assigned reads and mapping rate at least **0.7**. Among the failed libraries, **2** failed the read-depth rule and **2** failed the mapping-rate rule. All failures were in the treated arm, producing the arm imbalance above.

## What was changed and achieved

No study data were altered and no failed library was substituted. The QC predicates were applied to all **12** released library records, and the computed minimum replication of **2** was declared to the steward. That declaration correctly held the downstream releases rather than allowing an unsupported gene analysis.

## Required next action and control plan

Recover at least **1** additional usable treated library by resequencing an affected treated library or preparing a valid replacement. Then:

- rerun the same assigned-read and mapping-rate checks;
- confirm that each arm retains at least **3** usable libraries;
- obtain the sample sheet and determine whether arm is separable from preparation batch;
- if separable, fit the treatment comparison with preparation batch included as required;
- apply the prespecified gene-call thresholds only after those gates pass.

Keep the release gates in place: failed replication must continue to block design assessment and gene calling, and an unidentifiable treatment contrast must block gene calling even after library QC is repaired.
