"""adb_c24 generator — the first case that grades ALL FIVE DMAIC phases.

WHY THIS CASE EXISTS
--------------------
Measured over the 372 built task instances before it: the DEFINE phase carried 0 truths and
0 decision points (an agent that skipped Define forfeited nothing), and CONTROL carried
truths but 0 decision points (it was graded on numbers, never on whether the agent chose the
right sustaining strategy). ``tests/test_phase_coverage.py`` pins that finding. adb_c24 puts
at least one HARD truth and at least one EVIDENCE-OBSERVABLE decision point in every one of
the five phases.

PROVENANCE OF THE STRUCTURE (not of the data)
---------------------------------------------
The project skeleton is taken from the strongest documented Define+Control source in the
authors' corpus, an electronics automatic-assembly first-pass-yield report that is held out of
the public release (docs/HELD_OUT.md): a six-month baseline first-pass yield of
90.5%, a customer commitment of 96% with a 98% stretch, a seven-class teardown Pareto whose
counts are 792/363/340/282/118/105/83 (top four = 85.31%, which is the deck's own stated
scoping rule), a realised result of 98.05%, and a control plan carrying real tolerances
(72.1 +/- 0.1 mm carrier-pallet bore, 218.0 +/- 0.1 mm zeroing rod) with a per-row reaction
plan. Every SHAPE below — the phase content, the mandate, the class ranking, the tolerance,
the before/after levels — comes from that record. Every NUMBER is generated here from the
seed: that deck is image-only, its raw arrays exist as screenshots, and inventing a "true"
array would be a fabricated truth. ``provenance: SIMULATED`` therefore states the honest
thing about the DATA, and ``case.yaml``'s ``effort_source`` states the honest thing about
the human-effort axis: that project's observed effort is already recorded against the case
built directly from it, and entering it here too would double-count one project record, so no
figure is entered. The figure itself, its dates and its team composition are not repeated in
this public file.

derive, never hand-write — EVERY TRUTH IS DERIVED BY ``truth/verifiers.py``
-------------------------------------------------------------
Nothing in this file computes a truth of its own. Each expected value is read back out of
the reference implementation the V7 gate will use, so a truth here cannot disagree with the
gate by construction. Only methods that HAVE a reference implementation are bound; the four
``define.*`` verifiers proposed in ``docs/archive/define-phase-design-2026-09-04.md`` §4 do not exist
yet, so this case grades Define through ``capability.binomial`` (the baseline the charter
commits against) and ``quality.pareto`` (the scoping of the fault classes) instead of
inventing DPU/DPMO/COPQ truths nothing could re-derive.

DECLARED CONVENTIONS (payload-side, never verifier-side)
--------------------------------------------------------
Wherever two toolchains differ defensibly, the stage payload SAYS which reading the stored
truth used, so an agent that reads the payload knows which default to take:

  A_Bore     ``assumeEqualVariances: true``          -> the classic pooled-error F, not
                                                        Welch's k-sample F (Minitab's newer
                                                        default), which is a different number
             ``varianceTestCentering: "median"``     -> Levene/Brown-Forsythe, not Bartlett
             ``distributionCheckScope: "pooled"``    -> the shape check runs on the pooled
                                                        readings, not per group or on residuals
  A_Station  ``continuityCorrection: false``         -> no Yates on the 3x2 table
  I_Confirm  ``alternativeHypothesis: "NOT_EQUAL"``  -> two-sided
             ``continuityCorrection: false``         -> statsmodels' default, not R prop.test's
             ``standardErrorConvention: "pooled"``   -> the null-consistent SE
             ``comparisonOrder: "before minus after"``-> fixes the SIGN of z (which is why z is
                                                        carried SOFT and the p-value hard)
  I_Screen   ``coding: "coded_units_-1_+1"`` + ``termsInModel`` -> the model is the declared
                                                        one; nothing is re-coded or re-centred
  M_Baseline/C_Monitor ``limitConvention``           -> pooled centre line, per-point 3-sigma
                                                        limits from each period's own size, a
                                                        negative lower limit reported as zero
  C_Confirm  ``sigmaShiftApplied: false``            -> the reported process Z is the UNSHIFTED
                                                        long-term Z = Phi^-1(1 - p), which is
                                                        what ``verifiers.capability_binomial``
                                                        computes; no 1.5 shift is added

SEED-INVARIANT CONCLUSIONS (``_assert_invariants``, swept over seeds 1..500)
---------------------------------------------------------------------------
Every branch and every verdict this case grades must land the same way for every seed, with
a stated margin — otherwise a decision point is a coin flip under reseeding:

  * baseline first-attempt failure rate in (0.085, 0.108) and its process Z in (1.2, 1.4);
  * the leading fault class beats the second by >= 10 points of share, and the top four
    classes cover 80-90% of all failures (the deck's scoping rule stays true);
  * the bench judgement is ACCEPTABLE (min kappa > 0.78, agreement > 88%), so the project may
    rest conclusions on it;
  * the baseline daily record is CLEARLY overdispersed (Laney sigma_Z > 1.8 AND a Pearson
    dispersion test at p < 0.001) — the determinacy band of
    docs/archive/control-phase-design-2026-09-04.md §D1;
  * the post-release daily record is CLEARLY NOT overdispersed (sigma_Z < 1.15, dispersion
    p > 0.20) and holds 0 points beyond its limits, and its period sizes vary by >= 1.4x, so
    the sustaining chart is the varying-size proportion chart and neither of the two wrong
    branches is defensible;
  * the pooled bore readings pass the shape check (p > 0.15) and the three sources have
    homogeneous variance (p > 0.15) while their means differ (p < 0.005) — so the parametric
    branch is the correct one AND its preconditions are visibly met;
  * the station tally separates (p < 0.005);
  * the trial matrix model is significant (p < 0.005) and explains > 80%;
  * the pilot separates (p < 0.005);
  * NO p-value truth is smaller than 1e-6 — every guard band has that floor and every
    p-value is stored at 10 decimals, so a truth can never round to an unreportable 0.0;
  * the confirmed post-release failure rate clears the chartered 4.0% ceiling with >= 1.0
    point of margin AND improves on the baseline by >= 5 points — so the closure verdict is
    the same for every seed.
"""
import random
import sys
from pathlib import Path

_PKG_ROOT = str(Path(__file__).resolve().parents[2].parent)
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from scipy import stats  # noqa: E402

from dmaic_bench.core.models import CaseData, TruthEntry  # noqa: E402
from dmaic_bench.truth import verifiers  # noqa: E402

# ---- the source project's fixed frame (shapes, not data) -----------------------------------
#: Customer commitment and stretch level on the first-attempt pass rate, from the charter.
COMMITTED_PASS_RATE_PCT = 96.0
STRETCH_PASS_RATE_PCT = 98.0
#: The ceiling the Control phase is judged against, expressed as a failure rate.
CHARTER_FAILURE_CEILING = round(1.0 - COMMITTED_PASS_RATE_PCT / 100.0, 6)  # 0.04
#: Carrier-pallet bore drawing tolerance carried by the source deck's control plan.
BORE_TARGET_MM, BORE_TOL_MM = 72.1, 0.1
#: Monthly first-attempt pass rates of the recorded six-month baseline window.
BASELINE_MONTHLY_PASS_PCT = (92.94, 90.97, 90.67, 89.57, 88.89, 89.05)
#: Teardown fault classes, ranked as the source deck ranks them, with its share profile.
FAULT_CLASSES = (
    "connector_solder_bridge",
    "carrier_pallet_misalignment",
    "press_fit_incomplete",
    "firmware_load_timeout",
    "label_position_out_of_window",
    "housing_surface_scratch",
    "retaining_screw_torque_low",
)
FAULT_SHARES = (792, 363, 340, 282, 118, 105, 83)


# ---- primitive draws (pure python, deterministic given the rng stream) ---------------------

def _binom(rng, n, p):
    return sum(1 for _ in range(n) if rng.random() < p)


def _multinomial(rng, total, weights):
    """Split ``total`` across ``weights`` by sequential conditional binomials (exact sum)."""
    remaining_total, remaining_w = total, float(sum(weights))
    out = []
    for w in weights[:-1]:
        k = _binom(rng, remaining_total, w / remaining_w) if remaining_total else 0
        out.append(k)
        remaining_total -= k
        remaining_w -= w
    out.append(remaining_total)
    return out


def _gauss_series(rng, n, mu, sigma, nd=3):
    return [round(rng.gauss(mu, sigma), nd) for _ in range(n)]


def _redraw(rng, draw_fn, ok_fn, what, tries=400):
    for _ in range(tries):
        block = draw_fn(rng)
        if ok_fn(block):
            return block
    raise AssertionError(f"adb_c24: could not construct {what} in {tries} draws")


# ---- dispersion diagnostics used ONLY as generator guards ----------------------------------
# These decide whether a DRAW is admissible; no truth is derived from them. The rule is the
# conjunction stated in docs/archive/control-phase-design-2026-09-04.md §D1: a Pearson dispersion test
# (McCullagh & Nelder 2e §4.5.2) for the formal decision, and Laney's sigma_Z (Laney 2002,
# Quality Engineering 14(4) 531-537) for the magnitude.

def _pearson_dispersion_p(counts, sizes):
    total_d, total_n = sum(counts), sum(sizes)
    pbar = total_d / total_n
    x2 = sum((c - n * pbar) ** 2 / (n * pbar * (1 - pbar)) for c, n in zip(counts, sizes))
    return float(stats.chi2.sf(x2, len(counts) - 1))


def _sigma_z(counts, sizes):
    return verifiers.control_chart_laney_p(
        {"defectCounts": list(counts), "sampleSizes": list(sizes)})["sigmaZ"]


# ---- the case ------------------------------------------------------------------------------

def generate(seed: int) -> CaseData:
    rng = random.Random(seed * 1_000_003 + 20260904)

    # ---------------------------------------------------------------- DEFINE: charter pack
    # The charter pack holds BOTH candidate project metrics, which is the point: the customer
    # scorecard metric (a six-month pass/fail build ledger) and the engineering team's own
    # proposal (a one-off dozen-reading check of a carrier-pallet bore against its drawing
    # tolerance). Only one of them is an output characteristic the customer names and holds a
    # record for; the decision point `project_y_selection` is exactly that choice, and the two
    # candidates route to different method families so the choice is visible in a trace.
    def _draw_charter(r):
        units = [r.randint(3400, 3900) for _ in range(6)]
        fails = [_binom(r, n, min(max(r.gauss(1.0 - pct / 100.0, 0.004), 0.02), 0.20))
                 for n, pct in zip(units, BASELINE_MONTHLY_PASS_PCT)]
        bore = _gauss_series(r, 12, BORE_TARGET_MM + 0.004, 0.021)
        return {
            "recordWindow": "month_1..month_6 (six consecutive months, closed)",
            "recordSource": "line build log, end-of-line functional and fit check",
            "monthLabels": [f"month_{i}" for i in range(1, 7)],
            "subgroupSizes": units,
            "defectCounts": fails,
            "outcomeDefinition": ("one unit = one build; a unit is counted in defectCounts "
                                  "when it did not pass the end-of-line check on its first "
                                  "attempt and was routed to the rework bench"),
            "customerMandate": {
                "namedCharacteristic": "share of units passing the end-of-line check first time",
                "baselineWindow": "month_1..month_6",
                "committedLevelPct": COMMITTED_PASS_RATE_PCT,
                "stretchLevelPct": STRETCH_PASS_RATE_PCT,
                "recordedIn": "customer quarterly scorecard review, signed by both customers",
            },
            "engineeringCandidate": {
                "note": ("the equipment group proposed using the carrier-pallet bore instead; "
                         "the readings below are a single check taken last week on twelve "
                         "pallets pulled from the line, with no earlier record and no entry "
                         "on the customer scorecard"),
                "characteristic": "carrier pallet bore diameter",
                "collected": "one-off engineering check, twelve pallets, one reading each",
            },
            "data": bore,
            "unit": "mm",
            "lsl": round(BORE_TARGET_MM - BORE_TOL_MM, 3),
            "usl": round(BORE_TARGET_MM + BORE_TOL_MM, 3),
            "target": BORE_TARGET_MM,
        }

    def _charter_ok(b):
        ref = verifiers.capability_binomial(b)
        return 0.085 < ref["avgP"] < 0.108

    charter = _redraw(rng, _draw_charter, _charter_ok, "six-month baseline build ledger")
    charter_ref = verifiers.capability_binomial(charter)
    total_failures = sum(charter["defectCounts"])

    # ---------------------------------------------------------------- DEFINE: scoping
    # The teardown log classifies EVERY failed unit of the same window, so its counts sum to
    # the ledger's failures. The scoping question ("which classes carry most of it") is what
    # this block answers; the boundary consequence is a number, not a prose argument.
    def _draw_scope(r):
        counts = _multinomial(r, total_failures, FAULT_SHARES)
        return {
            "recordWindow": "month_1..month_6 (the same closed window as the build ledger)",
            "recordSource": "rework bench teardown log, one row per unit that failed first time",
            "faultClass": list(FAULT_CLASSES),
            "counts": counts,
            "coverageNote": ("every unit counted in the build ledger's defectCounts appears "
                             "exactly once here, classified by the fault seen at teardown"),
        }

    def _scope_ok(b):
        c = sorted(b["counts"], reverse=True)
        tot = sum(c)
        if tot <= 0:
            return False
        top1, top2 = 100.0 * c[0] / tot, 100.0 * c[1] / tot
        top4 = 100.0 * sum(c[:4]) / tot
        return (top1 - top2) >= 10.0 and 80.0 <= top4 <= 90.0

    scope = _redraw(rng, _draw_scope, _scope_ok, "teardown fault-class ledger")
    scope_ref = verifiers.pareto(scope)

    # ---------------------------------------------------------------- MEASURE: bench judgement
    # The project Y is a human pass/fail judgement, so what has to be established before any
    # conclusion rests on it is the agreement of the inspectors with a known condition — the
    # decision point `measurement_study_route`.
    def _draw_msa(r):
        std = ["fail" if r.random() < 0.40 else "pass" for _ in range(30)]
        ratings = {}
        for a in ("inspector_1", "inspector_2", "inspector_3"):
            acc = r.uniform(0.94, 0.985)
            ratings[a] = [[(lab if r.random() < acc else ("pass" if lab == "fail" else "fail"))
                           for lab in std] for _ in range(2)]
        return {
            "retainedSetSize": 30,
            "standardSource": ("condition of each retained unit established by the process "
                               "owner on a teardown bench before the study"),
            "standard": std,
            "ratings": ratings,
            "trialsPerInspector": 2,
            "presentationOrder": "randomised, blind to the inspector and to the earlier trial",
        }

    def _msa_ok(b):
        ref = verifiers.attribute_agreement(b)
        return ref["kappaMin"] > 0.78 and ref["agreementPct"] > 88.0

    msa = _redraw(rng, _draw_msa, _msa_ok, "bench agreement study above the acceptance floor")
    msa_ref = verifiers.attribute_agreement(msa)

    # ---------------------------------------------------------------- MEASURE: baseline record
    # Thirty baseline days with a REAL day-to-day component on top of the unit-to-unit one.
    # Binomial sampling theory alone underestimates that spread, so the baseline record is
    # clearly overdispersed and its limits have to absorb the extra component. Guarded into
    # the determinate band (sigma_Z > 1.8 AND dispersion p < 0.001).
    def _draw_baseline(r):
        sizes = [r.randint(120, 240) for _ in range(30)]
        day_p = [min(max(r.gauss(charter_ref["avgP"] * 0.94, 0.030), 0.012), 0.26)
                 for _ in sizes]
        counts = [_binom(r, n, p) for n, p in zip(sizes, day_p)]
        return {
            "recordWindow": "30 consecutive build days inside month_5..month_6",
            "periodLabels": [f"day_{i}" for i in range(1, 31)],
            "sampleSizes": sizes,
            "defectCounts": counts,
            "outcomeDefinition": ("defectCounts[i] units of sampleSizes[i] built that day did "
                                  "not pass the end-of-line check on the first attempt"),
            "limitConvention": ("centre line is the pooled share over the whole window; each "
                                "period's own limits are set three standard errors out using "
                                "that period's own build quantity; a negative lower limit is "
                                "reported as zero"),
        }

    def _baseline_ok(b):
        if min(b["defectCounts"]) < 1:
            return False
        if abs(sum(b["defectCounts"]) / sum(b["sampleSizes"]) - charter_ref["avgP"]) > 0.02:
            return False  # the same process, so the two windows must agree on its level
        return (_sigma_z(b["defectCounts"], b["sampleSizes"]) > 1.8
                and _pearson_dispersion_p(b["defectCounts"], b["sampleSizes"]) < 0.001)

    baseline = _redraw(rng, _draw_baseline, _baseline_ok,
                       "clearly overdispersed baseline daily record")
    baseline_ref = verifiers.control_chart_laney_p(baseline)

    # ---------------------------------------------------------------- ANALYZE: pallet sources
    # Bore readings from three pallet suppliers. Equal group sizes, homogeneous variance and a
    # pooled shape check that passes, so the parametric k-sample comparison is the correct
    # branch and its preconditions are visibly satisfied rather than assumed.
    def _draw_bore(r):
        mus = (BORE_TARGET_MM - 0.006, BORE_TARGET_MM + 0.003, BORE_TARGET_MM + 0.016)
        groups = {f"supplier_{k}": _gauss_series(r, 15, mu, 0.019, nd=4)
                  for k, mu in zip("ABC", mus)}
        pooled = [v for g in groups.values() for v in g]
        return {
            "recordSource": ("bore readings on pallets drawn from the three pallet suppliers, "
                             "all measured on the same bench gauge in one session"),
            "groups": groups,
            "data": pooled,
            "unit": "mm",
            "distributionCheckScope": ("pooled — the shape check below runs on all forty-five "
                                       "readings together, not per source and not on residuals"),
            "varianceTestCentering": "median",
            "assumeEqualVariances": True,
            "alternativeHypothesis": "NOT_EQUAL",
        }

    def _bore_ok(b):
        return (verifiers.normality(b)["pValue"] > 0.15
                and verifiers.equal_variances(b)["pValue"] > 0.15
                and 1e-6 < verifiers.anova_oneway(b)["factorPValue"] < 0.005)

    bore = _redraw(rng, _draw_bore, _bore_ok, "three pallet sources, parametric branch determinate")
    bore_norm_ref = verifiers.normality(bore)
    # The payload declares the SCOPE of the shape check but not which test; Minitab
    # (Anderson-Darling) and R (`shapiro.test`) disagree by 0.17 here. Admitting Shapiro at
    # its own precision is what lets this p-value be scored hard instead of warn-only.
    _bore_norm_p = round(bore_norm_ref["pValue"], 6)
    _bore_norm_accepts = verifiers.convention_windows(
        "basic.normality", "pValue", bore, _bore_norm_p, 0.06)
    bore_var_ref = verifiers.equal_variances(bore)
    bore_anova_ref = verifiers.anova_oneway(bore)

    # ---------------------------------------------------------------- ANALYZE: station tally
    def _draw_station(r):
        rates = (0.088, 0.110, 0.087)
        rows = []
        for rate in rates:
            n = r.randint(2600, 3200)
            f = _binom(r, n, rate)
            rows.append([n - f, f])
        return {
            "recordWindow": "month_1..month_6",
            "rowLabels": ["station_1", "station_2", "station_3"],
            "columnLabels": ["passed_first_attempt", "failed_first_attempt"],
            "table": rows,
            "continuityCorrection": False,
            "tableNote": ("each row is one assembly station; the two columns are that "
                          "station's first-attempt outcomes over the baseline window"),
        }

    def _station_ok(b):
        return 1e-6 < verifiers.chisquare_assoc(b)["pValue"] < 0.005

    station = _redraw(rng, _draw_station, _station_ok, "station tally that separates")
    station_ref = verifiers.chisquare_assoc(station)

    # ---------------------------------------------------------------- IMPROVE: trial matrix
    # Three settings at two levels each, replicated twice, in coded units. The model is the
    # DECLARED one (main effects plus the two-factor interactions a 2^3 supports).
    _TERMS = ["pressForce", "palletClearance", "dwellTime",
              "pressForce*palletClearance", "pressForce*dwellTime",
              "palletClearance*dwellTime"]

    def _draw_screen(r):
        a, b_, c, y = [], [], [], []
        for _ in range(2):
            for la in (-1, 1):
                for lb in (-1, 1):
                    for lc in (-1, 1):
                        a.append(la)
                        b_.append(lb)
                        c.append(lc)
                        y.append(round(8.0 - 2.3 * la - 1.5 * lb + 0.95 * lc
                                       + 0.85 * la * lb + r.gauss(0, 1.45), 3))
        return {
            "designNote": ("three line settings, each run at a low and a high setting, the "
                           "whole matrix run twice in randomised order"),
            "coding": "coded_units_-1_+1",
            "data": {"pressForce": a, "palletClearance": b_, "dwellTime": c,
                     "seatingDepthDeviationUm": y},
            "responseColumn": "seatingDepthDeviationUm",
            "termsInModel": list(_TERMS),
            "modelNote": ("the terms above are the model; nothing is re-coded, re-centred or "
                          "re-scaled, and no term outside this list is fitted"),
            "replicates": 2,
        }

    def _screen_ok(b):
        ref = verifiers.doe_factorial_analysis(b)
        p = ref.get("modelPValue", 1.0)
        return 1e-6 < p < 0.005 and ref["rSquaredPct"] > 80.0

    screen = _redraw(rng, _draw_screen, _screen_ok, "trial matrix with a determinate model")
    screen_ref = verifiers.doe_factorial_analysis(screen)

    # ---------------------------------------------------------------- IMPROVE: pilot run
    # Two INDEPENDENT production runs of different sizes, unit-level pass/fail. There is no
    # unit-to-unit correspondence between them, which is what makes `pilot_confirmation_route`
    # a real decision rather than a formality.
    def _draw_pilot(r):
        n1, n2 = r.randint(280, 330), r.randint(330, 380)
        return {
            "runNote": ("run 1 is the last production run at the old settings, run 2 the first "
                        "at the settings the trial matrix pointed to; the two runs are "
                        "different production orders of different size and share no units"),
            "trials1": n1, "events1": _binom(r, n1, r.uniform(0.092, 0.106)),
            "trials2": n2, "events2": _binom(r, n2, r.uniform(0.022, 0.032)),
            "eventDefinition": "events = units that did not pass the check on the first attempt",
            "alternativeHypothesis": "NOT_EQUAL",
            "continuityCorrection": False,
            "standardErrorConvention": "pooled",
            "comparisonOrder": "run 1 (before) minus run 2 (after)",
        }

    def _pilot_ok(b):
        return 1e-6 < verifiers.two_proportions(b)["pValue"] < 0.005

    pilot = _redraw(rng, _draw_pilot, _pilot_ok, "pilot run that separates")
    pilot_ref = verifiers.two_proportions(pilot)

    # ---------------------------------------------------------------- CONTROL: released line
    # Post-release daily record. Homogeneous (the day effect the baseline carried is gone), the
    # daily build quantity varies by more than 1.4x, and nothing sits beyond the limits — so the
    # sustaining chart is the varying-size proportion chart, a constant-size count chart is
    # inadmissible, and an individuals chart is the wrong data type entirely.
    def _draw_monitor(r):
        sizes = [r.randint(150, 260) for _ in range(24)]
        rate = r.uniform(0.016, 0.023)
        counts = [_binom(r, n, rate) for n in sizes]
        return {
            "recordWindow": "24 consecutive build days after the change was released",
            "periodLabels": [f"day_{i}" for i in range(1, 25)],
            "sampleSizes": sizes,
            "defectCounts": counts,
            "outcomeDefinition": ("defectCounts[i] units of sampleSizes[i] built that day did "
                                  "not pass the end-of-line check on the first attempt"),
            "limitConvention": ("centre line is the pooled share over the whole window; each "
                                "period's own limits are set three standard errors out using "
                                "that period's own build quantity; a negative lower limit is "
                                "reported as zero"),
            "reactionPlanNote": ("standing instruction on the released line: a period outside "
                                 "its own limits stops the line, quarantines that day's build "
                                 "and escalates to the process owner"),
        }

    def _monitor_ok(b):
        n = b["sampleSizes"]
        if max(n) / min(n) < 1.4 or min(b["defectCounts"]) < 1:
            return False
        ref = verifiers.control_chart_p(b)
        return (ref["outOfControlCount"] == 0
                and _sigma_z(b["defectCounts"], n) < 1.15
                and _pearson_dispersion_p(b["defectCounts"], n) > 0.20)

    monitor = _redraw(rng, _draw_monitor, _monitor_ok,
                      "homogeneous, in-control post-release daily record")
    monitor_ref = verifiers.control_chart_p(monitor)

    # ---------------------------------------------------------------- CONTROL: confirmation
    # THE CROSS-PHASE DEPENDENCY. The pass criterion of this stage is the level Define
    # committed to: the payload carries the charter's ceiling and names where it came from, and
    # the number that decides the project is the confirmed failure rate against it. The same
    # method (capability.binomial) is bound in D_Charter and here, on purpose and as separate
    # stages — that is what makes "did the project reach what it promised" a scored quantity
    # rather than a sentence.
    def _draw_confirm(r):
        sizes = [r.randint(800, 1000) for _ in range(12)]
        rate = r.uniform(0.016, 0.024)
        counts = [_binom(r, n, rate) for n in sizes]
        return {
            "recordWindow": "12 consecutive weeks after the change was released",
            "periodLabels": [f"week_{i}" for i in range(1, 13)],
            "subgroupSizes": sizes,
            "defectCounts": counts,
            "outcomeDefinition": ("defectCounts[i] units of subgroupSizes[i] built that week "
                                  "did not pass the end-of-line check on the first attempt"),
            "charterCommittedLevelPct": COMMITTED_PASS_RATE_PCT,
            "charterStretchLevelPct": STRETCH_PASS_RATE_PCT,
            "charterFailureCeiling": CHARTER_FAILURE_CEILING,
            "charterSource": ("the level the customers were committed to in the project "
                              "charter, carried forward unchanged"),
            "sigmaShiftApplied": False,
            "sigmaShiftNote": ("no long-term/short-term shift is added; the process Z reported "
                               "for this window is the unshifted value implied by the observed "
                               "share alone"),
        }

    def _confirm_ok(b):
        ref = verifiers.capability_binomial(b)
        return (ref["avgP"] < CHARTER_FAILURE_CEILING - 0.010
                and ref["avgP"] > 0.010
                and charter_ref["avgP"] - ref["avgP"] >= 0.05)

    confirm = _redraw(rng, _draw_confirm, _confirm_ok,
                      "post-release window that clears the chartered ceiling with margin")
    confirm_ref = verifiers.capability_binomial(confirm)

    blocks = {
        "D_Charter": charter, "D_Scope": scope,
        "M_Judgement": msa, "M_Baseline": baseline,
        "A_Sources": bore, "A_Stations": station,
        "I_Matrix": screen, "I_Pilot": pilot,
        "C_Released": monitor, "C_Confirmation": confirm,
    }

    _d = ("derived from the generated payload via truth.verifiers.{} (scipy/numpy), seed={}; "
          "conventions: {}")
    truths = (
        # ---- DEFINE ----------------------------------------------------------------------
        TruthEntry(method_id="capability.binomial", field="avgP",
                   expected=round(charter_ref["avgP"], 6), tol=0.0015, soft=False,
                   stage_id="D_Charter",
                   metric_cue=r"baseline|first[- ]attempt|first[- ]pass|failure rate",
                   derivation=_d.format("capability_binomial", seed,
                                        "pooled share over the six-month window, "
                                        "one unit = one build, failure = did not pass first time"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="capability.binomial", field="processZ",
                   expected=round(charter_ref["processZ"], 6), tol=0.03, soft=False,
                   stage_id="D_Charter",
                   metric_cue=r"process Z|\bZ\s*[=＝]|sigma level|capability of the baseline",
                   derivation=_d.format("capability_binomial", seed,
                                        "UNSHIFTED long-term Z = Phi^-1(1 - p); no 1.5 shift"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="quality.pareto", field="topCategoryPct",
                   expected=round(scope_ref["topCategoryPct"], 6), tol=0.3, soft=False,
                   stage_id="D_Scope",
                   metric_cue=r"largest|leading fault|top fault|accounts? for|biggest",
                   derivation=_d.format("pareto", seed,
                                        "share of the single largest fault class over all "
                                        "classified failures of the same window"),
                   verified_by=("numpy",)),

        # ---- MEASURE ---------------------------------------------------------------------
        TruthEntry(method_id="msa.attribute_agreement", field="kappaMin",
                   expected=round(msa_ref["kappaMin"], 6), tol=0.03, soft=False,
                   stage_id="M_Judgement",
                   metric_cue=r"agreement|inspector|appraiser|judgement|judgment",
                   derivation=_d.format("attribute_agreement", seed,
                                        "per-inspector Cohen agreement against the known "
                                        "condition, trials pooled; the MINIMUM over inspectors"),
                   verified_by=("numpy",)),
        TruthEntry(method_id="msa.attribute_agreement", field="agreementPct",
                   expected=round(msa_ref["agreementPct"], 6), tol=0.5, soft=False,
                   stage_id="M_Judgement",
                   metric_cue=r"agreement|matched the (known )?condition|inspector",
                   derivation=_d.format("attribute_agreement", seed,
                                        "individual ratings equal to the known condition over "
                                        "all ratings, as a percentage"),
                   verified_by=("numpy",)),
        TruthEntry(method_id="control_chart.laney_p", field="centerLine",
                   expected=round(baseline_ref["centerLine"], 6), tol=0.003, soft=False,
                   stage_id="M_Baseline",
                   metric_cue=r"cent(re|er) line|baseline.{0,40}(share|rate)|pooled",
                   derivation=_d.format("control_chart_laney_p", seed,
                                        "pooled centre line over the 30-day baseline window"),
                   verified_by=("numpy",)),
        TruthEntry(method_id="control_chart.laney_p", field="sigmaZ",
                   expected=round(baseline_ref["sigmaZ"], 6), tol=0.08, soft=False,
                   stage_id="M_Baseline",
                   metric_cue=r"dispersion|over-?dispers|sigma\s*Z|inflat|day-to-day",
                   derivation=_d.format("control_chart_laney_p", seed,
                                        "Laney 2002: z standardised per period, sigma_Z = mean "
                                        "moving range of z divided by 1.128"),
                   verified_by=("numpy",)),

        # ---- ANALYZE ---------------------------------------------------------------------
        # Hard, with Shapiro-Wilk admitted at its own precision: the payload declares the
        # SCOPE of the shape check but not which test, and AD and Shapiro disagree by 0.17
        # here — far outside the 0.06 window.
        TruthEntry(method_id="basic.normality", field="pValue",
                   expected=_bore_norm_p, tol=0.06, soft=False, accepts=_bore_norm_accepts,
                   stage_id="A_Sources",
                   metric_cue=r"shape|distribution|normal|P\s*[=＝>＞]",
                   derivation=_d.format("normality", seed,
                                        "A-squared with the small-sample p approximation, on "
                                        "the POOLED readings as the payload declares"),
                   verified_by=("scipy",)),
        # Hard with NO variant: this payload states `varianceTestCentering`, so the centring
        # that is convention-variant elsewhere is part of the specification here.
        TruthEntry(method_id="anova.equal_variances", field="pValue",
                   expected=round(bore_var_ref["pValue"], 6), tol=0.08, soft=False,
                   stage_id="A_Sources",
                   metric_cue=r"spread|variance|scatter|P\s*[=＝>＞]",
                   derivation=_d.format("equal_variances", seed,
                                        "median-centred spread comparison as the payload "
                                        "declares (varianceTestCentering)"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="anova.oneway", field="factorPValue",
                   expected=round(bore_anova_ref["factorPValue"], 10), tol=0.003, soft=False,
                   stage_id="A_Sources",
                   metric_cue=r"supplier|source|bore|P\s*[=＝<＜]",
                   derivation=_d.format("anova_oneway", seed,
                                        "classic pooled-error k-sample F with equal variances "
                                        "assumed, as the payload declares; two-sided"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="anova.oneway", field="fStatistic",
                   expected=round(bore_anova_ref["fStatistic"], 6), tol=0.4, soft=False,
                   stage_id="A_Sources",
                   metric_cue=r"\bF\s*[=＝]|F-?statistic|ratio",
                   derivation=_d.format("anova_oneway", seed,
                                        "classic pooled-error k-sample F, equal variances "
                                        "assumed as declared"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="tables.chisquare_assoc", field="statistic",
                   expected=round(station_ref["statistic"], 6), tol=0.4, soft=False,
                   stage_id="A_Stations",
                   metric_cue=r"station|statistic|association",
                   derivation=_d.format("chisquare_assoc", seed,
                                        "3x2 table, NO continuity correction, as declared"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="tables.chisquare_assoc", field="pValue",
                   expected=round(station_ref["pValue"], 10), tol=0.002, soft=False,
                   stage_id="A_Stations",
                   metric_cue=r"station|P\s*[=＝<＜]|association",
                   derivation=_d.format("chisquare_assoc", seed,
                                        "3x2 table, NO continuity correction, as declared"),
                   verified_by=("scipy",)),

        # ---- IMPROVE ---------------------------------------------------------------------
        TruthEntry(method_id="doe.factorial_analysis", field="rSquaredPct",
                   expected=round(screen_ref["rSquaredPct"], 6), tol=0.8, soft=False,
                   stage_id="I_Matrix",
                   metric_cue=r"R²|R2|R-?squared|explain",
                   derivation=_d.format("doe_factorial_analysis", seed,
                                        "least squares on the DECLARED terms in the DECLARED "
                                        "coded units; nothing re-coded or re-centred"),
                   verified_by=("numpy",)),
        TruthEntry(method_id="doe.factorial_analysis", field="modelPValue",
                   expected=round(screen_ref["modelPValue"], 10), tol=0.002, soft=False,
                   stage_id="I_Matrix",
                   metric_cue=r"trial matrix|model|setting|P\s*[=＝<＜]",
                   derivation=_d.format("doe_factorial_analysis", seed,
                                        "overall model F against the declared term list"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="basic.two_proportions", field="pValue",
                   expected=round(pilot_ref["pValue"], 10), tol=0.002, soft=False,
                   stage_id="I_Pilot",
                   metric_cue=r"pilot|before|after|confirm|P\s*[=＝<＜]",
                   derivation=_d.format("two_proportions", seed,
                                        "two independent runs, POOLED standard error, "
                                        "two-sided, no continuity correction — all declared"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="basic.two_proportions", field="zStatistic",
                   expected=round(pilot_ref["zStatistic"], 6), tol=0.4, soft=False,
                   stage_id="I_Pilot",
                   metric_cue=r"\bZ\s*[=＝]|z-?statistic",
                   derivation=_d.format("two_proportions", seed,
                                        "SIGN follows the declared comparisonOrder (before "
                                        "minus after) — the declaration is the specification, "
                                        "so the opposite sign is a failure to read it"),
                   verified_by=("scipy",)),

        # ---- CONTROL ---------------------------------------------------------------------
        TruthEntry(method_id="control_chart.p", field="centerLine",
                   expected=round(monitor_ref["centerLine"], 6), tol=0.002, soft=False,
                   stage_id="C_Released",
                   metric_cue=r"cent(re|er) line|released line|monitor|pooled",
                   derivation=_d.format("control_chart_p", seed,
                                        "pooled centre line over the released window; "
                                        "per-period limits, negative lower limit set to zero"),
                   verified_by=("numpy",)),
        TruthEntry(method_id="control_chart.p", field="outOfControlCount",
                   expected=float(monitor_ref["outOfControlCount"]), tol=0.0, soft=False,
                   stage_id="C_Released",
                   metric_cue=r"out[- ]of[- ]control|beyond|outside|signal|special cause",
                   derivation=_d.format("control_chart_p", seed,
                                        "periods outside their OWN limits only (the "
                                        "beyond-limits rule alone, no run rules)"),
                   verified_by=("numpy",)),
        TruthEntry(method_id="capability.binomial", field="avgP",
                   expected=round(confirm_ref["avgP"], 6), tol=0.0015, soft=False,
                   stage_id="C_Confirmation",
                   metric_cue=r"confirm|realis|realiz|sustain|after the change|reached",
                   derivation=_d.format("capability_binomial", seed,
                                        "pooled share over the 12-week post-release window; "
                                        "the quantity the chartered ceiling is judged against"),
                   verified_by=("scipy",)),
        TruthEntry(method_id="capability.binomial", field="processZ",
                   expected=round(confirm_ref["processZ"], 6), tol=0.04, soft=False,
                   stage_id="C_Confirmation",
                   metric_cue=r"process Z|\bZ\s*[=＝]|sigma level",
                   derivation=_d.format("capability_binomial", seed,
                                        "UNSHIFTED long-term Z = Phi^-1(1 - p), as the payload "
                                        "declares (sigmaShiftApplied: false)"),
                   verified_by=("scipy",)),
    )

    _assert_invariants(truths, blocks, charter_ref, confirm_ref, monitor_ref, baseline_ref)
    return CaseData(seed=seed, blocks=blocks, truths=truths)


def _assert_invariants(truths, blocks, charter_ref, confirm_ref, monitor_ref, baseline_ref):
    """Every branch and verdict this case grades must land the same way for every seed."""
    by = {(t.method_id, t.field, t.stage_id): t.expected for t in truths}

    # DEFINE — the baseline the charter commits against, and the class that carries it.
    base_p = by[("capability.binomial", "avgP", "D_Charter")]
    assert 0.085 < base_p < 0.108, f"baseline failure rate off the recorded frame: {base_p}"
    assert 1.2 < by[("capability.binomial", "processZ", "D_Charter")] < 1.4
    counts = sorted(blocks["D_Scope"]["counts"], reverse=True)
    tot = sum(counts)
    assert tot == sum(blocks["D_Charter"]["defectCounts"]), (
        "the teardown log must classify exactly the failures the build ledger counts")
    top1, top2 = 100.0 * counts[0] / tot, 100.0 * counts[1] / tot
    assert top1 - top2 >= 10.0, f"leading fault class is not a clear leader ({top1} vs {top2})"
    assert 80.0 <= 100.0 * sum(counts[:4]) / tot <= 90.0, "top-four coverage left its band"
    # The rejected candidate must stay obviously unfit as a project Y: one-off, a dozen
    # readings, no window. If it ever grew a history the decision point would stop being one.
    assert len(blocks["D_Charter"]["data"]) == 12
    assert "recordWindow" not in blocks["D_Charter"]["engineeringCandidate"]

    # MEASURE — the judgement is usable, and the baseline record is clearly overdispersed.
    assert by[("msa.attribute_agreement", "kappaMin", "M_Judgement")] > 0.78
    assert by[("msa.attribute_agreement", "agreementPct", "M_Judgement")] > 88.0
    assert baseline_ref["sigmaZ"] > 1.8, "baseline overdispersion is not determinate"
    assert abs(baseline_ref["centerLine"] - base_p) <= 0.02, (
        "the daily baseline window and the monthly ledger describe one process and must "
        "agree on its level")
    assert _pearson_dispersion_p(blocks["M_Baseline"]["defectCounts"],
                                 blocks["M_Baseline"]["sampleSizes"]) < 0.001

    # ANALYZE — the parametric branch's preconditions hold AND the effect is real.
    assert by[("basic.normality", "pValue", "A_Sources")] > 0.15
    assert by[("anova.equal_variances", "pValue", "A_Sources")] > 0.15
    assert by[("anova.oneway", "factorPValue", "A_Sources")] < 0.005
    assert by[("tables.chisquare_assoc", "pValue", "A_Stations")] < 0.005

    # IMPROVE — the model and the pilot both land on one side, with room to spare.
    assert by[("doe.factorial_analysis", "modelPValue", "I_Matrix")] < 0.005
    assert by[("doe.factorial_analysis", "rSquaredPct", "I_Matrix")] > 80.0
    assert by[("basic.two_proportions", "pValue", "I_Pilot")] < 0.005
    # A p-value truth of exactly 0.0 admits every small number and therefore measures
    # nothing. Every guard band above has a floor of 1e-6 and every p-value is stored at
    # 10 decimals, so neither the draw nor the rounding can produce one.
    for t in truths:
        if t.field.lower().endswith("pvalue"):
            assert t.expected > 0.0, f"{t.method_id}.{t.field} underflowed to zero"

    # CONTROL — the chart route and the closure verdict are the same for every seed.
    sizes = blocks["C_Released"]["sampleSizes"]
    assert max(sizes) / min(sizes) >= 1.4, (
        "the released window's period sizes must visibly vary, or a constant-size count chart "
        "stops being a wrong answer and the chart-route decision point is not a decision")
    assert monitor_ref["outOfControlCount"] == 0
    assert _sigma_z(blocks["C_Released"]["defectCounts"], sizes) < 1.15
    assert _pearson_dispersion_p(blocks["C_Released"]["defectCounts"], sizes) > 0.20
    # THE CROSS-PHASE DEPENDENCY: Control's pass criterion is the level Define committed to.
    confirmed = by[("capability.binomial", "avgP", "C_Confirmation")]
    assert confirmed < CHARTER_FAILURE_CEILING - 0.010, (
        f"confirmed failure rate {confirmed} does not clear the chartered ceiling "
        f"{CHARTER_FAILURE_CEILING} with margin — the closure verdict would flip on a reseed")
    assert base_p - confirmed >= 0.05, "the improvement must be unmistakable at every seed"
    assert blocks["C_Confirmation"]["charterFailureCeiling"] == CHARTER_FAILURE_CEILING


if __name__ == "__main__":
    bad = []
    for s in range(1, 501):
        try:
            generate(s)
        except AssertionError as e:
            bad.append((s, str(e)))
    print("failed seeds:", bad if bad else "NONE (500/500)")
