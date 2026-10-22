# Coating Thickness Project Report

## Bottom line

The recorded coating readings are good enough to describe and monitor the run, but not good enough for reliable dispositions near a specification boundary. The baseline grand mean was **219.7996 µm** against the charter target of **220.0 µm** [steps 4 and 1]. The accepted interval is **180.0–260.0 µm** [step 1]. No baseline reading was outside that interval, and the corrected baseline capability was strong: **Cpk = 1.637896** and **Ppk = 1.631247** [steps 5 and 9].

That process conclusion carries a material measurement qualification. The crossed gauge study had **90** readings from **3** operators, **10** parts, and **3** replicates [step 3]. Its **15.541734%** study variation and **8** distinct categories cleared the steward's discrimination gate, but the estimated gauge variation was **8.646092 µm**, or **64.845690%** of the **80.0 µm** tolerance [step 3]. Repeatability, not operator reproducibility, dominated the gauge variance [step 3]. Gauge improvement is therefore the first intervention priority.

The monitoring record kept since the process change shows an important improvement in dispersion, but the process owner supplied no routable fact identifying the physical change. The report quantifies the change and stops there; it does not guess at a cause.

## Evidence inventory

The steward released **5** batches and denied none [step 35]. The project used the charter, the crossed gauge study, the **125**-reading baseline run in **25** subgroups of **5**, the applicator sample of **60** readings in **4** groups of **15**, and the post-change record of **100** readings in **20** subgroups of **5** [steps 1, 3, 4, 12, and 25].

Two requests to the process owner for a process fact were unroutable; the inventory records **2** fact requests, and the engineer reported no recorded matching topic [step 35]. Thus the identity, location, and mechanism of the intervention are **not established by task evidence**. All statements below about the change are limited to the statistical contrast between the labeled baseline and monitoring batches.

---
cat >> /workspace/report.md <<'MD'

## Measurement system

The balanced crossed study used **90** readings: **3** operators, **10** parts, and **3** replicates [step 3]. Its estimated gauge standard deviation was **8.646092 µm**, compared with total study standard deviation of **55.631448 µm** [step 3]. The gauge contributed **15.541734%** of study variation and distinguished **8** categories [step 3], so the steward's discrimination precondition was cleared.

That result does not qualify the gauge for boundary decisions. The gauge variation consumed **64.845690%** of the **80.0 µm** tolerance [step 3]. Repeatability contributed **97.091389%** of the gauge variance and operator reproducibility **2.908611%** [step 3]; the estimated operator-by-part interaction variance component was zero after truncation [step 3]. The practical priority is therefore to reduce short-term measurement variation, starting with the instrument and measurement method rather than operator training.

---

## Baseline run

### Stability and shape

The baseline contained **125** readings in **25** subgroups of **5** [step 4]. Its Xbar chart centered at **219.7996 µm**, with limits at **208.928920** and **230.670280 µm**; the R center line was **18.8400 µm** with upper limit **39.827760 µm** [step 4]. There were **0** Xbar signals, **0** range signals, **0** two-in-three zone-A signals, and **0** eight-point same-side signals [step 4]. A regression of subgroup means on sampling order also found no significant trend (p = **0.410652**) [step 8].

The individual readings showed no material normality concern (Anderson-Darling p = **0.554407**) and near symmetry (skewness = **-0.018406**) [steps 6 and 5]. These results support using the normal capability calculations below.

### Location and capability

The baseline mean was **219.7996 µm**, median **218.9200 µm**, and overall standard deviation **8.132757 µm** [step 5]. The mean was only **0.200400 µm** below target [step 5], and a target test gave p = **0.783394** [step 29]. Observed minimum and maximum were **199.6400** and **240.5400 µm** [step 5]; **0%** of readings fell outside the accepted interval [step 5].

Against the full accepted interval, Cp was **1.646143**, Cpk **1.637896**, Pp **1.639460**, and Ppk **1.631247** [step 9]. Within-subgroup and overall standard deviations were **8.099742** and **8.132757 µm** [step 9], confirming that centering—not a special cause or drift—is the dominant process-performance feature. Although these point estimates are strong, boundary dispositions remain limited by the gauge result above.

---

## Applicator comparison

The separate applicator sample was balanced: **4** groups and **60** readings, with **15** readings per group [step 11]. Group means were **219.2320 µm** for nozzle A, **221.0333 µm** for B, **218.2307 µm** for C, and **221.0733 µm** for D; the pooled-sample mean was **219.8923 µm** [step 12]. Their sample standard deviations were respectively **3.720070**, **4.019955**, **4.109410**, and **6.321489 µm** [step 12]. Nozzle D had the largest observed spread, but that description alone does not establish a special cause.

The assumption checks did not identify a problem with the parametric comparison: the Brown-Forsythe/Levene test gave p = **0.196475** [step 13], and residual normality gave p = **0.711926** [step 14]. One-way ANOVA then gave p = **0.265242** [step 15], and the confirmatory Kruskal-Wallis test gave p = **0.190660** [step 16]. Neither global test detects an applicator effect in these data.

**Business action:** do not redirect applicators or change nozzle assignments on this evidence. The applicator study can rule out a detectable mean effect at the scale of this sample, but it does not prove the nozzles are identical and is not a substitute for the gauge improvement identified above.

---

## Post-change monitoring record

The post-change batch contained **100** readings in **20** subgroups of **5** [step 25]. Judged against the unchanged baseline Xbar/R limits, it had **0** Xbar signals and **0** range signals [step 25]. Re-derived from its own **20** subgroups, its Xbar center was **220.5499 µm**, limits were **212.721741** and **228.378059 µm**, its range center was **13.5670 µm**, and range upper limit was **28.680638 µm** [step 26]. These own-limit charts also showed **0** Xbar signals, **0** range signals, **0** zone-A pattern signals, and **0** eight-point same-side signals [step 26]. The monitoring batch therefore remained in statistical control on the calculations run here.

The post-change readings showed no material normality concern (Anderson-Darling p = **0.743230**) [step 24] and no significant time trend across monitoring subgroups (p = **0.658608**) [step 28]. The mean was **220.5499 µm**, median **220.8750 µm**, and standard deviation **5.838914 µm** [step 23]. The mean did not differ detectably from target (p = **0.348595**) [step 30]. The minimum was **206.7700 µm**, maximum **232.2200 µm**, and **0%** of readings fell outside the accepted interval [steps 23 and 27].

Using the same 180–260 µm interval, post-change Cp was **2.285939**, Cpk **2.254513**, Pp **2.283529**, and Ppk **2.252137** [step 27].

## What the labeled change achieved—and what remains unknown

The direct before/after mean comparison found only a **0.750300 µm** increase, from **219.7996** to **220.5499 µm**, with p = **0.422045** [step 31]. The Mann-Whitney confirmation also found no significant location change (p = **0.393513**) [step 33]. Thus there is no evidence of a meaningful center shift.

Dispersion did change. The Brown-Forsythe/Levene comparison gave p = **0.003567** [step 32]. Overall standard deviation fell from **8.132757** to **5.838914 µm**, a **28.204978%** reduction; range bar fell from **18.8400** to **13.5670 µm**, a **27.988323%** reduction; and post-change variance was **51.545252%** of baseline [step 34]. Ppk increased by **0.620890**, from **1.631247** to **2.252137** [step 34]. These are material, statistically supported improvements in observed variability.

The report must stop before naming a cause. The steward's process-owner route had **2** attempts and **0** recorded process-fact topics [step 35]. No released record identifies what physical or procedural change occurred, where it was applied, or when it took effect. Accordingly, this evidence does not establish which setting should be replicated beyond saying that the monitored condition should be preserved and its engineering record recovered.

---

## What should change next

1. **Fix the gauge first.** Reduce repeatability, which supplies **97.091389%** of estimated gauge variance [step 3]. Quarantine boundary dispositions until the estimated gauge variation is materially below **64.845690%** of tolerance [step 3]. Recalculate both gauge metrics after any instrument, fixture, or procedure change.
2. **Freeze and document the monitored condition.** Preserve relevant settings, operator/method details, material lots, and timing. Recover the missing engineering change record before trying to replicate the condition that produced the **28.204978%** standard-deviation reduction [step 34].
3. **Keep the Xbar/R plan.** Continue subgroups of **5**, using the post-change center and limits [step 26], and add the documented supplemental zone and run rules used here [step 26]. Rebaseline only after a stable period and an improved gauge study.
4. **Take no applicator action now.** The global comparisons did not detect a mean effect [steps 15 and 16]. Revisit nozzle D only if the improved gauge shows excess short-term spread; its baseline sample SD was **6.321489 µm** [step 12], which is an observation, not a cause.
5. **Hold the gains with explicit acceptance criteria:** no Xbar/R signal, mean centered at **220.0 µm**, and Ppk at least the post-change **2.252137** while a repeat gauge study confirms fitness [steps 1, 26, and 27]. Define what action follows if either capability or gauge performance deteriorates.

## Limitations

- **Cause and effect are not causally identified.** The change label precedes the monitoring record, but no released fact says what changed. The variance reduction could be confounded with time, lot, material, environment, or measurement changes.
- **Boundary decisions are constrained by the gauge.** Although observed baseline and post-change out-of-range percentages were **0%** [steps 5 and 27], the gauge consumes most of the tolerance [step 3].
- **Capability estimates are conditional.** They are sample estimates under a normal model supported here [steps 6 and 24], and they include measurement variation. They are not guarantees about future production.
- **The applicator comparison addresses location, not spread.** ANOVA and Kruskal-Wallis test location/rank effects [steps 15 and 16]; the observed nozzle SDs [step 12] do not establish a formal spread difference. The Brown-Forsythe test across all four groups was not significant [step 13].
- **No batch was denied, but the intervention fact was unavailable.** The engineering identity of the change therefore remains missing, and the conclusion intentionally stops there.
