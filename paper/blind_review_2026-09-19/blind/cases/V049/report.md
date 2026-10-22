# Seal Ring Strength Project Status

## Data released through the steward
The data steward released three batches:

- programme charter and seal-strength requirement (define);
- sixty consecutive seal-strength baseline assemblies, in build order;
- the two-level screening run over three assembly settings, with two replicates.

The later composite-design batch and the twenty seals made at the recommended settings could not be released during this analysis (see the screening conclusion below).

## How the line has behaved across the baseline
Sixty consecutive assemblies were tested.  The baseline mean seal strength is **52.3485 N**, the median is **52.81 N**, and the sample standard deviation is **3.8147 N**.  The normality test p-value is **0.8943**, so there is no evidence against a normal distribution for the baseline data at conventional significance levels.

The individual-moving-range chart has center line **52.3485 N**, upper control limit **63.3830 N**, lower control limit **41.3140 N**, and flagged count **0**.  No baseline point falls outside the individual-chart control limits.

## Where seal strength sits against requirements
The lower specification from the programme charter is **45.0 N**, and the committed product level is **55.0 N**.

- **1 of 60** baseline assemblies (1.67%) fell below the **45.0 N** lower specification.
- **45 of 60** baseline assemblies (75.0%) fell below the **55.0 N** committed level.

A one-sample t-test against **45.0 N** gave t = **14.9217** and one-sided p = **5.4479e-22**, so the baseline mean is significantly above the lower specification.  Against the committed **55.0 N**, t = **-5.3841** and one-sided p = **0.999999338**, so the baseline mean is not significantly above the required level.  This aligns with the fact that most baseline assemblies are below the 55 N target.

The lower-spec normal capability indexes are **cp = cpk = 0.665955** and **pp = ppk = 0.642127**.  These values indicate that the line is not capable against the lower specification, let alone at the 55 N commitment.

## Whether the varied settings account for seal strength
The screening run was a 2^3 factorial in **bond_angle**, **bead_spacing**, and **cure_temperature**.  The full factorial model produced model p-value = **0.833516** and R-squared = **29.0464%**.  The smallest individual-effect p-value was **0.2869**, and no term approached significance.

Therefore the three settings that were varied do **not** account for the seal-strength variation seen in the screening run.

## What the design work supports concluding
The design work supports stopping the current screening path: the three chosen factors are not the drivers of seal strength.  The steward gate for the next batch required `any_factor_significant=true`; our honest computed result is `any_factor_significant=false`, so the composite design and the subsequent seals made at recommended settings were locked and could not be obtained.  There is no data for those later stages, and the conclusion must stop there rather than invent parameter recommendations.

## What should happen next
- The line currently does not meet the committed 55 N seal-strength target; it is also not statistically capable at the 45 N lower specification.
- The screened factors (bond angle, bead spacing, cure temperature) did not account for the variation, so a composite design around those two settings is not justified by this experiment.
- The team should broaden the search to additional process inputs (for example material, pre-treatment, assembly handling, curing orientation, or measurement methods) and run a new screening study.
- Baseline SPC should continue until the process is understood and stabilised; one baseline point below 45 N is already unacceptable.
