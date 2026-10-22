# Yield Improvement Project - Status Report

**Task:** [TASK]
**Audience:** Plant quality manager
**Spec:** Yield accepted range is 80% to 100% (LSL = 80.0, USL = 100.0)

## 1. Can we trust the assay readings?

We pulled the analyst repeatability study (3 operators, 10 samples, 3 replicates each, tolerance = 20 percentage points) and ran a crossed Gage R&R (ANOVA method).

- %Study Variation (Gage R&R vs total variation): **23.16%**
- %Tolerance (Gage R&R vs the 20-point tolerance): **6.98%**
- Number of Distinct Categories (ndc): **5.92** (effectively 5)

By the usual AIAG bands, 23.2% %StudyVariation sits in the "marginal" zone (10-30%), while %Tolerance (6.98%) and ndc (5.9, at the 5-category minimum) both come out acceptable. Read together: the gage is not broken, but it is eating a meaningful slice of the variation we see between batches, mostly from repeatability (operator-to-operator reproducibility was small, 5.4% of study variation, vs. 22.5% from repeat readings on the same sample). **Verdict: usable for now, but tightening repeatability would sharpen every number that follows.**

## 2. How has the line behaved over the run?

Using the 30 batches production released to us (charge order), an Individuals-Moving Range (I-MR) chart shows:

- Center line (mean): **86.09%**
- Individuals control limits: **76.72% to 95.45%**
- Flagged (out-of-control) points: **0**

The process is **statistically stable** — no batch fell outside its own control limits and no special-cause signal appeared over these 30 charges. Whatever is holding yield down is a *common-cause*, built-in feature of the process, not a one-off upset.

We also checked the shape of the yield distribution: mean 86.09%, median 86.15%, standard deviation 2.86, skewness 0.17 (nearly symmetric), and an Anderson-Darling normality test p-value of 0.97 (Shapiro-Wilk p = 0.99). The data behaves like a normal distribution, so the capability numbers below are computed on solid statistical footing.

## 3. Where does yield sit against the 80-100% requirement today?

- Cp = **1.07**, Cpk = **0.65**
- Pp = **1.17**, Ppk = **0.71**

Cp/Pp above 1.0 says the *spread* of the process would just about fit inside the 80-100 window if it were perfectly centered. But Cpk and Ppk sit well under the usual 1.33 capability benchmark, and both are dragged down by the *lower* spec limit: with a mean of 86.1% and a spread of about 2.9 points, batches routinely run close enough to the 80% floor that low-yield excursions are expected, not rare. **The process is stable but not capable** — it is centered too close to its floor for the amount of variation it carries.

## 4. Does the tested setting justify more charges?

An earlier trial deliberately ran charges at a low (-1) and a high (+1) setting, 6 charges each. Before comparing means we checked whether the two groups have comparable spread: an equal-variances F-test gave F = 0.69, p = 0.70 — no evidence the variances differ, so a standard (pooled) two-sample t-test is the right tool.

- Mean yield at low setting: **90.81%** (sd 1.41, n=6)
- Mean yield at high setting: **88.95%** (sd 1.70, n=6)
- Two-sample t-test: t = **2.06**, p = **0.066**

The low setting out-yielded the high setting by about 1.9 points, and both means beat the current production average of 86.1%. But at p = 0.066 the difference misses the conventional 0.05 cutoff — with only 6 charges per arm, we do not yet have statistically firm ground to say the setting change is real rather than noise.

## 5. Bottom line for the quality manager

- **Measurement system:** usable, marginal — repeatability, not reproducibility, is the weak point; worth a tightening pass before trusting fine differences in future studies.
- **Process behavior:** the 30-batch production run is stable — no rogue batches, the shortfall is systemic.
- **Capability:** not capable against the 80-100% spec today (Cpk 0.65, Ppk 0.71); the process runs too close to the 80% floor for its own spread.
- **Setting trial:** the low setting looks promising (about 1.9 points better than high, and both above current production average) but the result (p = 0.066) is short of significance at the sample size run so far.

**Recommendation:** the setting trial result is directionally encouraging enough that abandoning it now would be premature, but it is not yet proven. Before committing to a full changeover, run a follow-up batch of charges at the low setting (larger n, to get the power the first 6-charge trial lacked) to confirm the effect is real. In parallel, address gage repeatability so the next study is not carrying an extra 20+ points of measurement noise into the comparison. Do not yet loosen or relax the 80-100% acceptance range — the capability shortfall is a process centering/spread problem, not a spec problem.

*No steps in this analysis were denied by the data steward; every figure above traces to a computed step in `trace.json`.*
