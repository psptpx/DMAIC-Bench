# Case sources

Where a case's *scenario* came from, and under what licence. This file exists because the
corpus has stopped being wholly self-authored, and that is a property worth tracking
explicitly rather than discovering later.

There are two pools here and they are not interchangeable.

**Onboarded** — a scenario that has been through the whole step: a decision graph, a
generator, and every gate green on every seed. Eight cases are in this pool, all from the
practitioner corpus described below.

**Records** — license-verified and structurally extracted, and nothing more. A record becomes
a case only once a decision graph and a generator are written for it and **G3 passes on every
seed**. None of the literature records below have been through that step.

## Scope of the source-route inventory

The eight onboarded entries below identify retained practitioner routes, not the
entire set of project-informed scenarios. Cases such as `adb_c30` and `adb_c31`
also record real black-belt origins in their modules, while their benchmark
routes are encoded from standards. The manuscript S/P field describes route
construction, not real versus synthetic scenario provenance. See
`CONSTRUCTION_QC.md` for source checks and the scope of expert validation.

## What is taken, and what is not

Every case in this corpus generates its data from a seed and derives its truths from that
data. That does not change here. What a source record contributes is the **scenario** — the
industry, the characteristic being measured, its units and limits — and the **decision
structure**: which judgements the analysts faced and which numbers decided them.

**No source data file is redistributed, and no case reproduces a source's prose.** The
verbatim sentences kept in the extraction records are evidence for the extracted numbers, so
that a reviewer can check a value against the sentence it came from rather than trusting the
extraction. They are quoted under the licences below. Records drawn from material that is not
openly licensed keep no verbatim sentence at all — see the practitioner corpus section.

## Licence rule

A record enters only if the article is **CC BY** with no NonCommercial and no ShareAlike
clause, and the licence notice is copied verbatim from the article's own `<permissions>`
block rather than from an aggregator's metadata field. That last part is not pedantry:
aggregator licence fields were observed mislabelling CC BY-NC as CC BY during this survey, so
the article's own statement is the only acceptable evidence.

## Onboarded — the practitioner corpus (adb_c32 … adb_c39)

Eight cases were onboarded from a corpus of completed Chinese black-belt project reports held
privately (the source corpus itself is not published). These are not open-licence material and **nothing from them is
redistributed**: no source file, no table, no figure, no sentence, no data array. What crossed
over is what the licence rule above calls the scenario and the decision structure — the kind
of process, the characteristic and its limits, the judgements the analysts actually faced, and
the ORDER OF MAGNITUDE of the numbers that decided them. Every case names no company, place or
person; the industry field carries one of the four coarse public values; every batch is
generated from the case's seed and every truth is derived from that generated batch by the
same verifiers every other case uses.

Where a source figure is mentioned in a module docstring or in this table, it is there to
record what the generator was calibrated against — the shape of a real result, not a value
lifted into the corpus.

| case | what the source project did | the decision it contributes |
|---|---|---|
| `adb_c32` rod_defect | attribute inspection at high volume; the report's own capability page reads 133060 PPM against a true 1331, a 100x unit error | a requirement stated in DPMO against a record kept in counts, and a follow-up question that is a contingency table rather than a means test |
| `adb_c33` placement_agreement | a visual judgement studied at kappa 0.44, criteria rewritten, re-studied at 1.00 | a repaired measurement system is not a proved one: the re-study is obligatory and is allowed to fail |
| `adb_c34` coating_thickness | capability sixpacks at Cp 1.37 on one characteristic and Cpk -1.56 with 1000000 PPM on another | a negative Cpk is the mean on the wrong side of a limit, not a bad index; Cp and Cpk read as a pair fork three ways |
| `adb_c35` dual_characteristic | two dimensions followed through the whole project, Cpk 0.71 and 1.63 on the same parts | a project is not finished because a characteristic passed; the worse of the two decides |
| `adb_c36` fillet_height | a screening design over line settings, with a confirmation step | the improvement is allowed to fail, and a failed confirmation sends the project backwards |
| `adb_c37` shaft_hardness | a hypothesis-test selection sequence, and a candidate cause reported as not significant | which comparison the data admits, and a candidate that does not survive |
| `adb_c38` capacitor_defect | defect shares verified before and after: 0.59%→0.21% and 0.18%→0.03% | "did it do anything" and "is that enough" are two questions, and an 82% reduction can answer only the first |
| `adb_c39` seal_strength | screen → response surface → optimiser → confirmation | an optimum is only worth having if the surface fits, reaches, and delivers |

What this pool gave the corpus that the literature could not: attribute measurement studies,
a measurement system that is repaired and re-proved, a negative capability index, a negative
hypothesis-test result, a failed improvement confirmation, and a full response-surface
sequence with its confirmation. Every one of those is a routing decision no open-licence
source in the survey below contained.

## Ready for authoring

### PMC12842731 — Process Capability Assessment and Surface Quality Monitoring in Cathodic Electrodeposition of S235JRC+N Electric-Charging Station

- **Journal**: Materials (MDPI), 2026
- **Domain**: surface coating / e-mobility component manufacturing (cathodic electrodeposition on S235JRC+N steel housings for EV charging stations)
- **Y type**: continuous · **decision points extracted**: 6 · **tables**: 11
- **Licence (verbatim from the article)**: © 2026 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Cre…
- **Attribution**: © the authors, CC BY 4.0. Scenario and decision structure referenced; no data redistributed.

### PMC7361965 — System Performance and Process Capability in Additive Manufacturing: Quality Control for Polymer Jetting

- **Journal**: Polymers (MDPI), 2020
- **Domain**: additive manufacturing (PolyJet / photopolymer jetting, Objet EDEN 350)
- **Y type**: continuous · **decision points extracted**: 5 · **tables**: 9
- **Licence (verbatim from the article)**: © 2020 by the authors. 2020 https://creativecommons.org/licenses/by/4.0/ Licensee MDPI, Basel, Switzerland. This article is an open access article dis…
- **Attribution**: © the authors, CC BY 4.0. Scenario and decision structure referenced; no data redistributed.

### PMC11858851 — Multivariate Data Analysis to Assess Process Evolution and Systematic Root Causes Investigation in Tablet Manufacturing at an Industrial Scale—A Case Study Focused on Improving Tablet Hardness

- **Journal**: Pharmaceutics (MDPI), 2025
- **Domain**: pharmaceutical solid-dose manufacturing (industrial-scale high-shear wet granulation → tableting → film coating)
- **Y type**: continuous · **decision points extracted**: 5 · **tables**: 3
- **Licence (verbatim from the article)**: © 2025 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Cre…
- **Attribution**: © the authors, CC BY 4.0. Scenario and decision structure referenced; no data redistributed.

## Candidate — needs extraction before it can be authored

### PMC6977137 — Practical application of Six Sigma management in analytical biochemistry processes in clinical settings

- **Licence**: CC BY 4.0 (Wiley/JCLA) - PASS · **Country**: CN (Hunan Provincial People's Hospital)
- **Score**: 3 nodes / 6 tables — **below the 4-node threshold**
- **Status**: no `decision_points` extracted yet. Held here rather than in the ready list
  because its arithmetic verified clean throughout, which is rare in this pool; promoting it
  requires running the structured extraction it never received.

## What the survey actually found

The search that produced these records is worth recording, because the headline number is a
warning rather than an invitation.

| | |
|---|---|
| full texts fetched and scored | 644 |
| pass the mechanical filter (≥4 decision nodes, ≥2 tables) | 19 (2.9%) |
| **survive manual verification** | **4 (0.62%)** |

About a quarter of the mechanical qualifiers were literature reviews or conference abstract
books whose numbers belong to other people's papers. Two were promoted by an earlier keyword
pass of ours that matched `gage` inside **engagement** and `DOE` inside **does** — substring
hits with no context check. Any future sweep must read `article-type` before it reads
keywords.

**Measurement-system analysis is essentially unpublished.** Across 644 full texts, a query for
`DMAIC AND "gage R&R"` returns a single article — PMC7361965, in the list above. Three
independent passes reached the same conclusion: real projects run MSA and do not write it up.
The corpus's earliest gate therefore cannot be sourced from the literature and has to keep
coming from hand-authoring.

**Attribute and count cases could not be sourced at all.** Zero survived three escalating
searches. The reason is structural: PMC is a biomedical archive, and industrial DMAIC reaches
it through materials-engineering journals whose responses are dimensions and hardness. That
gap needs a different index (DOAJ, or the open issues of IJQRM / IJLSS).

## Review is not optional

Every qualifying case carried at least one statistical defect, and several were
conclusion-changing:

- a paper whose stated goal attainment (22.2% ≥ 20%) is computed from **rounded** percentages;
  from its own raw counts the figure is **18.21%**, which misses the goal, and the rounding is
  never disclosed;
- a paper reporting `Only Centers A and B reached σ ≥ 3.5` whose own table gives those centres
  **3.42 and 3.19** — no centre qualified;
- a paired significance test that is **tautological by construction**, because the two sigma
  values it compares differ by a fixed constant;
- a Cpk defined as `x̄/σ`, whose reported values do not follow even that definition, with the
  paper's conclusion resting on the discrepant number.

Copying a decision structure unreviewed would encode these as correct answers, which is worse
than having no case. **Black-belt review per case is a release requirement, not a nicety** —
and these defects are themselves excellent trap material, since telling "the paper says it
passed" from "the data says it failed" is exactly the judgement this benchmark exists to test.
