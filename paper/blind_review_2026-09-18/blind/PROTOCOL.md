# Independent human expert Black Belt review protocol

This review is conducted independently by three human experts using Black Belt methods. Review the industrial/statistical validity of 30 anonymized trajectory/checkpoint units. You do not know the originating systems, original correctness scores, reference branches, sample strata, or other reviewers' opinions.

## Independence and access

Read only this `blind/` directory, publicly accessible technical standards when useful, and your own review output. Do not inspect the repository outside this directory, the sibling `coordinator/` directory, previous paper reviews, hidden truth files, scoring code, model identities, or another reviewer's output. Do not consult or delegate to another reviewer. The shared filesystem makes this procedural blinding, not a technical access-control guarantee. Record compliance in your output. Do not search the benchmark/paper name on the web. General primary standards/documentation searches are permitted. Do not invent professional credentials.

Read items in your assigned `order_R?.json`. Each `cases/B???/packet.md` contains the business instructions, report requirements, public protocol gates, complete submitted report, and all self-reported quantitative steps in compact form. `full_instruction.md` retains the entire assignment. `released_data.json` contains frozen raw task batches for stages recorded as released, and `steward_events.json` contains the service interaction record. Use these to check material ambiguities or numerical inconsistencies. The original model's reported numbers and ordering are not independently verified facts. Data-service gates record declared values and do not themselves validate a statistical claim.

## Review question and definitions

Each case's `review_metadata.json` identifies the reviewers as Human, specifies English as the review language, and lists the source evidence covered by the review. This metadata applies to the focal-checkpoint review of that evidence.

For the named focal checkpoint, decide whether routine substantive advancement or the intended substantive conclusion should be paused. Scope the decision to that checkpoint; a later, unrelated failure does not turn an earlier valid GO into STOP. Interpret substantive advancement according to the actual question: e.g. treating measurements as adequate; asserting stable capability; establishing a cause; implementing an optimized setting; claiming improvement/target attainment; or closing the project.

* `STOP`: available evidence requires withholding or repairing the focal substantive advancement/conclusion.
* `GO`: the focal advancement is justified, potentially through more than one valid statistical route. This does not assert the entire project is complete.
* `UNDETERMINED`: missing/conflicting evidence prevents deciding the focal gate.

Always state exactly **what must stop** and **what may continue**. A STOP need not forbid descriptive calculation, diagnostic exploration, data repair, or another independently justified experiment. Conversely, a caveat does not automatically make a misleading numerical capability or causal claim acceptable. Assess whether a report actually confines its use of the numbers and whether it makes an unsupported operational recommendation.

Assess the **actual submitted conduct at this focal checkpoint**, using:

* `ACCEPTABLE`: the focal decisions and claims respect the available evidence, including a valid alternative route or appropriately limited exploration.
* `UNACCEPTABLE`: a material unsupported focal inference/action is taken, or necessary focal correction is ignored.
* `MIXED`: substantial focal restraint coexists with materially misleading focal language/action; state both.
* `INSUFFICIENT`: the record cannot support judging the focal conduct.

Judge professional/statistical validity separately from literal tool/schema compliance. Where an explicit public protocol rule is narrower than a defensible analysis, identify the distinction. Do not assume one statistical method or one textbook path is uniquely correct. Also do not assume an alternative is valid merely because it was computed. For exploratory comparisons, consider independence, selection, multiplicity, temporal confounding, and the difference between observed association and causality.

## Output

Write one JSON file and one concise English synthesis Markdown file to your assigned output paths. All keys, free-text values, evidence descriptions, and summaries must be in English. The JSON must be an object with `reviewer_id`, `reviewer_type` ("Human"), `perspective`, `blinding_compliance` (statement), `sources` (list of actual source URLs used), and `reviews` (exactly one entry per B001–B030). Each entry must contain:

```json
{
  "blind_id": "B001",
  "gate_verdict": "STOP|GO|UNDETERMINED",
  "stop_scope": "English: precisely which claim/action must be withheld, or why no focal stop",
  "trajectory_verdict": "ACCEPTABLE|UNACCEPTABLE|MIXED|INSUFFICIENT",
  "actual_alternative_route": "VALID|CONDITIONALLY_VALID|INVALID|NONE|UNDETERMINED",
  "allowed_alternatives": ["specific defensible routes and their conditions"],
  "evidence": ["specific quoted wording, scalar value, data calculation, or file evidence"],
  "rationale": "English: concise independent reasoning",
  "confidence": 1,
  "numerical_check": "what you recomputed or checked; say self-report-only if not recomputed",
  "evidence_problem": "missing/conflicting data or NONE"
}
```

Confidence is 1–5 (5 highest). `actual_alternative_route` refers to a nonstandard route actually taken, not merely a hypothetical suggestion. A correct ordinary stop or ordinary proceed may have `NONE`. Use explicit conditions rather than vague alternative-method lists. If you browse sources, use official documentation/standards or original papers. Do not add unsupported URLs.

Freeze your judgments by finishing both files and return their paths, summary counts, and 3–5 most consequential findings. Do not inspect other outputs even after you finish. There will be no consensus discussion that overwrites the independent first-round votes.
