# Coating Thickness Project Report

## 1. Charter and acceptance range

The process target is **220.0 um**, with an accepted range of **180.0 to 260.0 um**.

## 2. Measurement system (MSA)

The released repeat-readings study contains **3 operators x 10 parts x 3 replicates** (90 measurements).

A crossed gage R&R was computed from those data:

- Percent study variation (`percentStudyVariation`): **44.438146%**
- Percent tolerance (`percentTolerance`): **54.843789%**
- Number of distinct categories (`ndc`): **2**

The steward gate for proceeding to the process-run data is the MSA acceptance criterion. Our computed `grr_pct` is **54.843789%**, and `ndc` is **2**. The measurement system does **not** pass the gate.

### Conclusion on gage capability

The recorded thickness readings from this gauge cannot carry a conclusion about the process. The gage R&R is too high and the number of distinct categories is too low; measurement variation would overwhelm process variation.

## 3. Process behaviour across the run and capability to specification

No process-run data were released. The batch _Thickness readings in sampling order, five to a point_ remains locked because the MSA gate failed (`grr_pct` did not meet the acceptance criterion). Therefore, no computation can be made for:

- how the line behaved across the run;
- where coating thickness sits against 180-260 um;
- applicator-to-applicator differences;
- monitoring record since the change.

There is no data for these steps, and the conclusion stops here rather than relying on guesses.

## 4. What should change next

The next action is not to adjust the process first, but to improve the measurement system. The plant should:

1. Investigate why gage R&R is above the acceptance criterion (`grr_pct = 54.843789%`).
2. Retrain operators and standardise the thickness-gauge method.
3. Inspect and maintain the gauge/fixture and repeatability conditions.
4. Rerun the MSA before collecting or using process-run data, with an acceptable `grr_pct` and an improved number of distinct categories.

Once the measurement system passes, the line, applicator, and monitoring batches should be released and analysed.
