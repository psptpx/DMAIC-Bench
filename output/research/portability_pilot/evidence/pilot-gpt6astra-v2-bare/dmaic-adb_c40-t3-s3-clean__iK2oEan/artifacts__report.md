# Study disposition: hold the compound-response conclusion

## Executive decision
The libraries do not meet the facility's minimum replication requirement. Do not issue a compound-responsive gene list or a claim of no compound effect. This is a failure of usable replication, not a negative biological result.

## Evidence and immediate cause
I applied the released QC rules to every library: assigned reads must be at least 5,000,000 and mapping rate at least 0.70. Of 12 libraries, 4 fail. The usable counts are 6 control and 2 treated; the minimum across arms is 2, below the required 3.

There are 2 libraries below the assigned-read threshold and 2 below the mapping threshold. All failed libraries are treated. This arm-specific loss is the immediate reason the study cannot support the planned conclusion. The available metrics do not establish whether preparation quality, sample quality, alignment issues, or another mechanism caused these failures.

## What can and cannot be concluded
After computing QC, I declared the observed minimum replication to the steward. The sample sheet was **locked** because replication was insufficient. This is not a denial that the data exist. Preparation-batch balance and treatment–batch identifiability therefore cannot be computed; neither confounding nor its absence has been established.

Gene-level differential expression, validation concordance, and gene-set enrichment were not computed. Counts, validation, and annotation remain downstream of the unmet gate. No genes can be named as responders from this analysis, and there is no assessed validation support for issuing a list. No batch was reported as genuinely nonexistent. A query about replacement or rescued libraries yielded no matching study fact, so their availability is unknown.

## Changes, recovery, and control
The analysis disposition was changed to a QC hold: failed libraries are excluded from eligibility, and inferential reporting is stopped. No physical library rescue or experimental redesign was performed, and no recovery benefit has been demonstrated.

The treated arm needs at least 1 additional usable biological replicate to meet the minimum, assuming all currently usable libraries remain eligible. Meeting that minimum would reopen assessment, not automatically validate the study. Review the failed libraries separately for low yield and low mapping, investigate sample and preparation records, and only resequence where the diagnosed failure can be remedied. Otherwise re-prepare or obtain replacement biological material. Technical repeats must not be counted as independent biological replication.

Preserve the original metrics and exclusions. Apply the same predeclared QC rules to replacement data, then inspect arm-by-batch allocation before choosing an identifiable expression model. Balance future preparation batches across arms and document randomization. Only after adequate replication and a valid comparison should the facility test expression, evaluate independent validation under the original criteria, and consider enrichment. Hold the release until these gates are documented; do not relax thresholds to recover a gene list.

## Audit
The accompanying trace records computed QC and failure-category diagnostics. The released data and analysis script are retained locally. All numerical study statements above are in trace outputs; unavailable downstream quantities have not been imputed.
