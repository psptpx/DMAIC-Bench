# Seal Strength Project Report

## Data obtained
All requested project batches were released by the steward and used for the computations below; none were denied.

## 1. Baseline line behaviour
Sixty consecutive assemblies were measured in build order. The baseline seal strengths had mean 52.09 N, median 51.36 N, and sample standard deviation 4.669 N. Minimum and maximum values were 42.88 N and 62.92 N. Normality was not rejected (Shapiro-Wilk W = 0.9805, p = 0.452). Against the product lower specification limit of 45.0 N, the baseline one-sided capability was Cpk = 0.587 and Ppk = 0.507, both below 1, so the line was not capable. An individuals control chart had centre line 52.09 N, UCL = 64.19 N, LCL = 40.00 N, and 0 out-of-control flags; this suggests the baseline line was stable but consistently too close to the lower limit.

## 2. Seal strength against product requirements
The product requires the seal to hold at least 45.0 N, and the programme margin requires strength above 55.0 N. In baseline, 3 of 60 assemblies were below 45.0 N and 41 of 60 were below 55.0 N. The line therefore did not meet either requirement at the start of this work.

## 3. Screening-run conclusions
The screening run was a 16-run two-level experiment in three assembly settings, with two replicates per corner. The full factorial model was significant (p = 0.000345, R-squared = 93.6%). Bond angle and bead spacing were significant factors (p = 3.71e-05 and p = 0.000316, respectively), and their interaction was also significant (p = 0.0195). Cure temperature was not significant (p = 0.853). This supports concluding that the settings that were varied, particularly bond angle and bead spacing, account for the seal strength.

## 4. Composite-design conclusions
The composite design over bond angle and bead spacing, with the centre run five times, consisted of 13 runs. A full quadratic response-surface model fit well: R-squared = 99.6%, adjusted R-squared = 99.3%, and lack-of-fit p = 0.575. The stationary point was predicted at 59.72 N, and the optimizer returned the same practical point at coded bond_angle = 0.760 and coded bead_spacing = 0.745, with predicted response 59.72 N.

## 5. Confirmation run at the recommended settings
Twenty seals were then made at the settings the design work recommended. The confirmation run had mean 58.607 N, median 58.68 N, and standard deviation 1.935 N. Normality was not rejected (Shapiro-Wilk W = 0.9722, p = 0.801). Minimum and maximum values were 54.62 N and 61.71 N; 0 of 20 were below 45.0 N, and 1 of 20 were below 55.0 N. Against the lower limit of 45.0 N, Cpk = 1.942 and Ppk = 2.345, so the current settings are now capable of holding at least 45 N. Against a strict individual-seal interpretation of the 55.0 N programme margin, Cpk = 0.515 and Ppk = 0.622. One-sample t-tests confirmed the mean is significantly above both 45.0 N (t = 31.456, one-sided p = 3.74e-18) and 55.0 N (t = 8.338, one-sided p = 4.5e-08).

## 6. What should happen next
1. Freeze the recommended coded settings: bond_angle = 0.760 and bead_spacing = 0.745.
2. Monitor the line with an individuals/moving-range chart going forward to hold the gain.
3. If the engineering requirement is that every seal must exceed 55.0 N, the current confirmation run shows one value below that margin and capability against 55 N is still too low (Cpk 0.515, Ppk 0.622); further work should reduce variation or shift the process higher before committing to the programme margin statement.
