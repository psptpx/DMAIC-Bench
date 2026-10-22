# Seal Strength Project Report - [TASK]

## Data batches examined
- Programme charter / seal requirement: LSL = 45.0 N; committed product margin target = 55.0 N.
- Baseline assembly-by-assembly seal strengths: 60 values in build order.
- Screening run: 16 runs over three coded factors (bead spacing, bond angle, cure temperature).
- Composite design: 13 runs over two factors (bead spacing, bond angle), centre run five times.
- Confirmation seals made at the recommended settings: 20 values.

## Baseline performance
Baseline seal strength averaged 52.08 N (median 51.80 N, standard deviation 4.30 N, range 41.08 to 62.92 N).  The distribution is consistent with a normal distribution (Shapiro-Wilk p = 0.676).  Against the lower specification of 45 N, the baseline mean is significantly above the limit (one-sample t = 12.75, p < 0.0001).  However, 4 of 60 seals fell below 45 N and 41 of 60 fell below the 55 N committed margin.  The one-sample t-test against 55 N is not significant in the desired direction (t = -5.27, p > 0.999), meaning the line has not demonstrated that the mean seal strength is above the programme margin.

From an IMR chart in build order, the baseline process centre is 52.08 N with individual limits 39.40 to 64.75 N and 0 flagged points.  The process is stable but centred too low relative to the 55 N target.  Lower-specification capability is Cpk = 0.558 and Ppk = 0.553, both below what the business needs.

## Factors contributing to seal strength
The screening run full-factorial model is significant (F = 21.32, p = 0.000142) and explains 94.91% of the variation.  Among the three varied settings, bead spacing and bond angle, and their interaction, dominate the explanation.  Cure temperature is not a significant main effect in this screening experiment.

## What the composite design supports concluding
The two-factor response-surface model explains 98.02% of the composite-design variation and predicted a maximum seal strength of 64.28 N at the optimised coded settings.  However, the lack-of-fit test for the quadratic response surface is significant (p = 0.0019), so the model should be used with caution; the high R-squared does not fully remove uncertainty about the exact response surface shape.  The centre-point mean in the composite design was 57.93 N.

## Confirmation seals at the recommended settings
The 20 confirmation seals made at the settings recommended by the design work averaged 59.27 N (standard deviation 1.98 N, range 56.41 to 63.24 N).  None fell below the 45 N lower limit and none fell below the 55 N target.  The confirmation mean is significantly above 55 N (one-sample t, p < 0.0001) and above 45 N (p < 0.0001).  Lower-specification capability improved to Cpk = 2.410 and Ppk = 2.466.

Comparing baseline and confirmation results, the confirmation mean is significantly higher than baseline (Welch two-sample t = -10.14, p < 0.0001; Mann-Whitney p < 0.0001).

## Where this project stands and next steps
The baseline line was stable but not capable of meeting the committed 55 N margin; it was at increased risk against the 45 N minimum.  The screening and composite design work identified bead spacing and bond angle as the key levers, and the confirmation run at the recommended settings shows all 20 seals above both limits with substantially improved capability.  Because the response-surface model has significant lack of fit, the current recommended settings should be treated as a strong starting point rather than a fully validated optimum.  Next steps should include: (1) run additional confirmation samples over time and across operators/shifts to verify the improvement is sustained; (2) consider a final follow-up DOE around the recommended bead-spacing/bond-angle region to resolve the lack-of-fit uncertainty; and (3) put an SPC or regular capability monitoring plan on seal strength at these settings.
