# Wave-solder fillet-height project report

## Executive position

The accepted fillet-height interval is **6.800 to 7.500 mm**, with **7.150 mm** as target. In the ordered baseline sample of **60** joints, the mean was **7.12495 mm**, the observed range was **6.807 to 7.457 mm**, and all **60** observations were inside specification. That is good observed conformance, but it is not evidence of a capable process: **Cpk = 0.79919** and **Ppk = 0.79893**. The practical issue is variation, not a demonstrated shift away from target.

The designed experiment did not identify any of the deliberately varied settings—or their interactions—as an explanatory driver. The overall factorial model had **p = 0.90345** and explained **23.8302%** of response variation; adjusted explained variation was **-42.8184%**. The three additional logged variables also failed to explain the response jointly (**p = 0.85713**, **R-squared = 1.71098%**). Because the experimental screen was negative, the steward locked the before/after batch. There is therefore no available computation showing what the line change achieved.

## Baseline behavior and conformance

The baseline median was **7.1445 mm**, sample standard deviation was **0.13558 mm**, and skewness was **-0.02485**. Anderson-Darling normality testing gave **p = 0.30601**, so a normal capability calculation is not contradicted by this sample. A one-sample test against target gave **t = -1.43118**, **p = 0.15765**, with the mean **0.02505 mm** below target; the data do not establish a target shift.

Sequence checks do not show special-cause behavior. The runs test gave **p = 0.60248**. The Individuals chart center was **7.12495 mm**, with limits **6.71835** and **7.53155 mm**, and flagged **0** points. The Moving Range chart also flagged **0** points. Thus this window looks stable enough for capability interpretation, while recognizing that it is one finite production window.

Normal capability estimates were **Cp = 0.86080**, **Cpk = 0.79919**, **Pp = 0.86052**, and **Ppk = 0.79893**. The close short- and long-term values agree with the stability finding. All observed pieces passed, yet indices below **1.00000** indicate that the modeled process spread is wider than the tolerance can reliably accommodate. Continued production should not rely on the zero observed defects alone.

## What accounts for fillet height

The designed run contained **16** observations across **8** treatment combinations with **2** replicates per combination. The full factorial model gave **p = 0.90345**. Main-effect estimates and p-values were:

- chain speed: effect **0.01181 mm**, **p = 0.71560**;
- rail angle: effect **0.01099 mm**, **p = 0.73454**;
- air pressure: effect **-0.01151 mm**, **p = 0.72246**.

The largest estimated interaction was chain speed by air pressure at **0.04446 mm**, but its **p = 0.19309**. The remaining interaction p-values were **0.78950**, **0.94228**, and **0.98239**. None of the tested settings or interactions is demonstrated to account for fillet height in this experiment. Residual normality was not rejected (**p = 0.83887**). Bartlett's cell-variance check gave **p = 0.13990**, although variance evidence is weak because each cell has only **2** replicates. A median-centered Levene calculation was degenerate under that replication pattern and was not interpreted.

The separate observational log contained **48** records. Its joint regression on preheat temperature, conveyor-width setting, and solder-pot dwell gave **p = 0.85713**, **R-squared = 1.71098%**, and adjusted **R-squared = -4.99054%**. Marginal correlations with fillet height were **0.06353**, **0.04495**, and **-0.11413**, with p-values **0.66793**, **0.76160**, and **0.43989**, respectively. These are weak, undetected associations; because these variables were logged rather than randomized, even a detected association would not by itself establish cause.

## The change and what it achieved

No before/after comparison could be computed. The steward's `screening_significant` gate requires a significant designed-run factor, while the computed verdict was `any_factor_significant = false`. The before/after measurements were therefore locked and not released. The conclusion stops here: this analysis cannot say that the change improved, harmed, or left fillet height unchanged.

## Recommended next actions and control

- Do not standardize or credit the change on the present evidence. Preserve its exact settings and obtain an authorized, time-ordered before/after data set if management still needs a change-effect claim.
- Focus improvement on reducing common-cause variation rather than adjusting the center. Expand the designed study with more replication and with factor ranges or candidate inputs chosen from process knowledge; include nuisance blocking where production conditions can drift.
- Treat the additional process-log variables as monitoring candidates, not proven causes. If any is to be acted on, vary it deliberately in a randomized study.
- Hold the process with an I-MR chart using a verified stable reference period, maintain reaction rules for signals, and recalculate capability only after stability is reconfirmed. Continue direct specification screening while capability remains below the required business criterion.
- Verify the measurement system before a larger improvement trial; no measurement-system data were released in this task, so measurement adequacy was not computed.
