# Final inspection project status

## Executive conclusion

The original accept/reject call could not be relied on, so the first prerequisite was to repair the measurement system. The rewritten criteria were followed by a large improvement in the attribute study, and the call now appears reliable. The lot record nevertheless did not hold steady: it shows a statistically significant downward trend. The improvement has not yet secured the business requirement. The current supplied placement window rejected **202 of 6,000 boards (3.367%)**, versus the **2.0%** requirement; it contains **82 excess rejects** relative to a 6,000-board allowance of **120**. Head 1 is the dominant immediate focus.

## Could the accept/reject call be relied on?

Originally, no. Three inspectors each judged the same 20 retained boards twice against the answer key (120 calls). Only **73.333%** of calls agreed with the key—**32 mismatches**—and the weakest inspector kappa was **0.285714**. The appraiser agreement rates were **70.0%**, **67.5%**, and **82.5%**. Repeat-trial agreement was only **63.333%**.

Thus, calls made before criteria repair could not safely be treated as truth. The numerical lot record was not interpreted as proof of true defect level until the measurement issue was addressed.

## What had to happen first, and what changed

The disagreement tally's largest category was **insufficient solder**, accounting for **43 of 90 tally entries (47.778%)**. With **16** tombstone entries, those two accounted for **65.556%**. The full tally was **insufficient solder 43, tombstone 16, component offset 13, wrong polarity 11, and solder bridge 7**. The steward did not define the tally's counting unit; it does not reconcile like-for-like with the 120 key-comparison calls and is therefore kept separate rather than presented as a percentage of calls.

The accept/reject criteria were rewritten afterward. In the second study, **99.167%** of 120 calls agreed with the key and the weakest inspector kappa was **0.941860**. There was **1 mismatch**, and repeat agreement rose to **98.333%**. Agreement increased by **25.833 percentage points**, minimum kappa by **0.656146**, and repeatability by **35.0 percentage points**. This supports reliance on the post-rewrite call; it does not by itself prove that every historical lot-level change was caused by the rewrite.

## Did the reject share hold steady across lots?

Across all 25 lots and 10,000 inspected boards there were 311 rejects (**3.11%**). The whole-series p chart had **0** points outside its three-sigma limits, and the above/below-center runs test was not significant (p = **0.154355**). However, “no point outside limits” is not the same as “steady”: lot order had a significant downward trend (p = **0.040377**; slope **-0.000531** per lot; R² **17.026%**).

The strongest data-detected split was after lot 17: the first 17 lots rejected **240/6,800 (3.529%)**, while the last 8 rejected **71/3,200 (2.219%)**; the two-proportion test gave p = **0.000428**, or **0.010276** after considering all 24 candidate splits. This is strong evidence of a level change in the archive, but I did not obtain a process fact tying the criteria rewrite to lot 17, so I will not claim that exact attribution.

## How does today compare with the requirement?

The current placement window is above requirement: **202/6,000 = 3.367%**, with a 95% Wilson interval from **2.939% to 3.854%**; the binomial upper-tail test against 2.0% gives p = **3.217e-12**. At 2%, 6,000 boards allow **120** rejects, so this window has **82 excess rejects**.

By head:

- Head 1: **128/3,000 = 4.267%**, **68 excess rejects**, upper-tail p = **7.684e-15**.
- Head 2: **74/3,000 = 2.467%**, **14 excess rejects**, upper-tail p = **0.042585**.
- Head 1 is **1.800 percentage points** higher than Head 2; the head-to-head two-proportion test gives p = **0.000111**.

The late eight-lot archive segment was **71/3,200 = 2.219%** (95% Wilson interval **1.763% to 2.789%**; upper-tail p = **0.203953**) and had no p-chart point outside limits. Its point estimate is still above 2.0%, but the segment alone does not statistically establish a capability violation. The current placement window is less favorable and is the stronger operational basis for action.

## What should be done next

- **Contain and prioritize Head 1.** Its current 4.267% rate is both materially and statistically worse than Head 2. Apply the plant's containment protocol to Head 1 output while its placement process is investigated.
- **Run a Head 1-specific mechanical/process investigation.** Compare nozzle, pick/place force, feed, solder-paste, and maintenance condition with Head 2. The supplied data identify the head difference, not its physical root cause.
- **Maintain the rewritten criteria and audit them.** Retain boundary boards, answer keys, and blind checks so the 99.167% agreement does not drift.
- **Use a p chart by lot plus trend and run rules.** The archive had no three-sigma flags despite a significant shift, so points outside limits must not be the only escalation trigger.
- **Obtain the missing timing facts.** The criteria-implementation lot and the linkage between the placement window and rewrite could not be retrieved. Until they are supplied, describe the late-lot improvement as occurring after the detected split—not formally as the rewrite's effect.
- **Do not declare the line capable.** Current output remains 1.367 percentage points above the 2.0% requirement. Re-evaluate after Head 1 corrective action with a predefined sample-size and control rule.

No archive batch was denied. The attribution gap is limited to unavailable process-timing facts; it does not undermine the computed MSA improvement, the observed lot shift, or the current head comparison.

**Bottom line:** the call had to be repaired before rejects could be managed; that repair succeeded. The lot record then shifted downward, but today's window is still above requirement, and Head 1 is the clearest next target.
