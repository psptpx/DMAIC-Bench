# Quality improvement project status

## Executive assessment
The accept/reject system was not initially dependable. Rewriting the inspection criteria was the necessary measurement-system intervention before interpreting production rejects. The retained-board recheck now supports using the calls, with ongoing audits. The production history is stable under the basic point-limit chart rule, but stability is not compliance: the observed reject share is **3.11%**, above the **2%** requirement. The higher-reject placement head is the next investigation priority, not yet a proven root cause.

## Measurement: what changed and what it achieved
The initial study contained 120 ratings on 20 retained boards. Overall agreement with the key was 73.33%; minimum appraiser Cohen kappa was 0.2857. Appraiser agreement was 70%, 67.5%, and 82.5%; repeatability was 60%, 55%, and 75%. These results do not support relying on the original visual calls.

The separate disagreement tally contained 90 items. Insufficient solder accounted for 47.78%, the largest category, followed by tombstone at 17.78%, component offset at 14.44%, wrong polarity at 12.22%, and solder bridge at 7.78%. This is a Pareto of disagreement with the key, **not** a Pareto proving the causes of production defects. It justified prioritizing clearer accept/reject examples, particularly solder adequacy. This separate tally should not be treated as the count of mismatches in the retained-board rating matrix.

After the criteria were rewritten, agreement rose to 99.17% and minimum kappa to 0.9419. Appraiser agreement was 100%, 100%, and 97.5%, with repeatability of 100%, 100%, and 95%. Kappa was calculated against the key separately for each appraiser, pooling repeat ratings; overall agreement is the fraction of all ratings matching the key. The recheck supports operational use, not a guarantee of perfect field inspection: retained boards and repeated ratings are not independent samples of all future production. Maintain the rewritten standard, boundary examples and inspector calibration. The data demonstrate improved measurement, not a reduction in physical defects.

## Process stability and requirement
Across 25 lots, 311 of 10000 inspected boards were rejected. A binomial p chart has center line 0.0311, lower limit 0.005062 and upper limit 0.057138, with 0 points outside the limits. This is evidence of common-cause behavior under the point-limit rule, not proof that every possible run-pattern test passes. Board independence and consistent classification are assumptions; the archive does not establish the timing of these lots relative to the criteria change.

Binomial capability gives average reject share 3.11%, or 1.555 times the required level. The unshifted yield-equivalent process Z is 1.8649; continuous-data capability indices are inappropriate for these counts. An exact upper-tail binomial test against the required share gives p = 1.253e-13, supporting that the underlying level exceeds the requirement if the sampling assumptions hold. The archive-wide estimate describes the observed window, not a separately measured current-day rate. Do not confuse control limits with the customer requirement.

## Placement-head evidence and next action
The head comparison window contains 128 rejects among 3000 placements for the first head and 74 among 3000 for the other. The rates are 4.2667% and 2.4667%, a difference of 1.8000 percentage points. A pooled, two-sided proportions test gives z = 3.8650, p = 0.000111069. The higher rejection rate merits a focused investigation of the first head.

This observational comparison cannot separate head condition from board mix, component mix, setup, operator, or time. Placement denominators also must not be conflated with inspected-board denominators. Inspect alignment, nozzle condition, feeders and setup records; stratify comparable jobs and confirm the mechanism before choosing a corrective action. Use a controlled matched-job trial where practical and verify both placement and final-board rejection afterward.

## Hold the gains and close the project
Quality should own version-controlled criteria, retained boundary samples, refresher training and periodic blinded agreement checks. Production engineering should own the head investigation and documented corrective trial. Continue lot-level p-chart monitoring with the validated inspection method; investigate signals rather than adjusting a stable process at random. After a verified physical process change, collect a fresh ordered lot series and reassess stability and compliance before resetting limits or claiming closure.

No physical head correction or post-correction production study was supplied, so no achieved production improvement or sustained compliance can be claimed. No batch was denied; the owner supplied no additional process facts in response to the criterion question. Mechanical root cause, comparability of head workloads, measurement-change chronology and present-day performance remain unverified. The project has qualified its inspection method and identified an actionable association, but has not yet demonstrated that the line meets its requirement.
