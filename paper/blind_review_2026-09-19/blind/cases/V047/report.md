# Project status report

## Bottom line

The requested bore-roughness conclusion **cannot be made**. The steward released **3** batches, but **0** roughness batches. The released records describe **percent void area** for joints, with limits **0** to **25**, not honing-line bore roughness Ra with limits **0.40** to **1.60** and target **1.00**. The evidence therefore addresses a different characteristic from the one requested.

The released measurement study also fails. Its estimated Gage R&R is **48.80%** of study variation, **64.10%** of tolerance, with **2** distinct categories. The computed verdict is that the measurement system is not acceptable. Repeatability accounts for **100%** of estimated measurement variance; estimated operator and interaction variance components are each **0**. Consequently, the void-fraction results are observations from an unreliable gauge, not confirmed product quality.

## Can these readings carry a conclusion?

No, not for acceptance of individual joints. The balanced study used **108** readings: **3** operators, **12** joints, and **3** replicates. Its large repeatability component and low distinct-category result mean differences between joints cannot be distinguished reliably. Any process capability statement below is therefore conditional and must not be used as an independent acceptance conclusion.

## Conditional baseline of the released void record

These results apply only to the released percent-void-area sequence, not to bore roughness. The sequence contains **50** joints in build order.

| Conditional baseline result | Computed value |
|---|---:|
| Mean | **10.2266** |
| Median | **10.4300** |
| Overall standard deviation | **2.2064** |
| Skewness | **0.2427** |
| Anderson–Darling normality p-value | **0.4437** |
| Shapiro–Wilk statistic / p-value | **0.9822** / **0.6493** |
| I-MR center line | **10.2266** |
| I-MR lower / upper control limit | **4.3981** / **16.0551** |
| Points beyond individual control limits | **0** |
| Cp / Cpk | **1.9016** / **1.5557** |
| Pp / Ppk | **1.8884** / **1.5450** |
| Observed below lower limit / above upper limit | **0** / **0** |

Thus, as calculated from the released values, the void sequence is approximately normal and has no point outside its I-MR limits or the stated 0-to-25 band. I did not evaluate supplemental run or pattern rules, so this is not a broader claim of chart stability. More importantly, the failed gauge means these capability figures are conditional descriptions of the recorded data, not evidence that individual joints are acceptable.

## Where the evidence stops

The steward made **3** released batches available, but **0** batches containing the requested roughness readings and **0** improvement-stage batches. Requests outside the released topics were `unroutable`, not `denied` record batches; nevertheless, status and routing showed that no such batch existed to request. Two provision calls found no configured process-fact topic.

Therefore:

- There is **no Ra reading** from which to assess honing performance against 0.40, 1.60, or target 1.00. The roughness conclusion stops here.
- There is **no root-cause data** and no computed cause. No causal statement can be made.
- There is **no baseline/post-change designation or post-change record**, and no process-change fact. What was changed, when it changed, and what any change achieved cannot be computed.
- The void baseline is the end of the available quantitative process story, and it rests on an unacceptable gauge.

## Where voiding sits against its acceptance limit today

For the released 50-joint sequence, **0** observations are below the lower limit of **0** and **0** are above the upper limit of **25**. The computed overall Ppk is **1.5450**. That result is conditional on the failed gauge and describes only the released sequence.

It cannot be promoted to a current-process conclusion: the released run has **no timestamps**, and there is no process-change evidence or post-change record. Where voiding sits **today** is therefore not computable from the held data.

## What should change next

1. **Stop using the current readings as acceptance evidence.** First qualify or replace the measurement system and repeat a balanced study after corrective action.
2. **Obtain the correct characteristic.** Ask the data steward specifically for the honing-line Ra record in finishing order. Do not substitute the released void-fraction record for it.
3. **Re-baseline only after the gauge passes.** With acceptable measurement error, assess Ra against 0.40, 1.60, and target 1.00 in production order.
4. **Control any change as a change.** Define the cause to be tested, designate pre-change and post-change runs, record the intervention and timestamp, and verify it with follow-up data. None of those items is currently held, so no cause, change, or improvement effect can be claimed today.
5. **Hold the line by charting the correct Ra measurement** with an approved gauge, documented reaction rules, and periodic measurement-system checks.
