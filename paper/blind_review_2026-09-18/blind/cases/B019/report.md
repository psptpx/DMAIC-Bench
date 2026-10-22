# Turning-cell project assessment

## Management decision

**Prioritize wall-thickness variation and investigate its dispersion signal. Maintain diameter performance rather than making fixture adjustment the main project.** The data support this prioritization, but do not establish a root cause or a successful improvement. Coolant pressure is a promising investigation variable, not yet a proven control lever.

## Can the readings support a conclusion?

The crossed instrument study was analyzed using random-effects ANOVA. The operator-by-part interaction was pooled into error because its computed p-value was 0.3882. Gage repeatability and reproducibility account for **23.88% of study variation**, and **14.72% of tolerance**, with **5 distinct categories**. This is conditional measurement adequacy, not an excellent measurement system. It permits a cautious diagnostic assessment; improve measurement technique and verify calibration, operator consistency and application-specific suitability before certifying gains.

The available repeat readings are at diameter-scale values. Use of the same instrument does not independently prove its performance on the thickness contact geometry or thickness range. That remains an explicit limitation. Neither bias nor long-term instrument drift was established by this study.

## Run behavior and acceptance performance

The ordered data were analyzed as consecutive rational subgroups using X-bar/R charts. Reported signals use the point-outside-control-limits rule, not an exhaustive suite of run-pattern tests. Normality was assessed with Anderson–Darling tests; the p-values were **0.7102 for diameter** and **0.4671 for thickness**. Neither indicates a detectable marginal departure from normality; this does not establish independence or stability.

| Computed result | Outer diameter | Wall thickness |
|---|---:|---:|
| Accepted interval, mm | 24.80–25.20 | 1.20–1.60 |
| Target, mm | 25.00 | 1.40 |
| Observations | 125 | 125 |
| Mean, mm | 25.00150 | 1.391770 |
| Within-subgroup sigma, mm | 0.040612 | 0.095684 |
| Overall sample standard deviation, mm | 0.041378 | 0.092180 |
| X-bar lower limit, mm | 24.94699 | 1.26335 |
| X-bar upper limit, mm | 25.05601 | 1.52019 |
| X-bar signals | 0 | 0 |
| Mean range, mm | 0.094464 | 0.222560 |
| Range upper limit, mm | 0.199697 | 0.470492 |
| Range signals | 0 | 1 |
| Cp | 1.6415 | 0.6967 |
| Cpk | 1.6292 | 0.6681 |
| Pp | 1.6111 | 0.7232 |
| Ppk | 1.5991 | 0.6935 |
| Observed readings outside acceptance | 0 | 6 |

Within-subgroup sigma uses mean range divided by the subgroup-size correction; overall indices use sample standard deviation. The diameter run has no detected chart-limit signals and is centered with substantial acceptance margin. Its results support maintaining the current process, subject to continued monitoring and measurement limitations.

Thickness has no subgroup-mean limit signal, but **subgroup 11 has a range of 0.474100 mm**, exceeding the range limit. Its dispersion is therefore not fully demonstrated stable. Its capability indices must be treated as **descriptive baseline estimates, not certified future capability**. Even the potential index is poor: merely recentering thickness would not solve the spread problem. Do not silently discard the flagged subgroup or recalculate favorable limits without an identified, corrected cause.

## What may be causing the problem?

### Fixture comparison is secondary

The Brown–Forsythe variance test gives p = **0.3486**. The ordinary fixture ANOVA gives F = **3.1641**, p = **0.03142**, indicating evidence of unequal diameter means, rather than evidence that every fixture pair differs. In archive order, fixture means are **24.97698, 24.99745, 25.00966 and 25.00287 mm**. These results warrant checking fixture offsets and setup repeatability during routine maintenance. They do not explain the wall-thickness shortfall; the fixture sample measured diameter. No pairwise significance claims or causal fixture claims are made.

### Pressure is an actionable hypothesis, not established causality

In the paired window, Pearson correlation is **0.7020**, p = **4.1212e-10**. The fitted relationship is:

**Thickness (mm) = 1.189992 + 0.055294 × delivery pressure (bar).**

The regression explains **49.2801%** of observed thickness variation, with adjusted explained variation **48.4056%** and residual standard deviation **0.059288 mm**, using **60 pairs**. Its model p-value is **4.1212e-10**. This supports investigating pressure delivery and regulation. It does not show that changing pressure will remove the observed variation: time, temperature, wear, material, setup or another coupled variable could confound the association. The paired window cannot automatically be equated to the full baseline run.

The process-owner question about independent pressure adjustment returned no matching process fact. Consequently, controllability and coupling remain unknown. Regression assumptions and replicated causal response have not been established; no optimum setting is prescribed.

## Next action and sustainment

- Quality should contain suspect thickness output under the plant's disposition procedure and arrange an application-specific measurement check. Avoid relying solely on borderline measured values for release.
- Process engineering should investigate the flagged sampling point using tool condition, coolant delivery, setup, material and measurement records. Preserve the original baseline and document any assignable cause.
- Establish whether pressure can safely be adjusted independently. Then plan a controlled, randomized and replicated pressure investigation, blocking known nuisance conditions and measuring both characteristics. Seek reduced thickness spread as well as appropriate centering; do not sacrifice diameter.
- After an approved change, collect a new ordered run with the same rational subgroup logic. Demonstrate dispersion and mean stability before claiming capability or improvement. Compare before/after measurement performance, capability and actual nonconformance.
- For sustainment, assign the cell owner to chart review and reaction, quality to acceptance disposition and measurement verification, and engineering to cause correction and change control. Track pressure with the dimensional records. Freeze validated control limits only after the improved baseline is established; on a signal, contain affected production, verify the gage and investigate rather than automatically adjusting the mean.

**What was changed and achieved:** no implemented intervention or verified gain is documented. A request for post-change validation re-served the original thickness baseline, not a new trial. No post-change evidence or control-plan execution data were supplied; the conclusion stops at diagnosis and the proposed investigation. The steward did not explicitly deny a named analytical batch. The missing process fact was an unroutable response, not evidence that pressure is or is not independently controllable.

All numerical findings above are rounded from computed outputs in `trace.json`. The scripts and released JSON records retain the calculation trail.
