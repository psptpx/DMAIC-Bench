# Wave-soldering fillet-height project report

## Business position

The accepted fillet-height range is 6.80 to 7.50 mm, with 7.15 mm as target. At the 0.05 decision standard, the baseline is centered and stable in the recorded sequence, but it does not have enough margin within the accepted range. The designed run identifies chain speed and rail angle—and their interaction—as significant contributors to fillet height. The later process log does not show that the three uncontrolled logged variables explain fillet height. The labeled after-change window did not demonstrate a credible mean shift, but it did show materially greater short-term and overall spread. The exact physical change cannot be identified from the available data; the process-fact requests returned no matching fact, so causal attribution for the window-to-window difference stops there.

## Baseline behavior

The baseline record contains 60 consecutive joints. Its mean is 7.16048 mm, median is 7.1765 mm, and standard deviation is 0.139507 mm. No joint is below the 6.80 mm lower limit and none is above the 7.50 mm upper limit.

An individuals chart has a center line of 7.16048 mm, upper control limit of 7.57046 mm, and lower control limit of 6.75050 mm. Zero points exceed those limits. The Anderson-Darling normality p-value is 0.535813, the time-order correlation is 0.152514 with p-value 0.244691, and a one-sample test against the 7.15 mm target gives p-value 0.562735. There is therefore no demonstrated normality violation, linear time trend, or offset from target.

The capability problem is spread rather than centering. Baseline Cp is 0.853700, Cpk is 0.828129, Pp is 0.836276, and Ppk is 0.811227. Although production remained inside the accepted range in this sample, the low indices show that ordinary variation leaves little protection and that wider variation can produce nonconforming fillets.

## What accounts for fillet height

The replicated two-level, three-factor designed run has 16 observations. Its full factorial model p-value is 0.0000768869 and it explains 95.6501% of the response variation. In coded units, the chain-speed coefficient is 0.144331 mm, the rail-angle coefficient is 0.092856 mm, and the chain-speed-by-rail-angle coefficient is 0.047994 mm. Chain speed has factorial p-value 0.00000578114 and rail angle 0.000141818; their interaction has p-value 0.00807677. In contrast, air pressure has p-value 0.0652331 and is not significant at 0.05.

These experimental results support chain speed and rail angle, not air pressure, as the settings that account for fillet-height differences in the designed run. They explain the designed contrast; they are not alone a proof that they explain all common-cause variation in the separate 60-joint baseline.

The three variables merely logged through the run do not provide a competing explanation. A joint OLS model using preheat-zone temperature, conveyor-width setting, and solder-pot dwell has 48 observations, p-value 0.893105, and R-squared of only 1.37157%. Their individual correlations have p-values 0.532133, 0.657482, and 0.655030. None is significant at 0.05.

## Before-versus-after change

Each labeled window contains 30 joints. The mean moves from 7.15667 mm before to 7.1957 mm after, while the standard deviation increases from 0.103152 mm to 0.147313 mm. Normality is not rejected in either window.

The variance-equality test is significant, with statistic 5.57004 and p-value 0.0216554. The mean increases by 0.0390333 mm after the change, with confidence interval from −0.0268545 to 0.104921 mm and Welch p-value 0.239919. A Mann-Whitney check similarly gives p-value 0.359308. Therefore the data do not demonstrate a credible mean change; they do demonstrate increased dispersion.

Capability deteriorates in the after window. Before it, Cp is 1.12645, Cpk is 1.10499, Pp is 1.13102, and Ppk is 1.10948. After it, Cp is 0.735054, Cpk is 0.639077, Pp is 0.791962, and Ppk is 0.688554. Again, no observed joint in either 30-piece window lies outside the accepted range. The loss of margin is a leading indicator and should be treated as a process-risk finding, not dismissed because zero defects were observed.

The labels establish sequence, but not mechanism. The process-fact requests returned no matching fact, so the exact setting—or even the physical nature—of what was changed cannot be computed or named. Consequently, the increase in variation cannot be causally assigned to that change from these data.

## Recommended actions

First, stop treating the current condition as acceptable merely because the observed samples contain zero out-of-spec joints. Investigate the after-window spread increase and restore traceable records identifying every line setting. Until that mechanism is documented, report only a temporal association with the after window, not a proven effect.

Second, run a controlled confirmation of the designed-run direction: high chain speed, low rail angle, and air pressure centered at its coded value. The full factorial prediction at those coded settings is 7.16968 mm, with interval 7.02827 to 7.31108 mm for a new observation. Translate the coded settings into their actual engineering units before operation; those units were not part of the released design data and cannot be inferred here. Confirm the result on subsequent production rather than assuming the prediction.

Third, continue an individuals chart and recompute capability on a defined next sample. Release further change only after spread returns to at least the before-window level, the selected settings remain on target, and the chart remains free of control signals. Record actual settings and any intervention in the batch history so the next investigation can distinguish cause from sequence.
