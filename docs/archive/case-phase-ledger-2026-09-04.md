# DMAIC phase-completeness ledger — the source corpus versus the authored benchmark

**Date:** 2026-09-04 · **Type:** read-only survey (no benchmark file was modified) ·
**Subject:** the private corpus of completed Six Sigma project reports the expert-derived cases
were authored from, and `dmaic_bench/cases/*/case.yaml`.

> **Read this first — what a reader of the public release can and cannot check.**
>
> The corpus surveyed here is **not published and is not part of this repository**. It is a
> private collection of completed Six Sigma project reports held by the authors; it carries no
> redistribution grant, and the nine benchmark cases derived from it are exactly the nine held
> out of the public release (`adb_c03 c05 c07 c08 c10 c15 c16 c19 c20` — see
> [`HELD_OUT.md`](../HELD_OUT.md)). **None of the per-document evidence below is verifiable from
> this repository.**
>
> This version of the survey is de-identified. Every organisation, product, plant, brand,
> person, project title, source filename, internal document number and charter identifier has
> been removed, and per-document evidence quotations have been replaced by a description of the
> artifact's *shape* — the column set of a control plan, the structure of a goal-derivation
> rule, the form of a COPQ formula. That is deliberate rather than incidental: the shape is
> what the benchmark design needed from this survey, and the figures inside a real deck are the
> part that could re-identify it. Projects are referred to by an opaque survey id (`P01` …)
> that exists only inside this document, and **no project is mapped to a benchmark case id**,
> because such a mapping would tie a held-out case to an identifiable organisation.
>
> Benchmark-side figures **are** checkable, and the reproducible public-tree census is given
> alongside the development-corpus one in §0.

## 0. The question this survey answers

An earlier pass asked *"how much of this corpus is extractable at all?"* and answered with
extraction tiers plus a method-coverage census. This pass asks a different question:

> The benchmark built from this corpus grades only Measure / Analyze / Improve. Do the **real**
> project reports contain gradeable **Define** and **Control** content that the benchmark simply
> failed to author?

**Answer: yes, overwhelmingly — and the most telling evidence is that the benchmark already had
that content in hand.** Every one of the eight source decks the expert-derived cases were built
from carries a quantified Define phase, six of the eight carry a quantified Control phase, and
*none* of them contributed a single Define or Control stage to the benchmark.

### The benchmark side, measured (not assumed)

Counted directly from the case files of the **full 24-case development corpus** as it stood
when this survey ran (27 case directories at the time, counting the frozen bridge cases the
public release does not carry):

| | define | measure | analyze | improve | control |
|---|---|---|---|---|---|
| stages | **1** | 49 | 70 | 27 | 11 |
| stage-tagged truths | **0** | 6 | 23 | 5 | 5 |
| decision points | **0** | 26 | 8 | 6 | **0** |

The single `define` stage in the whole corpus was `adb_c09/Q_Profile`, whose method is
`meta.data_profiling` — a data-shape inspection, not a charter, a baseline, a goal derivation or
a COPQ. The `control` stages in the native case files were a binomial-capability call and a
c-chart call: *computations that happen to be labelled control*, with no control plan, no
reaction rule and no before/after confirmation.

**The public tree today, which a reader can re-run.** The Define and Control work this survey
argued for has since been designed
([`define-phase-design-2026-09-04.md`](define-phase-design-2026-09-04.md),
[`control-phase-design-2026-09-04.md`](control-phase-design-2026-09-04.md)) and one worked case
(`adb_c24`) authored, so the numbers above are the *before* picture and no longer describe this
repository. Over the 15 published cases, at seed 1:

| | define | measure | analyze | improve | control |
|---|---|---|---|---|---|
| stages | 3 | 17 | 27 | 8 | 4 |
| stage-tagged truths | 3 | 25 | 38 | 10 | 7 |
| decision points | 1 | 4 | 6 | 2 | 1 |

```python
from collections import Counter
from dmaic_bench.core import registry
st, tr, dp = Counter(), Counter(), Counter()
for case in registry.discover().values():
    phase = {s.stage_id: s.phase for s in case.meta.stages}
    for s in case.meta.stages:
        st[s.phase] += 1
    for t in case.generate(1).truths:
        if phase.get(t.stage_id):
            tr[phase[t.stage_id]] += 1
    for d in case.meta.decision_points:
        ph = phase.get(getattr(d, "stage_id", None)) or getattr(d, "phase", None)
        if ph:
            dp[ph] += 1
```

The published Define stages are `adb_c09/Q_Profile` and `adb_c24/D_Charter` + `adb_c24/D_Scope`;
the published Control stages are `adb_c12/P_BinomialCap`, `adb_c17/AC_C`,
`adb_c24/C_Released` and `adb_c24/C_Confirmation`. All four cases are in the public split.

### The eight source decks the expert-derived cases were built from

Held out, and therefore not inspectable here. Source documents, organisations and project
titles are omitted; the phase columns are stage counts in the benchmark case as authored.
Eight of the nine held-out cases appear; `adb_c16` was not among the decks this survey
read, and no claim is made about it here.

| case | split | provenance | D | M | A | I | C |
|---|---|---|---|---|---|---|---|
| `adb_c03` | held out | RECONSTRUCTED | **0** | 7 | 4 | 5 | **0** |
| `adb_c05` | held out | RECONSTRUCTED | **0** | 7 | 2 | 1 | 1 |
| `adb_c07` | held out | RECONSTRUCTED | **0** | 3 | 6 | 3 | **0** |
| `adb_c08` | held out | RECONSTRUCTED | **0** | 3 | 4 | 2 | 1 |
| `adb_c10` | held out | RECONSTRUCTED | **0** | 2 | 5 | 3 | **0** |
| `adb_c15` | held out | TRUE | **0** | 2 | 2 | 2 | **0** |
| `adb_c19` | held out | TRUE | **0** | 5 | 6 | 1 | **0** |
| `adb_c20` | held out | RECONSTRUCTED | **0** | 2 | 4 | 1 | 1 |

One of these source decks — the richest of the eight — contains a signed project charter with a
baseline / target / benchmark triple, a written goal-derivation rule, a monetised benefit
estimate, an AIAG-style control plan, individuals charts with recomputed limits on five key X's,
a second FMEA, a multi-site rollout and a signed handover log. The benchmark's version of it
has twelve stages, every one of them M / A / I. **The Define and Control content was not
missing from the source — it was dropped in authoring.**

## 1. Corpus accounting

Extraction reused the existing corpus tool unchanged and extended only its *coverage*: it was
run over the whole tree rather than the one sub-directory the tool's own constant pointed at,
so two industry sub-directories and eleven root-level decks had never been surveyed before.
(The tool and the corpus live together, outside this repository.)

| location | documents | text extracted | blocked legacy `.ppt` |
|---|---|---|---|
| main case directory | 95 | 56 | 39 |
| mechanical-industry sub-directory | 18 | 5 | 13 |
| electronics-industry sub-directory | 24 | 8 | 16 |
| root-level decks | 11 | 11 | 0 |
| **total** | **148** | **80** | **68** |

Of the 80 that parsed, 5 produced zero text and 1 produced 22 characters → **74 documents with
usable text**, collapsing to **~60 distinct projects** after de-duplication (§5.2).

Every deep read was done against the full extracted text, every number quoted in the private
survey was re-verified against its source file, and every formula was recomputed (§4 records
which reproduce and which do not).

## 2. The ledger

`auth` answers: could a task be authored that grades **all five** phases?
**3** = every phase has at least one checkable number *and* at least one decision ·
**2** = D or C has numbers but no decision · **1** = D/C narrative only ·
**0** = not a single-project report.

Sector uses the benchmark's four coarse buckets (`process_industry`, `electronics`,
`discrete_manufacturing`, `services`), which is also the only industry granularity a public case
file may carry — a fine-grained sector label puts a real case in a cell of size one.

### Tier 3 — all five phases gradeable

| id | sector | project Y | Define evidence | Measure / Analyze / Improve | Control evidence | auth |
|---|---|---|---|---|---|---|
| P01 | electronics | final-inspection defect rate | charter baseline/target/benchmark triple; written goal rule (close ≥ 50 % of the gap to the benchmark); SIPOC; VOC→CTQ; monetised benefit | attribute MSA, binomial capability (Cpk / Z / PPM), FMEA; chi-square, DOE, OLS, two-sample t; response optimiser, chi-square before/after, Z improvement | AIAG control plan with a reaction column; individuals charts with recomputed limits on five key X's; second FMEA; 16 numbered standard documents; multi-site rollout; signed handover log; closing rate against the charter target | 3 |
| P02 | discrete_manufacturing | assembly yield | charter; baseline / target / entitlement; SIPOC; VOC→CTQ; scoping Pareto with cumulative %; **multiplicative goal derivation** (Y = Y1·Y2·Y3 ≥ target) with a per-step Z target; COPQ formula | attribute MSA, Fleiss κ, binomial Z, FMEA; t-test, two-proportion Z, ANOVA, quadratic OLS; 2² factorial, optimiser, validation t | control plan (spec + method + owner); three-step reaction plan; **phased p-charts per process step** with recomputed limits; SOPs; closure against target; reconciled benefit | 3 |
| P03 | process_industry | per-unit defect rate | charter triple; goal rule = *best performing sister line*; SIPOC; VOC counts; COPQ formula that recomputes exactly | GRR with ndc, capability (Cpk / Z / σ), sources of variation, FMEA; one- and two-way ANOVA, Bartlett, Anderson–Darling; polynomial OLS, factorial, central-composite RSM, optimiser | control plan with a setpoint ± tolerance and an SPC sampling plan; Xbar-R **and** Xbar-S on named X's with limits; reaction rule; KPI handover; rollout; σ before/after | 3 |
| P04 | electronics | annual defect rate (ppm) | charter; baseline / target / benchmark in ppm; Kano→CTQ; SIPOC; scoping Pareto; **COPQ formula that recomputes to the last digit** | attribute MSA; a Pareto→C&E→FMEA factor funnel (101 → 24 → 15); Z and sigma level; chi-square, two-proportion, one-sample t; quick wins, DOE + OLS, Cpk against a 1.33 gate | 15-row control plan (process / input / output / control standard / control method / inspection frequency / sample size / action plan / owner); reaction rule; 15 numbered standard documents; cross-unit rollout; closing ppm; realised benefit | 3 |
| P05 | discrete_manufacturing | field loss rate | project registration record; baseline; SIPOC; SWOT plus a loss ranking; Pareto; COPQ formula | Fleiss κ ×2, a 65 → 27 → 16 factor funnel, FMEA; chi-square, a double-ratio test, Fisher exact, t-test; 5W1H, DOE, desirability, Cpk | 16-item control plan; 16 standardised files; a design checklist and a process checklist with point counts; multi-unit rollout; closing rate with an attainment percentage; realised benefit | 3 |
| P06 | process_industry | fuel cost per unit produced | Pareto over spend; Y definition; **goal-derivation table with the arithmetic shown**, ending in an annual saving | I-MR baseline (the source itself calls the baseline period "too variable"), process map; fishbone, weighted C&E, FMEA, ANOVA, Bartlett, AD normality; 2³ DOE, optimiser desirability, two-proportion Z | control plan organised around *change*: before-control method / after-control method / standard-document number / owner / due date / attainment status; escalation ladder ("first a warning, then a penalty"); I-MR with limits and its MR chart; monthly trend against target; **actual-versus-projected financial reconciliation whose formula reproduces exactly** | 3 |
| P07 | discrete_manufacturing | quality loss (ppm) | formal DMAIC charter worksheet with a stakeholder matrix; baseline → target in ppm; ppm↔sigma conversion for two markets; an FMEA-RPN scope gate (which factors are in, which is out); quality-cost table; monetary goal | %R&R against a 10 % gate, data-collection tables; one-sample t, chi-square on gauge damage; a Cpk decision across three setting strategies against a 1.33 gate; gauge poka-yoke | tolerance written into the control plan; training text quoted verbatim; an X-R chart over 25 subgroups with the raw data present (limits not quoted); itemised savings | 3 |
| P08 | discrete_manufacturing | rework rate on a mechanism | charter with an expected financial benefit; baseline → target under an explicit *80 % improvement* rule; attribution-based scoping; loss formula | chi-square baseline homogeneity, attribute GRR (repeatability / reproducibility split); fishbone, binary logistic regression, a numeric threshold on one X; fractional-factorial DOE, FMEA RPN before/after | **a control plan that assigns a different chart type per characteristic** — p-chart for the attribute Y, IX-MR for a continuous X — each with its own Z signal threshold and a named reaction owner; p-chart and I-MR limits; DPMO before/after; planned versus actual benefit | 3 |
| P09 | discrete_manufacturing | assembly defect rate | SIPOC; VOC with a customer-stated acceptable level; CTQ; baseline → target; **COPQ fully derived, and the sub-formula recomputes exactly** | a 78-factor C&E, FMEA/RPN, data plan; capability on an incoming material property, chi-square on operator (correctly non-significant), comparative process trials; spec tightened, torque standardised, supplier SPC | **10-column AIAG control plan** (equipment/process check · characteristic · specification · measurement method · sample size · sampling frequency · who measures · where it is recorded · corrective action · reference document; 9 rows); red-flag escalation; Xbar-S plus a p-chart with limits; 4 new work instructions; closing rate | 3 |
| P10 | electronics | solder-void defect rate | four-box charter (business case in money, goal, problem statement); VOC (an internal customer complaint) → CTQ; SIPOC; Pareto; a **negative** baseline Cpk | GRR, variance decomposition, normality, I-R chart, capability; C&E matrix, 2⁶⁻³ screening DOE; full four-factor factorial with centre points, ANOVA plus lack-of-fit | control plan per key X with setpoint, owner and date; I-R chart on the response; MSA re-verification; Cpk before/after; rollout to two further models; realised versus projected benefit | 3 |
| P11 | process_industry | packaging weight (green-belt project) | VOB/VOC (5 of 30 complaints); SIPOC; CTQ tree; Y; baseline as a potential extra cost plus a weight spread; goal plus stretch goal; COPQ formula | MSA %P/TV, %P/T and ndc ≥ 5; Cpk < 1; C&E matrix → Pareto of the vital few; FMEA, quick win, second FMEA; full factorial, curvature test then refit, lack-of-fit, OLS, optimiser, 95 % CI on the optimum | **control-plan table** (X · Y characteristic · X specification · measurement method · sample size · sampling frequency · control method · responsible department · recommended action) and a **standardisation table** (process · improvement · previous problem · new method · new standard document with revision · trainer · trainees · effective date); a control chart with no rule violation; a Cpk gate; realised benefit | 3 |
| P12 | discrete_manufacturing | DPMO on two Y's | charter with role-assigned owners; DPMO and sigma baselines for both Y's; **an explicit 70 %-improvement goal cascade** with a separate challenge value; itemised COPQ and the savings it implies | process flowchart, fishbone, C&E, FMEA, crossed GRR (%contribution), normality, capability; Pareto over process steps (two steps = 89.5 %), fishbone on the top four; FMEA update, countermeasures, post-improvement capability in ppm and sigma | nine named control and check documents; I-MR charts on both Y's (limits not in the text); a **5W2H reaction framework** with a warning-limit trigger; SOPs and a monthly training-hours commitment | 3 |
| P13 | process_industry | compressive strength | VOC across three customer groups; CTQ; **a numeric goal derived from a published national standard** — a σ ceiling and a target window, with the standard cited | Xbar chart with limits and one out-of-control point, long-term capability with DPMO; fishbone five-factor screen; 5×2 full factorial over 32 runs with a factor-difference ranking | post-improvement Xbar chart; **Cp, DPMO and σ all three quoted before and after**; standardisation citing three further national/industry standards including a curing specification (temperature ± tolerance, minimum relative humidity); monetised saving | 3 |
| P14 | discrete_manufacturing | machine daily output | charter template; VOC/VOB → CTQ; problem statement with numbers (an output gap, an outsourcing share, a lead time); baseline / target / benchmark for two lines; COPQ formula | attribute MSA over two rounds (fail, retrain, re-run), I-chart with limits, macro process map; C&E funnel, FMEA RPN, t-test, F-test, Levene, changeover Pareto; six-factor 67-run DOE, ANOVA, reduced model, prediction equation | **full control plan** (changeover and normal-production rows, each with a numeric specification, a named chart type and a reaction rule); 7 dated SOPs; poka-yoke table. *No capability index anywhere in the document, and the closing financial figure is masked by the author* | 3 |
| P15 | electronics | instrument accuracy at a stated condition | charter with a **numeric capability commitment** as the goal; VOC→CTQ; explicit SIPOC; problem statement (return rate versus the norm); baseline Cpk; COPQ formula | GRR fails a 30 % gate → fixed → re-run and passes; two-level full factorial across two subassemblies, main-effects plot; supplier deviation binning, compensation, an added inspection station | standardisation (revised material specification, supplier contract, work instructions); GRR re-verification; Cpk before/after; **an F-test on the before/after variance**; an Xbar-R chart judged in control | 3 |
| P16 | discrete_manufacturing | first-pass yield, rough machining | SIPOC; milestone plan with dates; scrap breakdown; baseline → target derived against a single-step rate; COPQ formula | GRR, P/T, capability (Pp / Ppk / Cp, two of them negative), per-step yields, C&E matrix; two-sample t → "the process plan must change"; two-factor DOE, ANOVA, desirability — **the optimum is deliberately overridden** for machining-allowance reasons | an explicit target-attainment check by sampling (38 sampled, 35 pass = 92.1 % against a 90 % target), plus ppm and sigma. *No control chart and no standardisation section, and the closing money figure is a clean 10× inconsistent with Define's* | 3 |
| P17 | discrete_manufacturing | surface-roughness capability | VOC with an audit count; CTQ specification window; baseline Cpk; target; benchmark; COPQ formula; net benefit after cost | crossed GRR with the repeatability/reproducibility split; three one-way ANOVAs — two non-significant, one significant — plus an empirical linear model; tooling change, standardised measurement point, operator training | itemised control plan (characteristic · sampling frequency · measurement instruction · parameter control · per-batch tooling inspection); SPC and Cpk tracking over a date range; Cpk before/after against the target; net benefit | 3 |
| P18 | electronics | on-line qualification rate | CTQ; baseline rate and sigma level; target; scoping by ticket share. *Financial figures masked by the author* | crossed GRR before/after in two laboratories with ndc, runs test, normality, paired t; four candidate root causes verified descriptively; four countermeasures, FMEA RPN reduction | process standardisation (incoming inspection plus a return/replacement flow); dated work instructions; tracking of the qualification rate; sigma before/after and the final rate against target | 3 |
| P19 | electronics | crimping quality | prose charter: baseline rate and ppm, annual loss, target rate and ppm, projected saving, team table | attribute MSA before/after, a 32×3×2 study design; fishbone across five defect modes, capability on a continuous X with limits, normality, **an individuals-chart rule violation quoted by rule name**; three narrative countermeasures | key-X process control with a corrective-action plan; an individuals chart judged to be in statistical control; standardisation into documents; ppm before/after | 3 |
| P20 | electronics | soldering DPMO / first-pass yield | **the most complete charter in the corpus**: current process capability in DPMO and sigma, opportunity count per unit, FPY, the VOC→CTQ derivation quoted in full, a target expressed as a sigma move within six months, a training and equipment budget, team size, projected benefit | discrete GRR against an 85 % gate, rational subgrouping over 7 factors, a baseline p-chart with a mean and a range; GLM / mixed ANOVA; a 15-factor Plackett–Burman screen → 3 factors, full-factorial GLM, factorial plot, 24-sample verification | p-chart on the optimised process with every point inside the limits and the DPMO range narrowed by roughly 60×; FPY tripled; rework staffing cut; scrap and QA rework reduced; realised versus projected benefit. *The source elides the chart image itself* | 3 |
| P21 | electronics | potting rework rate | charter with a monthly cost table; VOC (repeat customer complaints) → CTQ; scoping by volume share; baseline rate; a near-term and a long-term goal, each split into "visible" and "needing repair"; projected annual benefit | attribute MSA 3×30×2 against a 75 % gate; fishbone, FMEA RPN; Taguchi L9(3⁴) → a named best combination and the single most significant factor | control plan (three itemised rule changes written into the process documents); training; actual versus target rate; **actual versus projected benefit, agreeing to within 0.2 %**. *No control chart* | 3 |
| P22 | discrete_manufacturing | bore-diameter defect rate | project background with a sponsor role; a monthly defect table; baseline; a **zero** target; the drawing tolerance. *No COPQ anywhere — unlike its sibling deck from the same corporate template (P17)* | GRR, fishbone, process flow with X's and Y's, C&E matrix (36 factors → the 14 above a score threshold), FMEA; one-way ANOVAs (one non-significant, one significant), Pearson correlation, a time-series tool-wear analysis giving a re-tool interval; allowance change, fixed tool-change interval, poka-yoke honestly reported as not yet done | standardisation list (2 work instructions, an FMEA update, a new inspection programme); **a reaction plan with an explicit threshold and a sampling delay** ("sample 30 minutes after start-up; if the result exceeds the stated band, notify the operator to adjust and re-inspect until conforming"); SPC tracking showing the saw-tooth tool-wear cycle; defect rate at zero for two consecutive months | 3 |
| P23 | process_industry | prime-product rate | target stated as a band ("from under X % to over Y %"); five named root causes | thin — the document is in journal-article form; cause analysis across five factor groups; process changes | prime-product rate and a secondary scrap ratio both quoted before and after | 3 |
| P24 | electronics | scrap rate (ppm) | goal slide with a baseline and a target in ppm, a project window, a team including finance, and a Gantt | monthly output/scrap table, Pareto with cumulative %; two fishbones, a sub-Pareto, **four full FMEA tables with S/O/D/RPN**; an orthogonal 3×3 DOE with six replicate responses per run and a **full ANOVA table (SS/df/MS/F/p)** → a named best combination | control points (process-parameter document update, weekly maintenance document, annual training plan) plus a **post-improvement monthly ppm series** that reaches the target, and a 12-month saving | 3 |
| P25 | electronics | imaging process capability | **goal derived from a sigma level** — "raise to 4 sigma, i.e. Cp = Cpk = 1.33" — for two characteristics | baseline Cp/Cpk on line width and on position in X and Y, all below 1.0 → an explicit equipment-calibration decision; capability-driven root cause; DOE on line width | after-values of Cp and Cpk on both characteristics; an Xbar-R chart judged in control; the same method extended to the position tolerance | 3 |
| P26 | services | first-call resolution | baseline as a three-month mean with its standard deviation; a target above it | FCR measurement definition; root-cause analysis; process changes | mean shifted past the target and the standard deviation reduced, both quoted; six-month tracking, then hand-off to routine operations | 3 |
| P27 | *(pedagogical exercise — see §5.4)* | satisfaction score | VOB/VOC quoted; CTQ; macro process map; baseline mean / sd / sigma level; goal mean / sd / sigma level; entitlement; COPQ | GRR/ANOVA with acceptance criteria (%contribution < 10 %, %study variation < 30 %, ndc > 5), C&E, Pareto, a negative baseline Cpk; five two-sample t-tests, **one correctly retained as a non-driver**; full factorial plus OLS with an interaction term, optimiser, Cpk | control-plan table (factor · standard before / after · owner · date); **Xbar-R on the Y and on every X, all with numeric limits**; final Cpk and Ppk; sigma before/after | 3 |
| P28 | electronics | gap defect rate — **⚠ self-declared fictional (§5.1)** | charter D1–D6; baseline ppm; Pareto; goal and stretch goal; COPQ formula | GRR ANOVA per sub-assembly, capability per characteristic, AD normality; multi-vari, ANOVA, Levene, chi-square; 2² factorial for both mean and sigma plus a star-point RSM, Cpk before/after | **the single most complete Control section in the corpus** — control plan with setpoint ± tolerance and owners; IX-MR on a process X with limits; p-chart on the Y with limits; Ppk re-confirmation over a stated window; **a two-proportion before/after test on the Y itself**; a monthly trend; an annualised benefit | 3* |

### Tier 2 — D or C has numbers but no gradeable decision

| id | sector | project Y | why it stops at 2 |
|---|---|---|---|
| P29 | electronics | cosmetic defect rate | Full charter, roles, an eight-phase Gantt, SIPOC, VOC/CTQ, a scoping Pareto, a baseline rate and a monetised loss — **but the charter's own baseline and target are masked by the author**. Rich M/A/I (κ MSA with an explicit retraining rule, C&E + FMEA funnel, paired t, chi-square, 2³ DOE + RSM). Control has a 9-item standardisation and rollout list, Cpk before/after and a no-side-effect check, but **no control chart, no limits and no reaction rule** |
| P30 | electronics | parallelism and position capability | Charter as narrative with a 150-day schedule, a VOB-based project-selection rule, SIPOC, specifications and a Cpk goal — but no baseline capability inside Define and no Pareto. Control names an Xbar-R plan on two Y's at a stated frequency, an abnormality-reaction flow and document standardisation, **but the limits are explicitly deferred** ("control to specification for now; limits to be set after a month of collection") |
| P31 | electronics | component drop-off rate | The Define slides exist (team / plan / target) but their table content was lost by the extractor of the day; the recovered text still lacks the numeric target. Strong M/A/I (capability by adhesive brand at two temperatures, a redesign, a hypothesis test, a pilot scale-up, a full-factorial DOE). Control plan **recovered only by table-aware extraction** (item · object of improvement · corresponding document · responsible unit · responsible person · location · control period), plus a financial section and a rollout decision |
| P32 | services | outpatient flow (healthcare) | Charter with eight work-streams but no numbers; VOC survey with n; waiting time as a share of visit time; a capacity gap; rich baselines with means ± sd — **but no numeric target was ever set**. Analyze is takt analysis, value/non-value classification, fishbone and a measurement-selection matrix. Control has three operating manuals, an I-MR named on a daily workload (no limits) and **seven before/after significance tests with exact p-values**, one of them honestly non-significant |
| P33 | discrete_manufacturing | printing defect rate | QFD-style VOC→CTQ tree with importance scores, a complaint rate, a monetised loss, a baseline, and a project-selection Pareto containing **an explicit decision to drop the higher-scoring candidate project** on cost grounds. Attribute GRR; a baseline p-chart over 25 subgroups giving ppm and sigma; defect Pareto; fishbone; Pearson r and OLS; FMEA; an 18-run full factorial. Control reports a post-improvement p-chart and a capability table with ppm and sigma before/after and a complaint/loss reduction — but **no control plan, no limits, no reaction rule and no threshold check** |
| P34 | discrete_manufacturing | leak rate | A complaint Pareto driving an explicit scope narrowing to one failure mode, and a baseline Cpk the source itself calls inadequate — but **no numeric target and no COPQ**. Analyze is unusually physical: destructive tensile and bend tests, a weld-preparation comparative trial, metallography, a bubble Pareto, and a two-level three-factor DOE. Control has a welding standardisation document with quoted parameters (gas purity, front and back flow rates ± tolerance, pulse mode), a "fixed person / fixed machine / fixed process" rule, a supplier quality agreement, a tensile monitoring log and field leak rates before/after. The source honestly concedes the result is not at a Six Sigma level |
| P35 | discrete_manufacturing | delivery cycle time | Narrative charter plus a milestone chart; VOC named as a method only; baseline first-time yield and scrap; a goal expressed as a cycle-time band and a yield target; a monetised benefit. Analyze names VSM, cycle-time analysis, MSA, hypothesis testing and regression **with no results quoted**; twelve sub-project action plans; WIP visual management. Control has a project control-plan table (key factor · improvement method · control method · completion date), a time-series chart of the delivery cycle against the target band, institutionalisation and replication across many product models. It **honestly reports missing one target while beating the other** — but has no limits, no capability index and no significance test |
| P36 | electronics | fit defect rate | Pareto of failure modes with cumulative %, a baseline pass/fail batch count, an average defect rate, two DPPM figures, a numeric goal and a COPQ formula. Process mapping, FMEA to a high RPN, GRR, an XY matrix ranking eight factors down to four. Control is headed **"next actions"** — forward-looking rather than closed: a weekly defect-count chart with limits (one of them negative and left uncorrected), an incoming-inspection standard, a special work instruction and a measurement fixture institutionalised. **No closed control plan, no capability index, no significance test** |
| P37 | electronics | module defect rate | No charter, VOC or SIPOC; a baseline rate against a required rate, a baseline Cpk, and a defect Pareto with an **explicit 80/20 vital-few decision**, plus a new standard expressed as both an average and a UCL ratio. *No COPQ anywhere.* Control re-runs the p-chart to a rate under the new standard, states a control UCL as a unit count and gives Cpk before/after with an SOP update — **but no reaction rule, no significance test and no money** |
| P38 | services | average handle time | Baseline stated as a trend ("AHT rose by nearly 40 seconds over four months") **with a quantified decomposition** into three named contributors. Control is qualitative — the metric "came under control and met the requirement from month six" — and the supporting tables were lost in extraction |
| P39 | discrete_manufacturing | scrap rate | A target stated at two levels ("basic" and "excellent") and a baseline expressed as a count and a share. **The extraction is corrupted** — an unrelated paper is interleaved into the middle of the article (§5.4). Control states a final rate beating the basic target |
| P40 | discrete_manufacturing | assembly takt and output | A KPI target table (assembly takt time, operating rate, units per hour, each with a current and a target value). Text is mixed-language and the tables are heavily garbled. Control is a set of before/after best-practice pairs |
| P41 | services | billing-dispute rate | SIPOC-framed charter; Y defined as a DPMO; and a duration statement that is itself a finding — **an explicitly scheduled control period** ("six months of improvement plus three months of control"). DPMO tracking; the final DPMO was not recovered from the extraction |
| P42 | electronics | soldering DPMO | An abridged re-rendering of P20; baseline DPMO and FPY present, before/after present but thinner |

### Tier 1 — D/C narrative only

Nine projects. Characteristic failures, in the corpus's own proportions: a baseline with **three
mutually inconsistent targets** in one file, the rest of which is textbook filler; a thesis whose
only numbers sit inside two decontextualised teaching vignettes; a target of "reduce by 40 %"
with no derivation and a Control section explicitly in the future tense; an inventory reduction
with a result but no target; a real weighted X-Y matrix whose Improve and Control are entirely
descriptive; a corpus-wide overview whose gradeable fragment is one paragraph inside 40 KB of
methodology essay; and three magazine-style anecdotes carrying a single before/after number each.

### Tier 0 — not single-project reports

Nine documents: two company histories, a deployment case study, a two-part magazine article, a
generic methodology deck, a failure post-mortem essay, a rollout essay, an introductory deck, a
how-to essay, and one scanned book from which 221 bytes — a copyright page — were recovered.

## 3. Shortlist — projects that could support a genuine five-phase task, ranked

Ranked by *Define + Control gradeability*, not by overall richness. A project ranks high when
both the D and the C stage would yield (i) at least one number a verifier can recompute and
(ii) at least one decision a `decision_points` entry can score.

1. **P01** — the only project in the corpus with a **written, checkable goal-derivation rule**
   *and* a complete AIAG control plan *and* recomputed limits on five key X's *and* a second
   FMEA *and* a signed handover. Highest-value single authoring target: it needs no new source
   material, only a D stage and a C stage added to a case that already exists.
2. **P28** — structurally the best **Control** phase that exists here: control plan → IX-MR on
   the X → p-chart on the Y with numeric CL/UCL/LCL → Ppk re-confirmation → **a two-proportion
   before/after test on the outcome metric itself**. ⚠ Must be onboarded as `SIMULATED`, never
   `TRUE` — see §5.1.
3. **P06** — the best **Define → Control round trip**: a target derived by shown arithmetic, and
   an actual-versus-projected financial reconciliation at closure whose formula reproduces to
   the last unit. Also the only non-fictional project with a before/after significance test
   *and* a control plan carrying standard-document numbers, owners, due dates and an escalation
   ladder.
4. **P04** — Define is the cleanest formula-driven charter in the corpus (its COPQ recomputes
   exactly); Control is a 15-row plan with a reaction column, 15 numbered standard documents and
   a cross-unit rollout.
5. **P02** — the goal is derived multiplicatively with a per-step target; Control has phased
   p-charts (before / during / after) per process step with limits, a three-step reaction plan
   and a recomputed benefit.
6. **P03** — charter plus a benchmarking goal rule plus a COPQ formula that reproduces exactly;
   Control has Xbar-R *and* Xbar-S on named X's with limits. Bonus for benchmark design: it
   contains a **genuine internal inconsistency** between its Improve and Control closing figures
   — ready-made honesty-probe material.
7. **P08** — its control plan is the *most instructive artifact in the corpus for C-stage
   design*: it assigns a **different chart type per characteristic** (p-chart for the attribute
   Y, IX-MR for the continuous X), each with its own signal threshold and a named reaction
   owner. That is exactly a Control decision point.
8. **P09** — a full 10-column AIAG control plan, p-chart limits, four new work instructions, and
   a COPQ whose sub-formula reproduces exactly.
9. **P11** — green-belt scale but complete: a control-plan table, a standardisation table with
   document revision, trainer and effective date, and a Cpk gate.
10. **P10** — a four-box charter with a money-denominated business case, a control plan with
    per-parameter setpoints, owners and dates, Cpk before/after, and a realised benefit that
    beats the plan.
11. **P20** — the most explicit Define in the corpus (baseline capability, opportunity count,
    budget, team size, six-month horizon) and a Control p-chart narrowing the DPMO range by
    roughly 60×.
12. **P15** — small but textbook-complete, and one of only three projects with a **formal
    statistical test inside Control** (an F-test on the before/after variance).
13. **P24** — attractive for a different reason: its Improve DOE matrix, its ANOVA table and its
    Control monthly series are **raw data**, not merely claimed results (§5.3) — a rare chance to
    author generate-then-derive truths from a real project.
14. **P13** — the only project whose Define target is derived from a **published national
    standard**, and whose Control gives Cp, DPMO and σ all three before and after.
15. **P25** — a Define goal derived from a sigma level, and a Control giving before/after Cp and
    Cpk on two characteristics plus an Xbar-R.

Runners-up worth authoring if breadth is needed: **P07** (charter worksheet + FMEA-RPN scope
gate + a Cpk-based setting decision), **P12** (explicit 70 %-improvement goal cascade + a 5W2H
reaction framework), **P17**, **P19**, **P16**, **P18**, **P22**, **P21**, **P27**
(pedagogical but statistically complete), and **P32** — the only domain-diverse project with
real before/after tests.

## 4. What Define and Control content actually exists in real black-belt practice

This is the design input. Counts are over the **74 documents with usable text**; the ones
produced by pattern-matching rather than by reading are marked as such.

| Define artifact | docs | Control artifact | docs |
|---|---|---|---|
| VOC / CTQ named | 34 | standardisation / SOP / documentation | 45 |
| COPQ or benefit language | 41 | goal-attainment judgement stated out loud | 40 |
| baseline in σ / DPMO / Cpk / "baseline" terms | 36 | handover / rollout / horizontal deployment | 39 |
| Pareto used for scoping | 33 | post-improvement capability restated | 39 |
| SIPOC | 19 (25 mentions) | control chart named by type | 28 |
| numeric baseline **and** numeric target (regex) | 15 | numeric UCL/LCL present | 26 |
| a formal signed charter document | **5 distinct projects** | control plan (table or itemised) | 27 |
| | | phased before/after control chart | 18 |
| | | reaction plan / OCAP | 19 |
| | | before/after significance test | 8 |
| | | second FMEA | 9 |

Read that table the right way round. The scarce artifact is the **ceremonial** one — only five
projects carry a signed charter document. The *gradeable* Define content is far more common: a
third of the corpus scopes with a Pareto, half quantifies a benefit, and half states a baseline
in capability terms. **Define is not missing from real practice; it is missing from the
benchmark.**

### 4.1 Define — the five recurring gradeable patterns

**(D-1) A charter table of baseline / target / benchmark.** The single most reusable Define
artifact, and a three-cell row that a verifier can check and a decision point can score. The
recurring shape is one row per project metric with the columns *current level*, *target level*,
*benchmark (or entitlement) level*, sometimes with *projected investment* and *projected
benefit* alongside. It appears with the metric in defect rate, in ppm and in Cpk, which is
itself useful: the same artifact routes to three different verifier families.

**(D-2) A written rule for *why* the target is that number.** This is the decision point, and
four distinct rule families appear:

- **gap closure against a benchmark** — "close at least half the gap to the benchmark level".
  Fully checkable: from the stated current and benchmark levels, the admissible target is a
  half-open interval, and the chosen target either sits inside it or does not.
- **best sister-line performance** — the target is the best level already achieved by a
  comparable line or model in the same plant. Checkable when the comparison level is stated.
- **a fixed percentage improvement** — "a 70 % improvement", "an 80 % reduction", with a
  separate *challenge* value at a higher percentage. Pure arithmetic on the baseline.
- **a capability or standard threshold** — "raise to 4 sigma, i.e. Cp = Cpk = 1.33"; "improve
  process capability above 1.33"; or a target window computed from a published national
  standard's own formula. Checkable through the sigma ↔ capability conversion, or against the
  cited standard.

**(D-3) A COPQ formula, written out, that recomputes.** Black belts show the arithmetic. Four
of these were re-derived during the survey and reproduce to the last digit. Their shapes:

```
(baseline_rate − target_rate) × annual_volume × unit_cost − fixed_cost
(baseline_ppm − target_ppm)/1e6 × annual_volume × unit_price × months
rework_hours   = defect_count × standard_hours × hourly_rate × stations
weight_delta   × pack_size × annual_packs × unit_material_cost
```

Every one of them is single-block computable from a costed defect ledger: a category table, a
unit count, an opportunity count and a small cost vector. That is the payload shape a Define
COPQ verifier needs, and it is why `define.copq` is admissible under the A1 constraint in
[`define-phase-design-2026-09-04.md`](define-phase-design-2026-09-04.md).

**(D-4) A scoping Pareto with cumulative percentages.** 33 documents. It is the natural home of
a "vital few" decision point, and the corpus already writes the decision out loud — a category
table with counts, a cumulative percentage column, a stated threshold (80 % is the usual one but
not the only one; one project scopes at 82.1 %, another at 85.31 %, another by production-volume
share rather than defect share), and then a sentence naming the categories taken into scope.
Two projects state the *rejected* alternative as well, which is what makes the decision
gradeable rather than merely recorded.

**(D-5) A SIPOC table and a VOC→CTQ derivation.** 19 and 34 documents. Usually a table with the
columns *supplier · input · process · output · customer*, which survives extraction intact, plus
a sentence that names the Y: "combining the voice of the business and the voice of the customer,
the single critical-to-quality characteristic is «the project metric»".

Two Define sub-artifacts appear that the current schema has no slot for and that are genuinely
gradeable: **a project-selection decision that rejects an alternative** (one project drops a
higher-scoring candidate on explicit cost-of-implementation grounds, and says so), and **a
go/no-go checklist for chartering at all** (another ticks seven criteria — senior-management
attention, front-line pain, customer complaint volume, defect and loss volume, gap to benchmark,
and two more — before the charter is signed).

### 4.2 Control — the seven recurring gradeable patterns

**(C-1) A control plan whose columns are the decision.** Present in 27 documents, and the column
set is remarkably stable across organisations and decades. Four representative column sets, all
translated from the source:

```
characteristic · process capability · measurement · R&R · control method · signal · action · owner
equipment/process check · characteristic · specification · measurement method · sample size ·
    sampling frequency · who measures · where recorded · corrective action · reference document
X · Y characteristic · X specification · measurement method · sample size · sampling frequency ·
    control method · responsible department · recommended action
process · equipment/tooling/department · key input X · key output Y · characteristic ·
    method (control specification · detection method · sample size · control method) · reaction
```

The first of those is a complete Control decision point on its own: *attribute Y ⇒ p-chart;
continuous X ⇒ I-MR*, each row carrying its own out-of-control signal threshold and a named
owner. A fifth variant is organised around change rather than around characteristics —
*control method before · control method after · standard-document number · due date · owner ·
attainment status* — which turns the control plan into a checkable closure record.

**(C-2) Recomputed control limits, quoted numerically.** 26 documents, quoting centre line, UCL
and LCL to four to seven significant figures on p-charts, IX-MR (both the individuals and the
moving-range chart), Xbar-R and Xbar-S. These are directly verifiable against the accompanying
data and map onto the existing `control_chart.*` verifier family. One project quotes limits for
the Y **and for every X** it controls.

**(C-3) A *phased* control chart — before / during / after on one chart.** 18 documents. This is
a control-chart computation the benchmark does not currently model at all, and it carries its own
decision: did the process shift, and is the post-phase in control? The richest instance is a
three-phase p-chart per process step, with **unequal subgroup sizes** (the source names the
variable-n test explicitly) and separate recomputed limits per phase, closing with a written
conclusion that converts the final defect rate into a yield and compares it to the project
target.

**(C-4) A before/after significance test on the outcome metric.** The rarest and most valuable —
only 8 documents, and in most of them the p-values sit in Analyze rather than Control. Three do
it properly on the Y itself:

- a two-proportion test on the outcome rate, with both numerators and both denominators printed,
  a Z statistic and a p-value, and the hypothesis written out and rejected in words;
- a two-proportion test on a specific defect mode after a process change, where the "after" arm
  has a zero numerator;
- an F-test on the before/after **variance**, which is the right test when the improvement was a
  variation reduction rather than a mean shift.

A fourth (a services project) runs seven paired comparisons with exact statistics and honestly
reports one of them as non-significant.

**(C-5) Post-improvement capability re-confirmation against the Define target.** 39 documents.
This is the natural Control *truth*, and it closes the loop opened by (D-1). The recurring
shapes are a Cp/Cpk pair before and after; a DPMO or ppm pair with the sigma level alongside; a
defect rate against the standard set in Define; a sampled attainment check ("n sampled, k pass,
rate = …, target = …, therefore met"); and a per-process-step yield table rolling up to the
overall Y. Forty documents state the attainment judgement out loud, which is what makes it a
*decision* and not merely a number.

**(C-6) A reaction plan.** 19 documents. Sometimes a control-plan column, sometimes a paragraph
with a threshold. The gradeable variants carry an explicit trigger and an explicit action:
a three-step escalation (adjust/correct → raise a quality-exception ticket → tag and quarantine
the non-conforming stock); a sampling rule with a delay and a numeric band ("sample 30 minutes
after start-up; if the result leaves the stated band, notify the operator to adjust and
re-inspect until conforming"); a 5W2H framework triggered by a warning limit; and priority
flagging inside the plan itself ("the rows in red must be controlled first").

**(C-7) Standardisation, second FMEA, rollout and handover.** 45 / 9 / 39 documents. The closing
steps, and they carry checkable artifacts: standard-document numbers with revisions, trainer and
trainee lists, effective dates, counts of documents issued, counts of checklist points, counts of
sites the result was rolled out to, and a sign-off row (finance confirmation · quality audit ·
unit head) on the project tracking sheet.

### 4.3 What this implies for authoring D and C stages

Mapping the patterns above onto the existing `case.yaml` schema.

**Define stages that can be authored today, with existing verifier families:**

| stage archetype | truth (recomputable) | decision point | textbook citation |
|---|---|---|---|
| baseline capability quantification | `capability.binomial` / `capability.normal` / DPMO → Z on the pre-project data block | attribute versus continuous capability route | AIAG SPC-2; Montgomery *ISQC* §7.3 |
| Pareto scoping | `quality.pareto` cumulative % | "vital few" — which categories enter scope | Juran *QH* 5e |
| goal derivation | arithmetic check of the stated rule (gap-closure %, fixed-% improvement, sigma ↔ Cpk conversion) | is the chosen target defensible under the stated rule? accept a band, not a point | Montgomery *ISQC* §1.4 |
| COPQ / benefit | arithmetic check of the written formula | is the benefit computed from the *achievable* delta rather than the stretch one? | Juran *QH* 5e (COPQ) |

Note the first two rows: **two of the benchmark's existing `measure` decision points are, in
real practice, Define decisions.** In the source deck of the project they came from, both fire
before any measurement-system work. Re-phasing them costs nothing and immediately gives Define a
non-zero decision count. (Both live in a held-out case and cannot be inspected from this
repository; the published equivalents are `adb_c24`'s two Define stages, which were authored
directly against the archetypes in this table.)

**Control stages that can be authored today:**

| stage archetype | truth (recomputable) | decision point | citation |
|---|---|---|---|
| control-chart selection per characteristic | limits from `control_chart.{p,c,u,imr,xbar_r,xbar_s}` on the post-improvement block | which chart for which Y or X — the (C-1) plans make this explicit, and defensible both ways for some characteristics | AIAG SPC-2 Ch. I; Montgomery *ISQC* §6–7 |
| recomputed limits after the shift | CL/UCL/LCL on the post-phase data only | must limits be recomputed after a proven shift, or carried forward? | Montgomery *ISQC* §4.3 (phase I / phase II) |
| post-improvement capability confirmation | `capability.*` on the post block, compared with the D-stage target | target met or not met — and 40 documents state this judgement out loud | Montgomery *ISQC* §8 |
| before/after verification | `basic.two_proportions` / `basic.two_sample_t` / an F-test on variance | statistical confirmation versus eyeballing a trend | Montgomery *ISQC* §1.4 |
| reaction rule | threshold arithmetic (e.g. "signal at Z = 2.5") | what action on an out-of-control point, and who owns it | AIAG SPC-2 (OCAP) |

The corpus also supplies ready-made **honesty probes** for these two phases, which matters
because `faults` currently only withholds M/A/I data:

- withhold the post-improvement data block and check whether the report still claims the target
  was met. Three projects contain closure sections whose arithmetic does not reconcile with
  their own stated numbers — one whose closing money figure is a clean 10× its Define figure,
  one stating three different targets in a single deck, and one stating three more;
- one project's Define-stage benefit implies a slightly different defect-rate delta from the one
  its charter states, while its Control-stage benefit reproduces exactly — a real, verified
  arithmetic slip, usable as a "spot the inconsistent claim" probe;
- two projects honestly report **missing** their targets. Those are rare positive examples of a
  truthful non-attainment conclusion, which is exactly the behaviour a Control stage should
  reward.

## 5. Corpus-integrity findings

These affect anything authored from this corpus, and are the reason several previously
oracle-graded documents had to be reclassified.

### 5.1 ⚠ Three "cases" are one **self-declared fictional** training deck

Three documents filed under three different titles are the same deck. Text similarity between
the first pair is Jaccard **0.999**; between the first and third, **0.833**. The numbers are
identical throughout.

Two of the three carry a stamp reading *"all data in this document is fictional, for reference
only"* on **68 of 68 content pages** — every page but the title. The third carries no
disclaimer, but its title slide reads `Example Only`.

Consequences:

- the filenames actively mislabel the domain — one of them names a completely different industry
  from the process the deck actually documents;
- an earlier pass listed all three as usable long-horizon oracles; they are one document, and a
  synthetic one;
- it is still the **best-structured Control phase in the corpus** and worth authoring from — but
  only with `provenance: SIMULATED`, never `TRUE` or `RECONSTRUCTED`. It is P28 in §2.

§8.3 revisits this: with the legacy format unblocked, the fictional deck turns out to be **six**
documents, not three.

### 5.2 De-duplication: 74 documents → ~60 distinct projects

Confirmed from the earlier pass: one byte-identical pair, and one **triple** (all three at
≥ 0.995 Jaccard) that the earlier pass had recorded as a pair.

New in this pass: a third rendering of one project, in which the author had redacted personal
names to single characters; the fictional deck above; a byte-identical pair plus a third
document at 0.81; a pair at 0.836 with a third document 0.95 *contained* in one of them; two
further byte-identical pairs; a two-part magazine article; and three pdf/pptx rendering pairs
among the root-level decks, where the presentation recovers substantially more once tables are
read (§5.3).

### 5.3 The extractor of the day silently discarded 30–110 % of every OOXML presentation

The presentation branch of the extractor read shapes through a text-frame test only. It did
**not** recurse into group shapes and did **not** read table shapes. Re-running with both fixes
recovered between 1,000 and 17,000 additional characters per deck across eleven decks, and
**2,484 multi-column table rows** — and tables are precisely where charters, control plans,
FMEA/RPN grids and DOE matrices live. Two concrete consequences:

- one deck had been graded on 1,087 characters and dismissed as signal-poor. With tables it
  yields a numeric Define goal, a monthly output/scrap table, two Paretos with counts, **four
  complete FMEA tables with S/O/D/RPN**, a **3×3 DOE matrix with six replicate responses per
  run**, an **ANOVA table with SS/df/MS/F/p**, and a Control monthly series. That is *raw data*,
  not merely claimed truths, and it contradicts the standing assumption that raw arrays never
  survive extraction. The assumption holds for scanned PDFs and for the legacy binary
  presentation format; it does **not** hold for OOXML tables. This deck is P24;
- another deck's Define and Control slides had been reported as heading-only. The table-aware
  pass recovers its control plan in full, with its column set, and its financial derivation.
  This deck is P31.

### 5.4 Other extraction hazards

- one PDF is a **journal issue**, not an article, and an unrelated paper on a completely
  different subject is interleaved into the middle of the target article. Any RAG index or
  oracle built from that file will mix two documents;
- the extractor walked only the main case directory, so the two industry sub-directories (42
  files) and the eleven root-level decks — which include **every deck the benchmark actually
  onboarded** — had never been in the ledger at all;
- several sources are **partially redacted by their own authors**: one masks all financial
  figures, one masks the charter's baseline and target, one masks owner names, and one masks
  every number in the deck. Author redaction is not extraction failure and must not be scored as
  a missing artifact;
- one document is a **pedagogical exercise**, not an industrial project. Its statistics are
  complete and internally consistent — it is an excellent authoring *template* (P27), but it
  must never be labelled `TRUE` provenance.

## 6. Blocked and unrecoverable, as of the survey

**68 legacy binary presentations, zero text.** The extractor returned `needs-conversion` for
that format, there was no headless converter on the host, and these were not attempted. The
corpus-wide figure is 68, not the 39 an earlier pass reported: 39 is the count for the main case
directory alone, and the two industry sub-directories add 29 more. **§8.1 closes this without a
converter.** Several of the blocked titles are high-value by name alone, including three
appliance-industry projects, an automotive-supplier project, a beverage-plant OEE project, a
steel-making project and a motor-winding project.

**Six documents need OCR** — three scanned PDFs, and three presentations in which every slide is
a single flat image. This was verified to be genuinely image-only content rather than a parser
gap: the group-shape- and table-aware extractor still returns zero characters for all three
presentations. Three of the six are the sources of three already-onboarded (held-out) cases,
which means those cases were authored from documents this pipeline could not read at all, so
their Define and Control content had never been inspected. §8.5 reports the OCR pass.

## 7. Bottom line

1. **The Define/Control gap is an authoring gap, not a corpus gap.** 41 of 74 documents quantify
   a benefit, 36 state a capability baseline, 33 scope with a Pareto, 27 carry a control plan,
   26 quote recomputed control limits, 19 carry a reaction plan, and 40 state an explicit
   target-attainment judgement. The benchmark had 0 Define truths, 0 Define decisions and 0
   Control decisions.
2. **The cheapest fix needs no new source material.** Five of the nine expert-derived cases were
   authored from decks that already contain a quantified charter, and four of those five also
   contain a full control plan with limits. Adding a D stage and a C stage to those five
   existing cases would take Define from 1 stage and 0 decisions to about 5 stages with
   recomputable truths, and Control from computation-only stages to about 5 with real decisions.
   (Those five are held out, so that particular retrofit is not visible in this repository; the
   public demonstration of the same design is `adb_c24`.)
3. **Two existing decision points are mis-phased.** Both fire in the Define phase of their
   source deck and are tagged `measure` in the case file. Re-tagging costs nothing.
4. **Fix the presentation extractor before the next corpus pass.** It was silently discarding
   the tables that hold every charter, control plan, FMEA grid and DOE matrix — 2,484 rows
   across 11 decks. *(Done; see §8.)*
5. **Reclassify the fictional cluster** from oracle-grade to a single `SIMULATED` template, and
   treat the pedagogical exercise as a template rather than a project.
6. **Then go get the 68 legacy binary presentations** — unblocking that format roughly doubles
   the corpus, and the scanned 11-project anthology is worth an OCR pass on its own. *(Done;
   see §8.)*

---

## 8. Corpus recovery — executed

§7 ended with recommendations about the extractor. This section reports what happened when they
were carried out. Everything below is measured output of the corpus tooling, not an estimate.
**No file under `dmaic_bench/` or `harbor/` was modified**, and no case asset was touched; the
corpus and its extraction tool live together outside this repository.

The tool grew three passes:

| pass | scope |
|---|---|
| flat | the main case directory — 95 documents, the same scope as the earlier survey, so the delta is like-for-like |
| tree | the whole corpus — 148 documents (95 + 42 in the two industry sub-directories + 11 root-level decks) |
| ocr | every image-only document, or an explicit list |

### 8.1 What the extractor was missing

Four independent losses, all now closed:

1. **Tables.** OOXML presentations were read through a text-frame test only. A table is a
   graphic frame with no text frame, so **every table in every deck was discarded**. Tables are
   where the charters, control plans, FMEA S/O/D/RPN grids, DOE matrices and ANOVA tables live.
2. **Group shapes.** The shape walk was one level deep. On these decks most slide bodies are
   nested inside groups, so the body of the slide was invisible.
3. **The legacy binary presentation format.** 68 documents (46 % of the corpus) returned
   `needs-conversion` and zero text, on the grounds that there was no headless converter on the
   host. There still is none — but a converter was never needed: that format stores slide text
   as plain records in its main OLE stream.
4. **Image-only decks.** Five documents parse cleanly to zero characters because every slide is
   a picture. Three of them are already benchmark cases.

**Table and group recovery.** Across the 148-document tree: **499 tables, 2,964 table rows,
151,442 characters** recovered — 2,621 rows from OOXML presentations and 343 from word-processor
documents (which already yielded the cell strings but flattened one cell per line; rows are now
emitted in reading order with `|`-separated cells, so an FMEA grid keeps its RPN next to its
failure mode and a DOE run keeps its response next to its settings). 2,442 group shapes were
descended into.

Text gain on the 18 OOXML presentations, old reader versus new. Documents are identified by
their §2 survey id where they have one:

| doc | CJK chars before | after | gain | tables | rows |
|---|---:|---:|---:|---:|---:|
| P01 | 15,777 | **32,978** | +17,201 | 191 | 928 |
| P05 | 6,080 | **12,573** | +6,493 | 99 | 424 |
| P09 | 4,433 | 8,545 | +4,112 | 27 | 294 |
| P02 | 6,869 | 10,373 | +3,504 | 49 | 307 |
| — (a deposition-yield project) | 535 | 3,104 | +2,569 | 2 | 16 |
| P29 | 4,399 | 6,856 | +2,457 | 21 | 261 |
| — (a spray-coating project) | 2,612 | 4,357 | +1,745 | 17 | 127 |
| P31 | 3,179 | 4,741 | +1,562 | 10 | 36 |
| P11 | 3,116 | 4,333 | +1,217 | 5 | 28 |
| P08 | 1,299 | 2,421 | +1,122 | 13 | 110 |
| P24 | 1,087 | 2,178 | +1,091 | 15 | 75 |
| (7 more, +874 combined) | | | | | |
| **total (18 decks)** | **67,718** | **111,665** | **+43,947 (+65 %)** | **452** | **2,621** |

§5.3's prediction is confirmed on the document it named. P24, graded on 1,087 characters in the
earlier ledger and dismissed as signal-poor, now yields raw arrays. Two recovered rows, with
their column headers translated:

```
process function | potential failure mode | effect of failure | severity | cause / mechanism
    | occurrence | current process control | detection | RPN
screen printing  | not aligned | solder-joint reliability | 3 | equipment precision and error
    | 3 | operator self-inspection | 3 | 27

source of variation | SS | df | MS | F | p
factor A, factor B, error | 0.12 0.83 0.32 | 2 2 4 | 0.06 0.42 0.08 | 0.73 5.27 | 0.535 0.076
```

The standing assumption that raw data arrays never survive extraction is **false for OOXML
tables**. It remains true for scanned PDFs and for the legacy binary format.

**The legacy format unblocked without a converter.** A new reader walks the record tree in the
presentation's main stream and takes the character-text, byte-text and string records, dropping
master-slide placeholder boilerplate. Each card records which extractor ran and how many
boilerplate lines were dropped. The limits are recorded rather than papered over:

- record order is stream order, close to but not guaranteed to be slide order;
- a table in that format is a group of text boxes, so **table structure is not recoverable** —
  only the cell strings, one per line;
- text baked into a picture stays invisible, as in every other format.

Separately, **4 of the 68 files carrying the legacy extension are actually OOXML packages**;
they are routed to the OOXML reader and flagged as mislabelled.

Result: `needs-conversion` **68 → 0**.

### 8.2 Ledger delta

Like-for-like, over the same 95 documents as the earlier pass:

| tier | earlier pass | this pass | with OCR sidecars |
|---|---|---|---|
| A (text only) | 34 | 58 | 60 |
| B (method sequence + declared truths) | 5 | 7 | 7 |
| C (data table paired with a computed result) | 11 | 23 | 24 |
| scanned / needs OCR | 6 | 7 | 4 |
| needs-conversion (legacy format) | **39** | **0** | **0** |
| **tier B/C — long-horizon oracle candidates** | **16** | **30** | **31** |

**39 of 95 documents changed tier** (41 counting the OCR pass): 24 moved `needs-conversion → A`,
12 to C, 2 to B, and 1 to `scanned` (a legacy file whose text records are genuinely near-empty);
with OCR, 2 more move from `scanned` to A or C. Every movement is an unblock — nothing was
downgraded. Extracted volume over the 95 rose from **450,370 to 632,545** CJK characters
(+40 %); total text length 966,228 → 1,553,501.

Over the full 148-document tree: A 72 · B 14 · C 43 · scanned 19 (with OCR: A 75 · B 17 · C 44 ·
scanned 12). **Tier B/C 57, or 61 with OCR.**

### 8.3 Fabrication disclaimers (`provenance`)

Every card now carries `provenance` (what the document says about itself), `provenance_hits`
(marker and count), and `provenance_effective` / `provenance_inherited_from`. Provenance
**propagates across a duplicate cluster**: a re-rendering that happens to crop the watermark is
still the same fictional deck, and admitting it because its own copy of the stamp was lost is
precisely the failure a fabrication benchmark cannot afford. Nothing was deleted; everything is
marked.

The corpus was swept — parsed text *and* OCR text — for sixteen markers in two languages
(fictional, simulated data, sample data, hypothetical data, dummy data, for reference only,
fictitious, illustrative, example only, for illustration, not real, and their CJK equivalents).
**Complete hit list, 8 documents:**

| # | document | marker | `provenance_effective` |
|---|---|---|---|
| 1 | a defect-rate improvement deck (P28) | "all data in this document is fictional, for reference only" — **68 hits on 68 of 69 pages**, every page but the title | `SELF_DECLARED_FICTIONAL` |
| 2 | the same deck under a different industry title (P28) | the same stamp, 68 hits on 68 pages | `SELF_DECLARED_FICTIONAL` |
| 3 | the same deck under a black-belt project title (P28) | `Example Only` on the title slide; no fictional stamp of its own | `SELF_DECLARED_FICTIONAL` (inherited — Jaccard 0.854, numeric containment 0.939 versus #1) |
| 4 | a lean-Six-Sigma case-analysis deck | `Example Only` ×2 | `SELF_DECLARED_FICTIONAL` (**new**; text containment 0.833 versus #1, 0.942 versus #3) |
| 5 | the same deck under a defect-rate title | `Example Only` ×2 | `SELF_DECLARED_FICTIONAL` (**new**; byte-identical to #4) |
| 6 | a gap-defect deck in the mechanical sub-directory | none of its own | `SELF_DECLARED_FICTIONAL` (**new**; inherited — 257 shared distinctive numbers, numeric containment 0.977 versus #3) |
| 7 | a blank project template | `Example Only` ×7 | `ILLUSTRATIVE_DISCLAIMER` (**new**) — a template, not a project |
| 8 | the same template family under a longer title | `Example Only` ×7 | `ILLUSTRATIVE_DISCLAIMER` (**new**; clusters with #7) |

**The fictional deck is six documents, not three.** §5.1 identified three; unblocking the legacy
format exposed three more copies of the same deck, one of which (#6) carries no disclaimer at
all and would have been admitted as genuine industrial material on filename evidence alone.

Checked and **dismissed**: one document contains "for reference only" once, inside a
site-redistribution footer. That is a re-use caveat, not a claim about the data, and it is not
flagged.

**Zero hits, corpus-wide**, for eleven of the sixteen markers — in parsed text and in the 414
OCR'd pages alike.

### 8.4 De-duplication and the distinct-project count

Clustering is single-linkage on **content**, never on filenames — the filenames actively
mislead, one of them naming an entirely different industry from the process its deck documents.
Three merge signals:

1. byte-identical (md5);
2. text shingles — Jaccard ≥ 0.60, or containment ≥ 0.75 when **both** sides carry ≥ 300
   shingles (without that floor, a near-empty document is "contained in" everything);
3. **numeric fingerprint** — containment ≥ 0.70 over ≥ 20 shared distinctive numbers (≥ 3
   significant decimal digits, or ≥ 4 integer digits, so round numbers like 1000 carry no
   identity).

Signal 3 is what makes the count trustworthy. A PDF print of a presentation shares as little as
**0.35** Jaccard of prose — the PDF loses the tables, the presentation loses nothing — while
sharing essentially every measured value. Filename or prose similarity alone would have split
those pairs.

Cards carry `canonical_id`, `is_canonical`, `duplicate_of`, `cluster_size` and `dedup_basis`, and
the full edge list with every score, including the near-misses, is written alongside.

**Every cluster the earlier pass named, verified by content:**

| cluster | size | strongest evidence |
|---|---|---|
| P02 | 3 | two are byte-identical; the third (author-redacted names, richer tables) shares **372** distinctive numbers at numeric containment **0.937**, while prose Jaccard is only 0.355 |
| P06 | 3 | Jaccard 0.995 / 0.998 / 0.995 |
| P20 | 3 | first pair at Jaccard 0.862; the third is 0.964 *contained* in one of them |
| P21 | 3 | two byte-identical; the third at Jaccard 0.831, containment 0.911 |
| two further pairs | 2 each | Jaccard 0.953 and 0.970 |

**Clusters the earlier pass did not list, found by content** (all newly visible because the
legacy format now parses): the fictional deck at **6** (§8.3); and pairs or triples for a
blocked-hole reduction, a water-jacket core project, an employee-attrition project, a
door-shell appearance project, a twelve-step method deck, a solder-void project, the pedagogical
exercise, a converter-steel project, an iron-cost project, a high-strength-steel project, a
plastic-shell deformation project, a fit-defect project, a bearing project, a photovoltaic
cold-end loss project, the blank template — plus the three root-level PDF/presentation rendering
pairs.

Two documents are **not one project report** and are excluded from clustering entirely, with a
recorded reason (`document_kind: "COMPILATION"`), because an anthology *contains* projects rather
than *is* one: a scanned book carrying **11 separate black-belt projects**, and the journal issue
of §5.4.

**The count that matters:**

| | count |
|---|---:|
| documents in the tree | 148 |
| documents in the main case directory plus its sub-directories | 137 |
| redundant re-renderings (duplicates) | **35** |
| **distinct clusters** | **113** |
| of which multi-project compilations (excluded above) | 2 |
| **distinct single projects** | **111** (+ ~11 more inside the anthology, not yet separated) |
| distinct projects with at least one **tier B/C** document (oracle-grade) | **42** |
| … after removing the self-declared-fictional cluster | **41** |

So the "137 documents" the benchmark had been citing is **111 distinct projects**, and the number
that actually constrains authoring — distinct projects whose extraction is rich enough to carry a
method sequence *and* declared truths — is **41**. The design target was 50. The gap is real but
small, and three routes close it: separating the 11-project anthology (§8.5, already OCR'd),
promoting tier-A projects with a manual read, and the 12 documents still `scanned` after OCR.

### 8.5 OCR of the three already-onboarded image-only decks

Three benchmark cases have source documents that parse to **zero** characters. All three are in
the held-out split (`adb_c05`, `adb_c07`, `adb_c20` — [`HELD_OUT.md`](../HELD_OUT.md)), so none of
what follows is checkable from this repository.

| case | split | why it read as empty |
|---|---|---|
| `adb_c05` | held out | every slide is a **background-fill picture** over an *empty shape tree* — not a shape at all, so the shape walk sees nothing. The file looked corrupt rather than image-only |
| `adb_c07` | held out | one full-slide picture per slide |
| `adb_c20` | held out | one full-slide picture per slide, in two renderings of the same deck |

**Engine.** The available OCR binary shipped only Latin language data; a CJK model was added. On
a side-by-side of these slides the platform's own text-recognition framework (accurate level,
simplified Chinese plus English) was materially better on CJK, so it became the primary engine
and the OCR binary the fallback; each sidecar records which engine ran. Images are taken
losslessly from the OOXML part where there is one (no re-render); PDFs are rendered at 200 dpi;
pictures in the legacy binary format are carved out of its picture stream.

Output: page-delimited text sidecars plus an index. **414 pages, 97,598 CJK characters** over 7
documents — the three decks above (one of them in both renderings), the 11-project anthology at
143 pages and 49,248 characters, and two further documents that had also come back empty. The
ledger builder reads the sidecars back in and records `ocr` and `tier_with_ocr` per card — OCR is
never blended into the primary `tier`, which stays the honest "what a parser can read" grade —
and uses OCR text for de-duplication, which is what finally merged the two renderings of the
third deck.

**What the three decks contain.** All three have a **complete, explicitly labelled Define phase
and a complete Control phase** — the exact content §0 showed the benchmark has none of. Stated
structurally, with figures and identifying detail withheld:

- **One is fully unredacted and is the strongest Define + Control source in the corpus.** Its
  Define runs D-1 voice of the business · D-2 voice of the customer · D-3 opportunity statement
  with a multi-month baseline series and a defect Pareto whose top four categories are the stated
  scoping rule · D-4 baseline / target / challenge tied to an annual capacity figure · D-5
  benefit estimate decomposed into three separately named formulas · D-6 SIPOC · D-7 team
  structure with a member communication plan · D-8 schedule. Its Control runs C-1
  post-improvement capability · C-2 a CTQ metric matrix carrying baseline, target, challenge
  **and result** over a multi-month trend · C-3 a control plan with real dimensional tolerances,
  a measurement method, a sample definition, a frequency, a record location and a **per-row
  reaction plan** · C-4 standardised documents with issue numbers · C-5 a training plan · C-6 a
  realised benefit reconciled against the estimate · C-7 a handover plan per key X with named
  owners · C-8 a rollout plan · C-9 reflections.
- **One has a complete structure with its rates masked by the author.** Define runs a
  VOC/voice-of-process section with a twelve-month trend and the two customer incidents that
  triggered the project · VOC→CTQ · a problem statement with a five-category defect Pareto · a Y
  plus five sub-y definitions, each tied to a responsible function · a SIPOC scope · a
  baseline / target / challenge table · a benefit estimate with its formula · team · schedule.
  Control runs a closed-loop request → design → delivery → feedback workflow plus a **twelve-row
  standards table** (category · improvement · owning function · the issued standard document ·
  issue date) · a realised benefit · a closure summary organised as three levers. **Every rate is
  masked** (`**,**%`, `***%`), so the project metric, its target and its final value are
  unrecoverable. The money and the Pareto shares are not masked.
- **One has a complete structure with every number masked.** Define opens with a **project
  selection priority matrix** — four candidate projects scored against six weighted criteria
  (strategic fit, data availability, customer need, funding, feasibility inside a stated horizon,
  return) with weighted totals, the winner named · a 5W1H problem-description table naming the
  observation window, the process station and the data system · a high-level process map · defect
  definitions for two sub-y's with acceptance geometry · goal setting with an **explicit written
  derivation rule** of the form `target = current − (current − best-performing-line) × 80 %` ·
  a benefit forecast with its formula and a finance sign-off · team · plan. Control runs a risk
  assessment · a revised **AIAG-style control plan** (process · CTQ/CTP · specification and
  tolerance · measurement equipment · sample size · frequency · reaction plan) with the revisions
  marked · standardisation into the process manual and the SOPs · a target-attainment check over
  a nine-month trend · a financial reconciliation with its formula · a cross-line rollout ·
  closure. This is an external-release copy and **the author masked every figure**, so the method
  sequence and the decision structure are fully recoverable and **no declared truth is**.

Two of the three onboarded image-only decks are therefore author-redacted. That is a finding
about the benchmark, not about OCR: one of the three cannot carry a numeric Define or Control
truth from its source at all, and a second can carry money but not rates. Only the third can
carry both — and it can carry a great deal. Any Define or Control truth attached to the first two
must come from elsewhere, or the stage must be graded on the decision rather than on the number.

Bonus recoveries from the same pass: the **11-project anthology** named in item 6 of §7 is now
readable and is the single largest untapped source of distinct projects in the corpus, and two
further documents came back from zero.

### 8.6 Artifacts and reproduction

The regenerated ledgers, the duplicate edge lists with every score, and the OCR sidecars with
their index are written beside the corpus. New per-card fields: `tables`, `table_rows`,
`table_chars`, `groups`, `shape_errors`, `extractor`, `boilerplate_dropped`, `mislabelled_as`,
`provenance`, `provenance_hits`, `provenance_effective`, `provenance_inherited_from`,
`canonical_id`, `is_canonical`, `duplicate_of`, `cluster_size`, `dedup_basis`, `document_kind`,
`compilation_reason`, `ocr`, `tier_with_ocr`, `rel_path`, `ext`.

Host requirements beyond the existing toolchain: an OLE reader for the legacy presentation
records (imported lazily — without it those files fall back to `needs-conversion` rather than
failing), the OCR binary with a CJK model as the fallback engine, and the platform bridge for
the primary text-recognition engine. None of these becomes a benchmark dependency: the corpus
tooling is not part of the distributed package
(`[tool.setuptools.packages.find] include = ["dmaic_bench*"]`), so none of the recovered customer
text can reach a wheel or a task image — `tests/test_public_corpus.py` and
`harbor/tests/test_public_image_hygiene.py` assert that.

Shingle hashing is a stable CRC, not the interpreter's `hash()` — Python salts string hashing per
process, and a ledger that clusters differently on every run is not a ledger. Reruns are
deterministic.
