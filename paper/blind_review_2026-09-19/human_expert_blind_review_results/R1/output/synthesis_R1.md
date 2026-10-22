# R1 independent first-round review

This is an independent human expert review from a **Master Black Belt** perspective, emphasizing measurement adequacy, process stability, and evidential discipline. All three protocol questions were answered for all 60 units in the assigned R1 order.

| Assessment | Counts |
|---|---:|
| Focal gate | STOP 44; GO 14; UNDETERMINED 2 |
| Submitted conduct | ACCEPTABLE 36; MIXED 21; UNACCEPTABLE 3; INSUFFICIENT 0 |
| Additional computation | VALID_ALTERNATIVE 24; RESTRICTED_DESCRIPTIVE 10; MIXED 21; UNACCEPTABLE 3; NONE 2 |
| Completeness | COMPLETE 54; STOPPED_APPROPRIATELY 6 |
| Confidence | 5: 33; 4: 22; 3: 5 |

There are 22 forbidden-assertion flags and 12 forbidden-action flags, affecting 23 units in total; these overlap. One unit withholds a warranted statistical conclusion. Twenty-four STOP units have acceptable submitted conduct. These are descriptive counts for the supplied units, not estimates of system performance or a representative population.

Five findings are most consequential:

1. **A declared gate pass is not a verified measurement result.** V059 reports GRR near 15.54% with ndc 8, whereas independent crossed-ANOVA calculations give about 44.44% and fractional ndc 2.84; pooling the interaction still gives 44.34%. Its gauge SD, 8.52, even exceeds the subsequent recorded process SD, 5.84, requiring reconciliation. V039 reports 7.94% and ndc 17; the raw study gives 22.78% and about 6.03. The latter may permit conditional investigation, but the incorrect precision claim must be repaired before relying on a small centering adjustment. Conversely, V054's final restrictions are sound despite an earlier erroneous declaration releasing data.

2. **Instability limits generalization without banning useful analysis.** The reports can investigate a shift, describe observed failures, or run independent designed experiments after a baseline STOP. V011, V030, and V058 illustrate defensible, explicitly bounded routes. Deleting an unexplained exceptional lot and then inferring compliance, as in V017 and V019, is materially different. V033 recognizes the pooled instability but overstates the capability and remote-tail safety of a short, selected current segment. Selection, physical phase definition, and prospective verification matter more than merely obtaining a clean second chart.

3. **Null comparisons do not clear candidate causes.** V020, V060, V016, and V049 turn nonsignificance into exclusion or causal redirection. Effect bounds, an explicit practical equivalence margin, or a stronger design would be needed. V048 appropriately reports no demonstrated screening effect and preserves the missing-data boundary. V006's strong machine association supports an investigation priority; its explicit separation of machine totals, defect categories, and missing physical mechanism keeps the focal conduct acceptable despite strong wording.

4. **Relative improvement, absolute attainment, and individual-unit guarantees are separate decisions.** V015 and V042 show substantial recorded improvement while the sustaining rate still exceeds the commitment; their STOP dispositions are appropriate. V051 supports a conditional absolute-rate GO: 147/80,000 versus a 0.0025 maximum gives a recomputed lower-tail binomial probability of approximately 0.0000506. For seal strength, evidence that a mean exceeds 55 N does not demonstrate that every seal will exceed it. A later overstatement of that guarantee does not retroactively invalidate an earlier valid screening or baseline decision.

5. **Arithmetic and provenance errors can determine the decision.** V028's fitted stationary point is approximately (0.240716, 0.234432), not the reported doubled coordinates. Its local prediction is about 48.362 N, far below the 59.873 N confirmation mean; V050 appropriately demands reconciliation before rollout. V023 reports an inconclusive target test despite 176/5,000 versus 5% giving a recomputed lower-tail probability of approximately 2.67e-7. Conflicting roughness instructions and void-area batches leave the original gate unresolved in V024 and V055; V024 handles that conflict transparently.

The measurement judgments are decision-specific. A marginal GRR percentage does not categorically prohibit broad monitoring or a controlled trial. It also does not automatically establish reliable near-limit disposition. The five confidence-3 judgments, V012, V022, V055, V053, and V030, identify genuine questions about window selection, measurement use, scope, or the boundary between descriptive and substantive language.

The audit used complete reports, full instructions, packet focal questions and public rules, released raw batches, service events, and trace records. Identical full instructions were verified by SHA-256; all 12 unique versions were read. Python standard-library calculations independently checked relevant counts and rates, agreement/kappa, crossed-ANOVA gauge components, basic control-chart limits, means and spread, one-way ANOVA, two-proportion contrasts, binomial lower tails, factorial fits, quadratic fits, lack-of-fit F statistics, and stationary coordinates. The per-unit numerical records state what was recomputed. Other reported statistics, including unrecomputed distribution-test p-values and many confidence intervals, remain **self-report-only**. Basic point-limit checks are not proof that every special-cause pattern is absent; computed capability ratios do not validate their assumptions.

Procedural blinding was maintained. Only the assigned R1 blind directory and R1 output directory were inspected. No other reviewer output, hidden truth, scoring code, source identity, repository material, or prior study was consulted, and no review work was delegated. This was shared-filesystem procedural isolation, not OS-enforced isolation. No external technical sources were used; the source list is empty. The coordinator supplied only a structural duplication notice, not substantive opinions. The two final files are frozen first-round judgments and will not be revised for consensus.
