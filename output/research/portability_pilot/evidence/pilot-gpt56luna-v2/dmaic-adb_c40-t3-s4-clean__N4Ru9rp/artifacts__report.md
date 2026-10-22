# Compound-versus-vehicle panel study report

## Executive conclusion

The libraries can carry a conclusion and the planned treatment-versus-control comparison is estimable. All 12 libraries passed the stated usability rules, leaving 6 usable control replicates and 6 usable treated replicates. The design is not confounded: both arms are represented in the single preparation batch.

However, the expression analysis nominated no genes. The result is therefore a negative panel result under the prespecified calling rule, not evidence that every gene is biologically unchanged. No candidate list should be issued.

## What was measured and changed

The QC computation found 0 failed libraries and a minimum of 6 usable replicates per arm. The minimum replicate requirement was met. The design computation found `confounded = false` and `batchCount = 1`, so the treatment contrast is identifiable; there was no multi-batch term to add.

For expression, the complete panel contained 400 genes and the analysis used 6 control and 6 treated libraries, library-size CPM normalization, log2(CPM+1) transformation, two-sample treatment-versus-control tests, and Benjamini-Hochberg adjustment. The computed count of genes meeting both calling criteria was 0.

## Validation and annotation

The independent qPCR batch contained 0 nominated candidates. Consequently, there are 0 confirmed candidates and no empirical validation concordance can be defined. The recorded concordance value of 1.0 is vacuous for an empty candidate set; it must not be interpreted as independent confirmation. The validation rule therefore does not support issuing a candidate list.

The gene-set annotation was released, but no enrichment computation was run because the called-gene set is empty. There is no gene-set result to report and no biological pathway conclusion should be drawn from this panel result.

## Where the study stands

- Library readiness: adequate; 0 libraries failed QC, with 6 usable replicates in each arm.
- Design readiness: adequate; the contrast is estimable and `confounded = false`.
- Compound-responsive genes: 0 genes passed the calling rule.
- Validation: no candidates were available for qPCR confirmation, so validation cannot support a list.
- Issuable output: no candidate list.

## Recommended next action

Hold the candidate list. First review the negative result with the study lead and confirm that the biological effect size expected from the compound is compatible with the observed assay sensitivity. If a positive result is required, repeat or extend the experiment with a prespecified power and effect-size plan, preserving balanced treatment and control allocation within each preparation batch. Any future candidate list should again require independent qPCR confirmation before release.

## Control and traceability

The computations and route decisions are recorded in `/workspace/trace.json`. The gene-set batch was not used to manufacture a result: because 0 genes were called, enrichment was not computed. No denied data batch stopped the conclusion; the initial locked releases were obtained after declaring the computed replicate, design, and empty-candidate gate results.
