# Void-fraction project status

## Executive conclusion

The measurement system is usable for this study. The crossed repeat-reading study used 108 readings from 3 operators, 12 parts, and 3 replicates. Its computed gage R&R results were 19.579787400305115% study variation, 14.39670975513979% tolerance, and ndc 7.061917468066983. On that basis, the process data can be evaluated, with the important qualification that the process itself is not stable.

The released build-order run contained 50 joints. Every one of the 50 readings was within the charter limits of 0.0 to 25.0 percent void area; the observed range was 6.31 to 17.7. This is an acceptance result for the run, not proof of a controlled process.

## What the line did

The overall mean was 11.828199999999999 and the median was 11.235, with standard deviation 3.0870312599648226. The ordered run is not random: the runs-test p-value was 4.822134315143417e-06, based on 10 runs, and the individuals chart flagged 5 points. The chart center line was 11.828199999999999, with limits 7.1330285714285715 and 16.523371428571426.

The sequence also shows a sustained upward shift. The mean of the first 25 readings was 9.176799999999998 and the mean of the second 25 was 14.479599999999998, a difference of 5.302799999999999. The executed normality test returned p-value 0.010893005178885098 and statistic 9.03926884489909, so the combined run should not be treated as a single normal, stable population.

## Capability and voiding limit

The computed overall indices were Cp 1.3497325798748623, Cpk 1.2771925521020675, Pp 1.3497325798748623, and Ppk 1.2771925521020675. Because the runs test and individuals chart show instability, these indices are provisional and should not be used to claim sustained capability. No reading exceeded the 25.0 percent upper limit in the released run, but the upward shift is a warning that future performance could differ from this aggregate result.

## Cause, change, and achieved result

The data support an order-related process shift, not a specific physical cause. The run begins at a lower level and later operates at a higher level; the data supplied contain no lot, machine, tool, recipe, operator, timestamp, or intervention labels that would identify what changed. Therefore the responsible cause cannot be isolated from this batch.

No process improvement or before/after batch was released. Consequently, there is no computed change to report and no computed improvement achieved. The only demonstrated result is that all 50 released readings met the current limit while the sequence was unstable.

## Recommended next action and control

1. Preserve the build-order sequence and add time, lot, machine, recipe, tool condition, operator, and intervention fields to every reading.
2. Investigate the transition associated with the sustained level increase before changing settings; use the chart-flagged observations as review points rather than deleting them.
3. After the assignable cause is addressed, collect a new ordered run and recompute stability and capability separately for the resulting conditions. Do not pool unlike conditions.
4. Hold the process with an individuals/moving-range chart and a documented reaction plan for any signal. Continue periodic verification of the measurement system using the established repeat-reading study design.

The project therefore stands at **Measure/Analyze**: the measurement system is adequate and the current batch meets the voiding limit, but the process is not yet demonstrated to be stable or sustainably capable.
