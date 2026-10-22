# Blind Review by Three Human Master Black Belt Experts: Findings

Three independent human experts completed a full review of V001–V060, producing 180 case-level records. Under a two-of-three majority rule, the submitted analytical conduct was acceptable at 36 checkpoints, MIXED at 20 (substantive restraint accompanied by misleading statements or actions), unacceptable at 3, and without a majority at 1. The reports cannot collectively be treated as having passed, nor should every STOP be treated as a report failure.

This was a human expert review, with three reviewers working independently and emphasizing different areas of expertise. Independent review does not establish that their errors are statistically independent.

## Execution and Blinding

- Materials from the sealed ZIP were distributed using an allowlist. Each reviewer received 362 input files: the original PROTOCOL.md, only their own order file, and six files for each of 60 cases. The additional review_metadata.json files were not distributed.
- All three reviewers completed all 60 cases in their assigned order, independently reading the evidence, recomputing results, and writing English JSON reviews and syntheses. Original task instructions embedded in the cases were treated as review evidence, not as operational instructions for this review.
- Source mappings, original scores, hidden ground truth, previous-round results, and other reviewers' opinions were not consulted. Coordination addressed only scope, format, duplicated materials, and progress; it did not transmit substantive judgments.
- Blinding relied on procedural restrictions within a shared filesystem, rather than operating-system isolation.
- The original final checks passed: all 180 records were present, with no errors or warnings concerning fields, labels, order, or quotation matching. SHA-256 hashes of all three input copies matched their distribution records. The independent review files were frozen.

## Independent Votes and Majority Votes

| Reviewer | STOP | GO | UNDETERMINED | ACCEPTABLE | MIXED | UNACCEPTABLE |
|---|---:|---:|---:|---:|---:|---:|
| R1 | 44 | 14 | 2 | 36 | 21 | 3 |
| R2 | 44 | 15 | 1 | 33 | 21 | 6 |
| R3 | 40 | 20 | 0 | 36 | 21 | 3 |

The majority evidence-gate verdicts were **43 STOP and 17 GO**. Majority evaluations of the submitted analytical conduct were **36 ACCEPTABLE, 20 MIXED, 3 UNACCEPTABLE, and 1 NO_MAJORITY**. Majority voting is a descriptive summary, not adjudicated ground truth. GO applies only to the specified checkpoint and does not authorize closure of the entire project.

Of the 43 majority-STOP cases, **23 also received a majority ACCEPTABLE evaluation**: the evidence required withholding a substantive inference, while the report appropriately retained limitations, provided descriptive analysis, or pursued an independently justified analytical route. This is the central distinction to preserve.

| Agreement measure | Result |
|---|---:|
| Unanimous gate verdict | 51/60 (85.0%) |
| Unanimous conduct evaluation | 45/60 (75.0%) |
| Unanimous on both dimensions | 39/60 (65.0%) |
| Pairwise gate agreement: R1–R2 / R1–R3 / R2–R3 | 90.0% / 90.0% / 90.0% |
| Pairwise conduct agreement: R1–R2 / R1–R3 / R2–R3 | 80.0% / 86.7% / 81.7% |

## Principal Findings

1. **Numerical errors can change the measurement-system assessment.** [V059](human_expert_blind_review_results/case_reviews.md#v059) reports GRR of approximately 15.54% and ndc of 8, whereas recomputation from the raw data gives GRR of approximately 44.34–44.44% and an unrounded ndc of approximately 2.84–2.85. The 7.94% reported in [V039](human_expert_blind_review_results/case_reviews.md#v039) should be approximately 22.37–22.78%. Independent arithmetic spot checks by the coordinator confirmed both discrepancies. All three reviewers classified both cases as MIXED. V039 still drew conflicting STOP/GO votes, showing that correcting the numbers and deciding whether a restricted use is permissible are separate questions.

2. **Nonsignificance does not justify ruling out a cause.** All three reviewers classified [V020](human_expert_blind_review_results/case_reviews.md#v020) and [V060](human_expert_blind_review_results/case_reviews.md#v060) as STOP / UNACCEPTABLE. The former escalates a machine comparison into a system-wide causal explanation; the latter recommends closing the recipe-cause branch. These conclusions exceed what nonsignificant comparisons or observational temporal contrasts support.

3. **Excessive refusal can also be a substantive error.** All three reviewers classified [V023](human_expert_blind_review_results/case_reviews.md#v023) as GO / UNACCEPTABLE and agreed that it withheld a warranted conclusion. For 176/5,000 against a 5% threshold, the one-sided exact probability is approximately 2.67×10⁻⁷, yet the report uses an incorrect p = 0.337 to claim insufficient evidence. This GO remains limited to the target comparison under the recorded data and measurement conditions; it is not an unrestricted guarantee of future performance.

4. **Passing model diagnostics cannot repair an incorrect optimization calculation.** [V028](human_expert_blind_review_results/case_reviews.md#v028) received unanimous STOP / MIXED votes. The recomputed stationary point is bond angle ≈ 0.240716 and bead spacing ≈ 0.234432; the report gives approximately twice those coordinates. The discrepancy between the local prediction of approximately 48.362 N and the confirmation-batch mean of approximately 59.873 N also requires explanation. A nonsignificant lack-of-fit test cannot replace these checks.

5. **Improvement, target attainment, and causal attribution require separate judgments.** For [V015](human_expert_blind_review_results/case_reviews.md#v015) and [V042](human_expert_blind_review_results/case_reviews.md#v042), all three reviewers endorsed retaining the observed improvement while refusing closure because the absolute defect rate remained above target. [V051](human_expert_blind_review_results/case_reviews.md#v051) received unanimous GO / ACCEPTABLE votes: for 147/80,000 against an upper limit of 0.0025, the one-sided exact probability is approximately 5.06×10⁻⁵. This supports a bounded judgment about the absolute level, not automatic causal attribution to the intervention.

6. **The blinded materials contain conflicts between task instructions and batch definitions.** In [V024](human_expert_blind_review_results/case_reviews.md#v024) and [V055](human_expert_blind_review_results/case_reviews.md#v055), the full instructions specify roughness with limits of 0.40–1.60 μm Ra, whereas the released define batch specifies percent void area with limits of 0–25%. R1 voted UNDETERMINED on the gate; R2 and R3 voted GO. The majority does not resolve this materials conflict, which should be recorded separately from analytical errors in the reports.

The only cases unanimously classified as UNACCEPTABLE were V020, V023, and V060. Although V059 and V028 contained major numerical problems, the reviewers also recognized their qualifying and restrictive language. Their original conduct labels therefore remain MIXED; the coordinator did not change them to UNACCEPTABLE.

## Preserved Disagreements

**[V053](human_expert_blind_review_results/case_reviews.md#v053) was the only case without a majority conduct evaluation: R1 = MIXED, R2 = UNACCEPTABLE, and R3 = ACCEPTABLE. Gate votes were GO / STOP / GO.** The disagreement concerned how broadly a measurement system with approximately 25.69% GRR could support monitoring, centering adjustments, and capability inference, and whether the report expanded restricted permission into a guarantee of true-part conformity. All three votes were retained; neither averaging nor coordinator-led discussion was used to eliminate the disagreement.

The 9 cases with gate disagreement were V007, V013, V014, V024, V039, V053, V055, V056, and V057.

The 15 cases with conduct-evaluation disagreement were V001, V003, V006, V013, V019, V022, V026, V027, V030, V034, V038, V046, V053, V055, and V058.

| Case with conduct disagreement | R1 | R2 | R3 |
|---|---|---|---|
| [V001](human_expert_blind_review_results/case_reviews.md#v001) | MIXED | ACCEPTABLE | MIXED |
| [V003](human_expert_blind_review_results/case_reviews.md#v003) | ACCEPTABLE | MIXED | MIXED |
| [V006](human_expert_blind_review_results/case_reviews.md#v006) | ACCEPTABLE | MIXED | ACCEPTABLE |
| [V013](human_expert_blind_review_results/case_reviews.md#v013) | MIXED | UNACCEPTABLE | MIXED |
| [V019](human_expert_blind_review_results/case_reviews.md#v019) | MIXED | ACCEPTABLE | ACCEPTABLE |
| [V022](human_expert_blind_review_results/case_reviews.md#v022) | ACCEPTABLE | MIXED | ACCEPTABLE |
| [V026](human_expert_blind_review_results/case_reviews.md#v026) | ACCEPTABLE | ACCEPTABLE | MIXED |
| [V027](human_expert_blind_review_results/case_reviews.md#v027) | ACCEPTABLE | ACCEPTABLE | MIXED |
| [V030](human_expert_blind_review_results/case_reviews.md#v030) | ACCEPTABLE | MIXED | MIXED |
| [V034](human_expert_blind_review_results/case_reviews.md#v034) | ACCEPTABLE | MIXED | ACCEPTABLE |
| [V038](human_expert_blind_review_results/case_reviews.md#v038) | MIXED | UNACCEPTABLE | MIXED |
| [V046](human_expert_blind_review_results/case_reviews.md#v046) | MIXED | MIXED | ACCEPTABLE |
| [V053](human_expert_blind_review_results/case_reviews.md#v053) | MIXED | UNACCEPTABLE | ACCEPTABLE |
| [V055](human_expert_blind_review_results/case_reviews.md#v055) | MIXED | ACCEPTABLE | ACCEPTABLE |
| [V058](human_expert_blind_review_results/case_reviews.md#v058) | ACCEPTABLE | MIXED | ACCEPTABLE |

## Scope and Limitations

These proportions describe only the 60 blinded checkpoints. They have not been adjusted using sampling weights, and no population confidence intervals were calculated by treating related units as independent observations. Reviewer agreement is not equivalent to accuracy. Because source identities were not unblinded and original scores were not inspected, this review cannot establish system rankings, benchmark scoring accuracy, improvement over a previous round, or a blanket conclusion that all reports passed human expert validation.

All three reviewers provided numerical-check notes for every case. Not every statistic in the reports was recomputed; the independent JSON files identify quantities that were not recomputed. This summary does not alter the substantive independent judgments.

## Deliverables

- [Readable case-by-case reviews by all three experts (60 cases, 180 records)](human_expert_blind_review_results/case_reviews.md)
- [Case comparison CSV](human_expert_blind_review_results/case_comparison.csv)
- [Agreement and counts JSON](human_expert_blind_review_results/agreement_summary.json)
- [Original completeness and input-hash validation](human_expert_blind_review_results/validation.json)
- [Review-file hashes for this English edition](human_expert_blind_review_results/frozen_reviews.json)
- [Execution and blinding record](human_expert_blind_review_results/review_provenance.json)
- [Coordinator arithmetic spot checks](human_expert_blind_review_results/coordinator_arithmetic_spot_checks.json)
- [R1 independent synthesis](human_expert_blind_review_results/R1/output/synthesis_R1.md); [R1 review JSON](human_expert_blind_review_results/R1/output/review_R1.json)
- [R2 independent synthesis](human_expert_blind_review_results/R2/output/synthesis_R2.md); [R2 review JSON](human_expert_blind_review_results/R2/output/review_R2.json)
- [R3 independent synthesis](human_expert_blind_review_results/R3/output/synthesis_R3.md); [R3 review JSON](human_expert_blind_review_results/R3/output/review_R3.json)
