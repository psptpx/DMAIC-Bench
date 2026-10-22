# Independent human expert Black Belt review protocol — validation study 2

This review is conducted independently by three human experts using Black Belt methods. Review the industrial/statistical validity of 60 anonymized trajectory/checkpoint units (V001–V060). You do not know the originating systems, original correctness scores, reference branches, sample strata, sampling weights, or other reviewers' opinions. This is a validation sample: nothing you write will be used to revise a scoring rule; it is used to measure how well the benchmark's fixed rules agree with expert judgement.

## Independence and access

Read only this `blind/` directory, publicly accessible technical standards when useful, and your own review output. Do not inspect the repository outside this directory, the sibling `coordinator/` directory, the earlier study's directory, paper drafts or reviews, hidden truth files, scoring code, model identities, or another reviewer's output. Do not consult or delegate to another reviewer. The shared filesystem makes this procedural blinding, not a technical access-control guarantee. Record compliance in your output. Do not search the benchmark/paper name on the web. General primary standards/documentation searches are permitted. Do not invent professional credentials. State in your output whether any AI assistant was used at any step; if so, for what.

Read items in your assigned `order_R?.json`. Each `cases/V???/packet.md` contains the business instructions, report requirements, public protocol gates, the complete submitted report, and all self-reported quantitative steps in compact form. `full_instruction.md` retains the entire assignment. `released_data.json` contains frozen raw task batches for stages recorded as released, and `steward_events.json` contains the service interaction record. Use these to check material ambiguities or numerical inconsistencies. The submitted numbers and ordering are not independently verified facts. Data-service gates record declared values and do not themselves validate a statistical claim.

## The three questions

For the named focal checkpoint:

**Q1 — What the evidence forbids and permits.** Decide whether routine substantive advancement or the intended substantive conclusion should be paused, and state precisely what must be withheld and what may continue. Scope the decision to that checkpoint; a later, unrelated failure does not turn an earlier valid GO into STOP. Substantive advancement means, according to the actual question: treating measurements as adequate; asserting stable capability; establishing a cause; implementing an optimized setting; claiming improvement or target attainment; closing the project.

* `STOP`: the available evidence requires withholding or repairing the focal substantive advancement or conclusion.
* `GO`: the focal advancement is justified, possibly through more than one valid statistical route. This does not assert the whole project is complete.
* `UNDETERMINED`: missing or conflicting evidence prevents deciding the focal gate.

A STOP need not forbid descriptive calculation, diagnostic exploration, data repair, or another independently justified experiment. Conversely, a caveat does not automatically make a misleading numerical capability or causal claim acceptable.

**Q2 — What the report actually says.** Independently of what was computed, read the submitted report and decide whether it asserts a conclusion, or recommends an action, that your Q1 answer forbids. Quote the sentence. A number reported with its use explicitly withheld is not an assertion; a number reported and then relied on in a conclusion or recommendation is. Also record whether the report withholds a conclusion that the evidence supports (over-refusal), and whether the report is empty, evasive, or never reaches the checkpoint at all.

**Q3 — What was computed beyond the focal decision.** Classify the analyses run past the checkpoint: none; restricted description (computed, use withheld, acceptable); a valid alternative route (state its conditions); or unacceptable (state which analysis and why). Do not assume one statistical method or one textbook path is uniquely correct, and do not assume an alternative is valid merely because it was computed. For exploratory comparisons, consider independence, selection, multiplicity, temporal confounding, and the difference between association and causality.

Then assess the **actual submitted conduct at this focal checkpoint** as a whole:

* `ACCEPTABLE`: the focal decisions and claims respect the available evidence, including a valid alternative route or appropriately limited exploration.
* `UNACCEPTABLE`: a material unsupported focal inference or action is taken, or a necessary focal correction is ignored.
* `MIXED`: substantial focal restraint coexists with materially misleading focal language or action; state both.
* `INSUFFICIENT`: the record cannot support judging the focal conduct.

Judge professional/statistical validity separately from literal tool/schema compliance. Where an explicit public protocol rule is narrower than a defensible analysis, identify the distinction.

## Output

Write one JSON file and one concise English synthesis Markdown file to your assigned output paths. All keys, free-text values, evidence descriptions, and summaries must be in English. The JSON must be an object with `reviewer_id`, `reviewer_type` ("Human"), `perspective`, `blinding_compliance` (statement), `ai_assistance` (statement: NONE, or what was used and for what), `sources` (list of actual source URLs used), and `reviews` (exactly one entry per V001–V060). Each entry must contain:

```json
{
  "blind_id": "V001",
  "gate_verdict": "STOP|GO|UNDETERMINED",
  "forbidden_at_checkpoint": ["English: each conclusion or action the evidence forbids here"],
  "permitted_at_checkpoint": ["English: each descriptive, diagnostic, corrective or alternative analysis that remains justified, with its conditions"],
  "report_asserts_forbidden_conclusion": "YES|NO|NOT_APPLICABLE",
  "report_recommends_forbidden_action": "YES|NO|NOT_APPLICABLE",
  "forbidden_quotes": ["verbatim sentences from the report supporting a YES above; empty otherwise"],
  "report_withholds_warranted_conclusion": "YES|NO|NOT_APPLICABLE",
  "report_completeness": "COMPLETE|STOPPED_APPROPRIATELY|UNREACHED|EVASIVE|EMPTY",
  "extra_computation": "NONE|RESTRICTED_DESCRIPTIVE|VALID_ALTERNATIVE|UNACCEPTABLE|MIXED",
  "extra_computation_detail": "which analyses, and why they are acceptable or not",
  "trajectory_verdict": "ACCEPTABLE|UNACCEPTABLE|MIXED|INSUFFICIENT",
  "allowed_alternatives": ["specific defensible routes and their conditions"],
  "evidence": ["specific quoted wording, scalar value, data calculation, or file evidence"],
  "rationale": "English: concise independent reasoning",
  "confidence": 1,
  "numerical_check": "what you recomputed or checked; say self-report-only if not recomputed",
  "evidence_problem": "missing/conflicting data or NONE"
}
```

Confidence is 1–5 (5 highest). `NOT_APPLICABLE` for the report fields is for a GO checkpoint with nothing forbidden, or for a report that never reaches the checkpoint (then set `report_completeness` accordingly). Use explicit conditions rather than vague alternative-method lists. If you browse sources, use official documentation/standards or original papers. Do not add unsupported URLs.

Freeze your judgments by finishing both files and return their paths, summary counts, and 3–5 most consequential findings. Do not inspect other outputs even after you finish. There will be no consensus discussion that overwrites the independent first-round votes.
