# Final-inspection project status

## Bottom line

The visual accept/reject call is **usable with qualification**. It was not assumed: the first gate was an attribute measurement-system study, and its pooled appraiser-to-standard results were 115 matches among 120 calls (95.8333% agreement) with minimum kappa 0.89899. The system still had error: 3 false accepts and 2 false rejects.

Rewriting the accept/reject criteria did not prove a statistically significant accuracy gain. Accuracy rose to 117/120 (97.5%), but the 1.6667 percentage-point change had p = 0.47202. The observed false rejects fell from 2 to 0; false accepts remained at 3. Thus, the call can support project decisions, but false accepts and inconsistent trials must continue to be managed.

The full 25-lot series was not steady: lot 13 had 38 rejects among 400 (9.5%) and was the single high p-chart signal. The other 24 lots had no 3-sigma outlier and averaged 141/9,600 (1.46875%). Across all 25 lots, the rate was 179/10,000 (1.79%), below the 2.0% requirement on point estimate, but its confidence interval was 1.53925% to 2.06936% and therefore still crossed the requirement.

Today's two-head window was 105 rejects among 6,000 placements (1.75%). This is 0.25 percentage points below the requirement and statistically unchanged from the archive (p = 0.85283), but its confidence interval was 1.43350% to 2.11457%, also crossing 2.0%. The correct business message is favorable current performance, not demonstrated long-term capability with margin.

## What had to be fixed before the call could be trusted

The baseline study compared each inspector's calls with an agreed answer key. It found 5 mismatches among 120 calls, comprising 3 false accepts and 2 false rejects. At the individual-trial level, the weakest result was 18 matches among 20 (90%) with kappa 0.79798. This was sufficient to proceed with analysis, but not evidence that inspection was perfect.

The disagreement tally showed where clarification was needed. Of 90 differing calls, insufficient solder accounted for 46, or 51.1111%. The remaining counts were component offset 14, tombstone 12, solder bridge 9, and wrong polarity 9. The first four categories totaled 81, or 90%, so the rewrite had to cover multiple boundary conditions rather than one isolated defect type.

After the rewrite, accuracy was 117/120, the minimum pooled appraiser kappa was 0.875, and false rejects were 0. However, false accepts remained at 3, and the weakest trial was again 18/20 (90%) with kappa 0.736842. The improvement in total agreement was not statistically significant. The change should therefore be treated as a criteria/clarification intervention with no proven accuracy gain, not as a completed measurement-system fix.

## Whether the reject level held steady

The p-chart center line for all 25 lots was 1.79%, with an upper control limit of 3.77882%. Lot 13 rejected 38/400 (9.5%); the exact probability of 38 or more at the chart center line was 1.66e-16. It is a clear high special cause. Lot 15 had 0 rejects, but the computed lower limit was truncated at zero, so no lower out-of-control claim is made for a point at that boundary.

The runs-around-median check had 11 runs versus an expected 13 and p = 0.40380, providing no evidence of an additional nonrandom pattern. Excluding special-cause lot 13, the remaining 24 lots averaged 1.46875%, had no 3-sigma outlier, and had a confidence interval from 1.23771% to 1.72988%. The retained series is statistically below the 2% requirement (lower-tail p = 0.0000595916). In practical terms: one exceptional lot destabilized the full archive; the rest of the series appears steady and below the requirement.

No process fact explaining lot 13 was released. There is no data on its material, head, operator, settings, corrective action, or closure. The analysis therefore stops at “special statistical cause” and cannot honestly assign a physical cause.

## Today's level and placement heads

Head 1 rejected 56/3,000 (1.8667%) and head 2 rejected 49/3,000 (1.6333%). The difference was 0.2333 percentage points, z = 0.68919 and p = 0.49071, so this window does not identify either head as the problem. Combining them gives 105/6,000 (1.75%). That is 0.25 percentage points below the requirement and unchanged from the archive rate (difference -0.04 percentage points; p = 0.85283), but its confidence interval is 1.43350% to 2.11457% and still crosses 2%.

## Next actions

- Close lot 13's special cause: retrieve lot traceability, material records, placement-head logs, maintenance records, and corrective-action closure evidence. Keep both the all-lot and special-cause-removed views until that investigation is complete.
- Run the p chart routinely at the current lot size and investigate upper-limit signals or sustained shifts; do not manage solely by comparing a single lot with 2%.
- Prioritize false accepts in recurring calibration, using retained boundary examples led by insufficient solder, then the other high-count categories.
- Keep the rewritten criteria and answer key under control. Continue reporting pooled appraiser-to-standard agreement, worst-trial behavior, false accepts, and false rejects—not total agreement alone.
- Collect sequential placement-head subgroups before taking head-specific action; the present head comparison is not significant.
- Declare long-term capability only when the upper confidence bound is below 2% under an agreed stable-period rule. The current all-lot and today windows have not met that evidence standard.
