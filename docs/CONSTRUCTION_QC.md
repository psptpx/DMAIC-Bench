# Construction and quality-control evidence

This inventory separates source extraction, executable verification and expert
checkpoint review for the current 15-case / 97-task corpus. It records coverage,
not an assertion that every instance received independent human sign-off.

## Evidence and scope

| Stage | Record | Scope |
|---|---|---|
| Manual source extraction | Author-reported construction; `CASE_SOURCES.md`; case module provenance | Scenarios, quantities and decision evidence extracted from real project material; released measurements are generated. |
| Source recovery and verification | `archive/case-phase-ledger-2026-09-04.md`, source survey and executed recovery sections | Table/figure recovery, legacy formats, OCR, duplicate and illustrative-material identification, source checks and formula recomputation. Includes earlier-corpus work, not a final-instance approval list. |
| Graph and task checks | `tests/test_v2_graph.py`, `test_v2_graph_truth.py`, `test_v2_cases.py`, `test_v2_routes_frozen.py`, `test_truth_verification_closure.py`; Harbor reference tests | Different tests cover different invariants and scopes. Inspect parametrization and results before asserting full-instance coverage; the existence of a test is not a successful run. |
| First expert study | `paper/blind_review_2026-09-18/coordinator/DESIGN.md` and `manifest_sealed.json` | 30 checkpoints, all 15 cases, 26 distinct case/seed instances, 24 case/checkpoint pairs. Boundary-enriched, not a population error estimate or full-route review. |
| Feedback and correction | Study-1 coordinator probes; `shaft_hardness.py` unit B022 note; manuscript discussion | Evidence timing and admissible alternatives were revised while preserving original votes and disagreements. |
| Second expert study | `paper/blind_review_2026-09-19/coordinator/DESIGN.md` and `manifest_sealed.json` | 60 fresh checkpoints, 12 cases; excludes study-1 trajectories. Independent measurement after revisions, not another rule-tuning pass. |

## Scenario provenance versus route construction

The manuscript's S/P field identifies route construction. Cases 32–39 retain
an actual project route; cases 25–31 encode standards-based routes. This does
not classify scenarios as real or invented. For example, `bore_roughness.py`
and `bga_void.py` explicitly identify real black-belt project origins despite
being in the S group. Nor does retaining one source route imply that every
counterfactual seed was observed in the source project.

## Reproducible coverage inventory

Run `python scripts/construction_qc_inventory.py` in an environment with the
project dependencies. It reads the current registry and both sealed manifests,
then writes `construction_qc_coverage.csv` and `construction_qc_summary.json`.
Each CSV row is one current case/seed; empty review cells mean no sampled
checkpoint in that study, not an incorrect task or proof that no other review
occurred. Multiple reviewed model responses can share one task instance.

The script checks that sampled instances exist in the checkout. Run it on the
full research checkout; a reduced public export cannot claim full-corpus
coverage. The exported inventory contains no private source file identities or
model names. Route-construction labels follow the current published case IDs;
revisit that mapping if the corpus is extended.

## Private records to consolidate

Maintain a private case-level mapping from source report/page to extracted
fields, retained decisions, standards-derived additions and the original
extraction/review record. Include reviewer role, date, version, issue and
resolution when documented. Public counterparts can use anonymous source IDs.
Existing evidence should be consolidated before commissioning additional review.

The design documents' requirement for per-case black-belt validation does not
by itself document completion. The available checkpoint studies likewise do
not establish independent full-instance acceptance for all 97 tasks. Where
historical records are absent, record the attribution/coverage uncertainty;
where review has genuinely not occurred, target the uncovered content and
record the new review date rather than backdating it.

## Verification of this documentation revision

On 2026-09-21, the selected graph, graph-truth, frozen-route and numerical-closure
suites ran with the dependencies pinned by `pyproject.toml`: **424 passed,
1 skipped**. The exact selection was:

```
python -m pytest -q tests/test_v2_graph.py tests/test_v2_graph_truth.py \
  tests/test_v2_routes_frozen.py tests/test_truth_verification_closure.py
```

This is a selected-suite result, not a claim that the entire repository suite
or every reference-agent execution was rerun for this editorial change. The
coverage inventory was independently regenerated from both sealed manifests.
