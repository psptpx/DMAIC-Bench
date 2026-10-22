# Sequencing study status report

## Executive conclusion

The libraries are technically usable and the treatment comparison is estimable on this design. The expression analysis nominated 39 genes, but independent qPCR validation confirmed 0 of 10 nominated candidates, giving a concordance of 0.0. The required minimum concordance is 0.75, so the candidate list must be withheld. The panel result should be reconsidered rather than issued as a validated compound-response list.

## What was assessed

- **Library QC:** 0 libraries failed the read-count and mapping-rate rules. The minimum usable replicate count across the two arms was 6, so the minimum-replicate requirement was met.
- **Design:** The design was not confounded, and it contained 1 preparation batch with both arms represented. The treatment contrast was therefore estimable.
- **Expression:** The analysis used library-size normalization, log2-transformed counts, Welch two-sample tests, and Benjamini–Hochberg adjustment. It evaluated 400 genes with 6 control and 6 treated libraries. A gene was nominated only when adjusted p was below 0.05 and absolute log2 fold change was at least 1.0. This yielded 39 nominations.
- **Validation:** Independent qPCR used 4 biological replicates per arm for 10 nominated genes. Confirmation required p below 0.05 and matching direction. 0 genes met that rule; concordance was 0.0, below the required 0.75.

## Nominated genes from the panel analysis

G0002, G0005, G0038, G0045, G0055, G0060, G0062, G0100, G0108, G0112, G0125, G0153, G0156, G0165, G0169, G0173, G0210, G0214, G0215, G0237, G0239, G0241, G0244, G0247, G0263, G0265, G0267, G0271, G0284, G0314, G0327, G0333, G0339, G0341, G0366, G0370, G0372, G0379, G0387

This is an analysis nomination only, not an issuable validated candidate list.

## Current business decision

The study can carry a technically valid treatment comparison, but it cannot support release of a validated candidate list. The immediate cause is validation failure: none of the nominated genes satisfied the independent qPCR confirmation rule. Because the validation gate was not met, the gene-set annotation batch was not released; no annotation-based interpretation was performed.

## What changed and what it achieved

The analysis applied the facility QC and design gates before calling genes, then applied the stated expression thresholds and the independent validation rule. This established that the sequencing material and comparison design are adequate, while preventing unsupported biological claims from being issued.

## Recommended next actions and control

Withhold the candidate list. Review the panel analysis and qPCR experiment together, check assay directionality and sample handling, and repeat or extend independent validation before reconsidering release. Any future release should again require the same QC, design, expression, and validation gates, with the computed decisions recorded in the analysis trace.

## Data and computation note

All quantitative results above were computed from the steward batches and recorded in `/workspace/trace.json`. The gene-set annotation was not provided because its steward gate requires validation concordance of at least 0.75 and the computed concordance was 0.0.
