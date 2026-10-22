# Honing Line Void-Fraction Project Report

## 1. Data obtained

This project used three batches released by the data steward:
- project charter and voiding limit (`define`);
- repeat X-ray readings of the same joints (`msa`);
- per-joint void fraction in build order (`process_run`).

No requested data batch was denied.

## 2. Can the recorded readings carry a conclusion?

The repeat X-ray study contains 3 operators x 12 parts x 3 replicates.
The crossed gage R&R results are:

- percent study variation = **19.58%**;
- percent tolerance = **14.40%**;
- ndc = **7**.

The measurement system is not ideal (study variation is above the common 10% ideal), but it is within a conditionally acceptable range (less than 30%) and the ndc is 7, above the usual minimum of 5. Therefore the recorded readings can carry a conclusion for process-level decisions, with the explicit caveat that measurement variation must continue to be reduced.

## 3. How the line behaved across the run

The build-order data contains **50** void-fraction readings.
The overall descriptive summary is:

- mean = **11.83**% void area;
- median = **11.23**%;
- stdDev = **3.09**%;
- skewness = **0.1667**;
- minimum = **6.31**%;
- maximum = **17.70**%.

The Anderson-Darling normality test on the 50 readings gives statistic **0.9047** and p-value **0.0195**; normality is rejected at the 5% level.

The line did not stay stable. The first 25 readings have mean **9.18**% and median **9.41**%; the last 25 readings have mean **14.48**% and median **14.57**%. A Mann-Whitney test between these halves gives p-value **2.888e-09**, confirming the two periods are not from the same location distribution.

The I-MR control chart has center line **11.83**%, upper control limit **16.52**%, lower control limit **7.13**%, and flags **5** of 50 points outside control limits. The low-side flags occur in the first portion of the run and the high-side flags occur later. Thus the process shifted upward during the run rather than holding steady.

## 4. Where voiding sits against its acceptance limit

The acceptance limit is **0.0** to **25.0**% void area.
Normal-capability indices computed from all 50 readings are:

- Cp = **1.35**;
- Cpk = **1.28**;
- Pp = **1.35**;
- Ppk = **1.28**.

However, these normal indices must be read with caution because the normality test rejected normality and the run is not statistically stable. The percentile-based nonnormal capability indices are:

- Pp(nonnormal) = **2.20**;
- Ppk(nonnormal) = **1.98**.

All individual void-fraction readings lie within specification. The current run shows Cpk/Ppk above 1.28 (normal) or above 1.98 (nonnormal), so the line is currently inside the acceptance band with margin. The risk is not near-spec location; it is instability caused by a level shift during the run.

## 5. What should change next

1. **Stabilise the line first.** The build-order data show a clear upward shift: the first 25 readings averaged **9.18**% and the last 25 averaged **14.48**%. The process team should investigate what changed between those periods and lock the factor at the setting that keeps the line on target and steady.
2. **Do not rely on normal capability until the process is stable.** The normal capability indices should be recomputed after the process is in statistical control.
3. **Continue reducing measurement variation.** The gage R&R percent tolerance is **14.40%**, above the 10% ideal, which consumes process tolerance and weakens future capability conclusions.
4. **Hold the improvement with an I-MR chart.** The current control limits are UCL **16.52**% and LCL **7.13**%. Future runs should be plotted against these provisional limits until stability is restored, then limits should be recomputed.

## 6. Gaps and limitations

No data batch was denied. The process is not statistically stable, so final capability statements should be treated as conditional. The normal capability index is reported for inspection but should not be used alone until the special causes behind the shift are removed and verified.
