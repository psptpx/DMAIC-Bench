# Study disposition: withhold conclusions and re-sequence

## Executive conclusion
The libraries cannot support a compound-response conclusion under the facility's standing rules. Of 12 libraries, 4 fail QC. All 6 control libraries remain usable, but only 2 treated libraries remain, below the required minimum of 3 per arm. No candidate list should be issued. This is an insufficient-data finding, **not evidence that the compound has no effect**.

## What was computed
I applied both acceptance criteria to each library: assigned reads at least 5,000,000 and mapping rate at least 0.70. There are 2 low-read failures and 2 low-mapping failures. The low-read failures are S07 and S10; the low-mapping failures are S09 and S12. The retained treated libraries are S08 and S11; all control libraries pass. These calculations use the full released per-library metrics, not the preview alone. The computed counts and applied thresholds are recorded in `trace.json`.

The immediate cause of the stop is loss of treated-arm replication through inadequate read yield and inadequate mapping. The metrics alone do not establish the underlying laboratory or biological causes of those failures.

## Where the conclusion stops
After I declared the computed minimum usable replication, the steward locked the sample sheet because the replication requirement was not met. It was **locked, not denied or demonstrated nonexistent**. Consequently, preparation-batch structure could not be inspected and treatment-versus-batch identifiability could not be computed. I cannot say whether this design is confounded or estimable.

No gene-count analysis, batch-effect assessment, differential-expression test, validation concordance, or gene-set enrichment was run. Those downstream materials were not released along this route. Responding genes and validation support therefore remain undetermined; there is no defensible gene list. A request for existing remedial sequencing data returned only the original QC batch, not evidence of a successful repair.

## Action and control plan
The change made during this review was analytical: exclude failing libraries from eligibility and stop gene calling. It exposed the treated-arm replication shortfall and prevented an unsupported candidate release. No laboratory correction has yet been demonstrated, and no improvement in usable replication is claimed.

Investigate low assigned-read yield separately from poor mapping. Review library integrity, alignment quality, sample identity and possible contamination before deciding whether to add sequencing depth or reprepare affected libraries. Re-sequence first as required by the brief, retaining biological replicate identity; extra technical reads must not be counted as new biological replicates.

After remediation, repeat the same library-level QC and require the minimum usable replication in each arm. Then audit the sample sheet for treatment estimability independently of preparation batch. If that condition fails, redesign with treatment and control represented across preparation batches rather than attempting to correct a nonestimable contrast computationally. If multiple batches are present in an estimable design, include batch in the expression model.

Only after these gates pass should the facility apply its prespecified fold-change and multiple-testing rules, nominate candidates, and evaluate independent qPCR against its direction-and-significance concordance rule. Withhold the list if validation fails. Preserve the exclusion log, sample identities, batch assignments, versioned analysis, and an explicit release checklist so that QC, design and validation gates remain enforced on the rerun.
