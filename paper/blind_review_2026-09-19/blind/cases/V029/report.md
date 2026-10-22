# Brightness Line Improvement Project Report

## Data used
The released records were the project brightness requirement, the operator repeat-reading study, and the per-unit end-of-line record. Post-change or improvement-verification data were requested, but the steward refused the request as unroutable and stated that no such data topic exists for this project. Therefore no change effect can be computed.

## Can the recorded readings be relied on?
A crossed Gage R&R analysis used 3 operators, 10 parts, 3 replicates, 90 measurements, and a tolerance of 200.0 cd/m².
- Percent study variation: 13.984264130461085%.
- Percent tolerance: 14.259033002220269%.
- Number of distinct categories: 9 (raw 9.983685666830777).
- GRR standard deviation: 4.75301100074009 cd/m².
- Repeatability variance: 21.241249330888724; interaction variance: 1.3498642422675833; operator variance: 0.0; GRR variance: 22.591113573156306; part variance: 1132.6121377391812; total variance: 1155.2032513123374.
- Variance contribution: repeatability 1.8387456325766203%, interaction 0.11685080012838489%, operator 0.0%, GRR 1.9555964327050053%, part 98.044403567295%.

The readings are usable for process-level decisions, but the measurement system is marginal and not strong enough for high-confidence individual-unit decisions. Repeatability is the dominant GRR component.

## How has the line behaved over the run?
The released sequence contained 50 units.
- Mean: 446.86600000000004 cd/m².
- Median: 446.85 cd/m².
- Overall standard deviation: 23.58527394241533 cd/m².
- Skewness: -0.13349201373014186.
- Anderson-Darling p-value: 0.9179899086225278.
- Shapiro-Wilk p-value: 0.8243790243885181.
- I-MR center line: 446.86600000000004; individuals UCL: 509.43656013894923; individuals LCL: 384.29543986105085; flagged points: 0.
- Moving range center line: 23.526530612244894; moving range UCL: 76.86117551020406; within sigma: 20.85685337964973.
- OLS trend slope: 0.07685474189675591 per unit; trend p-value: 0.7432313497928538; R-squared: 0.2256412107087713%; adjusted R-squared: -1.8529912640681268%.
- Pearson correlation: 0.0475017063597499; p-value: 0.7432313497928463.

The process was stable across the released run. No special-cause points and no significant drift or correlation with production order were detected.

## Where does brightness sit against the accepted range today?
The accepted range is LSL 350.0 and USL 550.0 cd/m², width 200.0, midpoint 450.0.
- Below LSL: 0 units.
- Above USL: 0 units.
- Outside spec: 0 units (0.0%).
- Cp: 1.5981956974323388; Cpk: 1.54810824427481; Pp: 1.4133112642540593; Ppk: 1.3690180892323376.
- One-sample t against 450.0 cd/m²: t-statistic -0.9396001325442588, p-value 0.3520316394297086.

The released process is centered near the midpoint and has good capability against the accepted range, with no observed out-of-spec readings. The sample is 50 units, so this describes the released run rather than a guaranteed future population.

## What was changed and what did the change achieve?
No post-change or improvement-verification batch could be obtained. The steward refused the corresponding request as unroutable and stated that no such data topic exists for this project. That is a missing-data gap. No process change effect can be estimated, and this report does not claim one.

## What should be changed next?
The next change should be in the measurement and monitoring system, not in a production brightness setpoint unsupported by the data.
- Reduce measurement repeatability through a controlled fixture and standardized operator technique, because repeatability is the largest GRR component.
- Re-run the crossed Gage R&R after that measurement improvement and compare percent study variation, percent tolerance, and number of distinct categories against the values above.
- Continue I-MR monitoring of per-unit brightness readings to hold the stable state.
- Create a post-change sampling batch and a pre-specified comparison so the next report can compute what the change achieved.
