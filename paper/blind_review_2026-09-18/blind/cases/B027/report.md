# Precision-Turning Cell: Outer Diameter and Wall Thickness Project Report

## 1. Can the readings carry a conclusion?

Yes. A crossed Gage R&R study (3 operators, 10 parts, 3 replicates, tolerance = 0.4 mm) was run on the
instrument that measures both characteristics. The ANOVA-method Gage R&R gives:

- %Study Variation (GRR) = **15.24%**
- %Tolerance (GRR) = **12.87%**
- Number of Distinct Categories (ndc) = **9.15** (rounds to 9)

Both figures sit inside the generally accepted band (%StudyVar and %Tolerance under 30%, ndc ≥ 5), so
the measurement system is fit for judging the process. The readings that follow can be trusted to
support a conclusion.

## 2. How has each characteristic behaved across the run?

Both characteristics were sampled five pieces at a time across 25 points (125 readings each) on the
same instrument.

**Outer diameter** — Xbar-R chart: center line (grand mean) = 25.0030 mm, 0 subgroups flagged on
either the Xbar or R chart. The run is statistically stable; Shapiro-Wilk normality test on the raw
data gives p = 0.880, so a normal-distribution capability model applies.

**Wall thickness** — Xbar-R chart: center line = 1.3957 mm, 0 subgroups flagged. Also stable;
Shapiro-Wilk p = 0.661, normal capability model applies.

Neither characteristic shows an out-of-control run. Any shortfall against spec is therefore a matter
of where the stable process is centered/spread, not of an unstable process.

## 3. Where does each sit against its accepted range?

| Characteristic | LSL | USL | Mean | Cp | Cpk | Pp | Ppk |
|---|---|---|---|---|---|---|---|
| Outer diameter (mm) | 24.80 | 25.20 | 25.0030 | 0.677 | 0.667 | 0.685 | 0.674 |
| Wall thickness (mm) | 1.20 | 1.60 | 1.3957 | 1.801 | 1.762 | 1.743 | 1.706 |

Wall thickness is comfortably capable (Cpk/Ppk well above the common 1.33 minimum) and is centered
close to its 1.40 mm target. It is not a priority for action.

Outer diameter is **not capable**: Cpk = 0.667 and Ppk = 0.674, both far short of 1.0, let alone
1.33. Even though the run is stable and roughly on target (mean 25.003 mm vs. target 25.0 mm), the
spread of the process is too wide for the 24.80–25.20 mm window — expect a meaningful fraction of
parts outside spec at the current spread.

## 4. Which characteristic decides what happens next, and why

**Outer diameter decides the next action.** It is the only one of the two characteristics that fails
capability; wall thickness is already well inside its range and stable.

To find out why diameter is wide, diameter was pulled apart by which of the four turning fixtures
produced each piece (15 pieces per fixture). A one-way ANOVA gives:

- F = 18.23, p = 2.2 × 10⁻⁸ (highly significant)
- Fixture explains **49.4%** of the total diameter variance
- Fixture means: fixture 1 = 24.875 mm, fixture 2 = 24.973 mm, fixture 3 = 25.021 mm, fixture 4 = 25.064 mm

The four fixtures are not producing the same diameter. Fixture 1 runs about 0.19 mm below fixture 4
on average — nearly half the total tolerance band by itself. This fixture-to-fixture offset is the
leading candidate explaining why the pooled diameter capability is poor even though the overall
process is statistically stable: the instability isn't in time, it's across fixtures.

## 5. Wall thickness and coolant pressure: checked and ruled out

A paired sample of 60 records of coolant delivery pressure and wall thickness was also examined,
since coolant pressure was suspected as a possible driver of wall thickness variation.

- Pearson correlation: r = 0.103, p = 0.433
- OLS regression (thickness on pressure): R² = 1.06%, adjusted R² = -0.65%, model p = 0.433

There is no statistically significant relationship between coolant delivery pressure and wall
thickness in this sample. Since wall thickness is already capable, this is a closed line of
inquiry rather than a gap in the record — the data needed to check it was available and checked,
and it did not turn up a driver worth acting on.

## 6. What this means for the plant and what to do

- **Where things stand**: wall thickness is in good shape (Cpk/Ppk ~1.7-1.8) and should stay on
  standard SPC monitoring. Outer diameter is not capable (Cpk 0.667, Ppk 0.674) despite a stable,
  on-target run.
- **What is causing it**: fixture-to-fixture differences in the four turning fixtures account for
  about half of all diameter variation (ANOVA p < 0.001). Fixture 1 trends low, fixture 4 trends
  high, relative to the 25.00 mm target.
- **What should change**: the four fixtures need to be checked against each other — tooling offsets,
  fixture wear, or setup differences are the leading suspects given the magnitude and significance
  of the between-fixture spread. Bringing the four fixture means together (e.g., re-zeroing offsets
  fixture-by-fixture) should shrink the pooled diameter spread and lift Cpk/Ppk toward the
  capable range, without needing to move the overall run's center or address any out-of-control
  behavior (there isn't any).
- **How it will be held**: continue the Xbar-R chart on outer diameter, but going forward, track
  and chart it by fixture (or at minimum, re-run the by-fixture ANOVA periodically) so a fixture
  drifting out of alignment with the others is caught before pooled Cpk erodes again. Wall
  thickness stays on its existing Xbar-R chart; no new investigation is warranted there absent a
  future capability breach.

## 7. What was not available

Every batch of data asked for in this project was released and analyzed — the charter, the Gage R&R
study, both characteristics' sampling-order runs, the by-fixture diameter breakdown, and the paired
coolant pressure/thickness sample. No batch was denied, so there is no gap in this report to flag on
that account.
