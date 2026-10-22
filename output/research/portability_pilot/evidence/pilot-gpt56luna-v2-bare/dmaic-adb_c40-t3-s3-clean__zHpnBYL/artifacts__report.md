# Study status report

## Executive conclusion

The released sequencing QC does not support the planned compound-versus-vehicle comparison. The QC found 4 failed libraries out of 12. The control arm has 6 usable libraries, but the treated arm has only 2. The minimum usable replicate count is therefore 2, below the facility requirement of 3.

The immediate cause is treated-arm library QC failure: some treated libraries do not meet the assigned-read and/or mapping-rate rules. The facility rules require at least 5000000 assigned reads and a mapping rate of at least 0.7 for a library to be usable.

## What was computed and what changed

I applied both stated usability rules to every released library and recorded the result in `trace.json` as `qc.sample_qc`. The QC result was declared to the steward as `min_replicates=2`, and the design was declared confounded. That declaration did not release the next batch because the steward requires at least 3 usable replicates per arm.

## What cannot be concluded

The steward refused the sample-sheet request because the replicate gate was not met. There is no released sample-sheet data for preparation-batch assessment, so design identifiability and batch confounding cannot be computed beyond the failed replicate gate. The gene-level read-count batch is consequently unavailable; the number of responsive genes cannot be computed and no gene list should be issued. The qPCR validation batch and gene-set annotation are also unavailable, so validation concordance and enrichment cannot be computed.

## Recommended next action

Do not issue a biological response list from this archive. Investigate the treated-arm library failures and repeat or replace the failed treated libraries, then rerun the complete QC and release sequence. Once the replicate gate is met, reassess preparation-batch balance before performing gene-level testing, and only then nominate candidates for qPCR confirmation.

## Holding the improvement

Retain the per-library QC rule as a release gate, require the minimum usable replicate count before downstream analysis, and preserve the computed QC table and steward declarations with the study record. This prevents an under-replicated treated arm from being presented as a supported comparison.
