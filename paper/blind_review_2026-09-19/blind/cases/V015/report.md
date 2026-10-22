# Capacitor defect-share project report

## Executive summary

The baseline was stable but not compliant. Across **25** baseline lots, **546** defective units were found in **100000** inspected units, for a defect share of **0.00546**. The p-chart flagged **0** of the **25** lots. Thus the process was predictable, but its center was **2.184** times the committed share of **0.0025**; the exact one-sided comparison produced a p-value of **4.220242209124989e-59**.

The line improvement coincided with a substantial reduction. The before/after windows fell from **0.005925** to **0.003375**, a **43.0379746835443%** reduction, with a two-sided p-value of **1.1530117357517475e-07**. The **20** lots since the change are also stable, with **0** chart flags and a pooled share of **0.0034375**. However, they still contain **75** more defectives than the same **80000** units would contain at target, and the current share must fall another **27.272727272727273%** to reach the commitment. The change helped, but it did not close the gap.

## What the data show

### Baseline condition

The baseline aggregate was **546** defectives out of **100000** units. Its p-chart center line was **0.00546**, and no individual lot crossed the chart limits, so common-cause variation—not one isolated assignable lot—characterized the period. The aggregate share was significantly above **0.0025** (p-value **4.220242209124989e-59**), with **296** excess defectives relative to that commitment.

### Settings associated with the baseline response

A model using the supplied paste thickness, reflow peak, and their interaction was fitted to **40** records. Its overall p-value was **1.20039199680057e-06**, and it accounted for **56.426363457132034%** of response variation (adjusted **52.795227078559705%**). All three supplied model terms were significant: paste thickness p-value **1.5878687634538685e-05**, reflow peak p-value **3.647421126578713e-05**, and interaction p-value **1.2151358677491888e-05**. This identifies line-settings information that is on file and statistically associated with defect share; because these are observational lot records, it does not by itself prove a causal effect or identify an optimum.

### Effect of the change

The before window had **237** defectives in **40000** units (**0.005925**), while the after window had **135** in **40000** (**0.003375**). The two-proportion test gave z **-5.300792345784441** and p-value **1.1530117357517475e-07**, or **43.0379746835443%** relative improvement. The separate aggregate of lots since the change was also **37.04212454212454%** below the baseline share (p-value **2.48636583545256e-10**).

The trial was planned at **40000** units per group with alpha **0.05** to detect a change from **0.0059** to **0.0025**. Its computed power was **0.9999999914471074**, so lack of statistical evidence is not a concern; the detected before/after difference was nevertheless smaller than the target improvement.

### Current hold and remaining gap

The post-change lot set has **275** defectives out of **80000**, giving **0.0034375**. Its p-chart again showed **0** outliers, so the new level appears to be holding, but at **1.375** times the committed **0.0025**. The one-sided target comparison gave p-value **2.847837963216255e-07**. The computed Wilson interval was **0.003055072228494698** to **0.003867613591607647**, entirely above target. Meeting the commitment requires a further **27.272727272727273%** reduction from the current lot-share level.

## Limitation that stops a conclusion

No released data identifies the specific physical or procedural change. Process-owner requests were unroutable, and the steward reported no recorded process topics. Therefore, we cannot state what was changed, verify it was implemented as intended, or attribute the improvement specifically to that change rather than to another concurrent condition. That conclusion stops at the available data.

## Recommended actions

1. Obtain and document the actual change and its implementation evidence, then use a controlled confirmation trial to establish causation.
2. Use the significant settings relationship to guide a designed optimization; confirm the selected settings on independently inspected lots before rollout.
3. Continue the lot-level p-chart after the next intervention. Do not declare success until the stable center is at or below **0.0025**, not merely below the old baseline.
4. If the current settings do not reach the remaining **27.272727272727273%** reduction, escalate to the next identified design or material lever and recheck capability after the new lots accumulate.

One initial settings-model implementation failed before producing output; it is recorded as a failed trace step. The conclusions above use only the subsequently successful computations. No steward batch containing the process-change fact was denied outright, but none could be routed or released.
