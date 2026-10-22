"""adb_c24 — the first case that grades all five DMAIC phases.

Before it, measured over the whole corpus: DEFINE carried 0 hard truths and 0 decision points,
so an agent that skipped Define forfeited nothing; CONTROL carried truths but 0 decision points,
so it was graded on arithmetic and never on whether the right sustaining strategy was chosen.
``tests/test_phase_coverage.py`` pins that at the corpus level. This file pins the properties of
the case that closed it, because "Define is graded now" is only true while four separate things
stay true, and each of them has been violated somewhere in this benchmark's history:

  1. every truth is re-derivable by ``truth/verifiers.py`` — the V7 gate. A self-derived truth
     passes validation by SILENCE (a method with no reference implementation is skipped), which
     is how a third of the corpus once went through the gate untouched;
  2. a decision point's branches route to GENUINELY DIFFERENT methods. Two branches running the
     same method are invisible to ``pq.branch_evidence`` and would score "does your adapter emit
     route_decisions" rather than "did you decide correctly";
  3. no wrong branch's method is required anywhere else in the case. ``pq._judge_point`` marks a
     point incorrect if ANY walked branch is outside the acceptable set — so a wrong-branch
     method that another stage legitimately needs turns a perfect run into a PQ failure. This is
     the authoring trap ``docs/archive/control-phase-design-2026-09-04.md`` §1.3 records having been
     learned the hard way;
  4. no method name reaches the agent-visible text, and no truth is readable off a payload.

The scoring assertions run real ``pq``/``nf`` over hand-built traces rather than trusting the
declarations, because points 2 and 3 are claims about what the SCORER sees, not about what the
YAML says.
"""
from __future__ import annotations

import json
import re

import pytest

from dmaic_bench import taxonomy as taxonomy_mod
from dmaic_bench.core import registry, validation
from dmaic_bench.core.models import PHASES, Trace, TraceStep, RouteDecision
from dmaic_bench.core.validation import _LEAKAGE_PATTERNS
from dmaic_bench.scoring import nf, pq
from dmaic_bench.tasks import builder

CASE_ID = "adb_c24"
SPOT_SEEDS = range(1, 31)

#: The deliverable table this case exists to move: hard truths and decision points per phase.
#:
#: analyze 4 -> 6 and improve 3 -> 4 when three of this case's warn-only truths were hardened:
#: the shape check (Shapiro-Wilk admitted at its own precision through `accepts`), the spread
#: check (whose centring the payload already declares), and the pilot z (whose comparison order
#: the payload already declares). A soft truth scores nothing either way, so those three
#: phases were being graded on fewer numbers than the table claimed.
EXPECTED_PHASE_TABLE = {
    "define":  {"truths": 3, "points": 1},
    "measure": {"truths": 4, "points": 1},
    "analyze": {"truths": 6, "points": 1},
    "improve": {"truths": 4, "points": 1},
    "control": {"truths": 4, "points": 1},
}

#: The route a competent agent walks. Nothing outside this set is required by any stage, which
#: is what lets every decision point carry an observable WRONG branch (property 3 above).
CORRECT_PATH = {
    "capability.binomial", "quality.pareto", "msa.attribute_agreement",
    "control_chart.laney_p", "basic.normality", "anova.equal_variances", "anova.oneway",
    "tables.chisquare_assoc", "doe.factorial_analysis", "basic.two_proportions",
    "control_chart.p",
}


@pytest.fixture(scope="module")
def case():
    return registry.discover(include_legacy=False)[CASE_ID]


@pytest.fixture(scope="module")
def data(case):
    return case.generate(1)


@pytest.fixture(scope="module")
def tax():
    return taxonomy_mod.load()


def _phase_of(case) -> dict:
    return {s.stage_id: s.phase for s in case.meta.stages}


def _by_key(data) -> dict:
    return {(t.method_id, t.field, t.stage_id): t.expected for t in data.truths}


# --------------------------------------------------------------------------- onboarding

class TestOnboarding:
    def test_validate_zero_errors(self):
        findings = validation.validate_case_dir(f"{registry.CASES_DIR}/{CASE_ID}")
        assert validation.errors(findings) == [], [str(f) for f in findings]

    def test_registered_parametric_and_english(self, case):
        assert case.meta.parametric is True
        assert case.meta.tier == "T3"
        assert case.meta.language == "en"
        assert case.meta.y_type == "attribute_proportion"

    def test_all_five_phases_are_present(self, case):
        assert sorted({s.phase for s in case.meta.stages}) == sorted(PHASES)

    def test_topics_are_disjoint_across_stages(self, case):
        """The steward routes by substring; two stages sharing a topic makes one unreachable."""
        seen = set()
        for s in case.meta.stages:
            assert not (set(s.topics) & seen), f"topic overlap at {s.stage_id}"
            seen |= set(s.topics)

    def test_every_stage_produces_a_block(self, case, data):
        assert set(data.blocks) == {s.stage_id for s in case.meta.stages}
        for sid, payload in data.blocks.items():
            assert len(json.dumps(payload, ensure_ascii=False)) > 200, sid

    def test_it_carries_fault_targets(self, case):
        assert len(case.meta.fault_targets) >= 1
        stage_ids = {s.stage_id for s in case.meta.stages}
        for f in case.meta.fault_targets:
            assert f.stage_id in stage_ids


# --------------------------------------------------------------------------- the headline

class TestEveryPhaseIsGraded:
    """The deliverable: hard truths AND decision points in all five phases, not three."""

    def test_the_per_phase_table(self, case, data):
        phase = _phase_of(case)
        table = {p: {"truths": 0, "points": 0} for p in PHASES}
        for t in data.truths:
            if not t.soft:
                table[phase[t.stage_id]]["truths"] += 1
        for dp in case.meta.decision_points:
            table[dp.phase]["points"] += 1
        assert table == EXPECTED_PHASE_TABLE, table

    @pytest.mark.parametrize("ph", sorted(EXPECTED_PHASE_TABLE))
    def test_no_phase_can_be_skipped_for_free(self, case, data, ph):
        phase = _phase_of(case)
        truths = [t for t in data.truths if phase[t.stage_id] == ph and not t.soft]
        points = [dp for dp in case.meta.decision_points if dp.phase == ph]
        assert truths, f"{ph} carries no hard truth — skipping it would forfeit nothing"
        assert points, f"{ph} carries no decision point — its routing is never judged"

    def test_define_and_control_are_the_phases_this_case_was_authored_for(self, case, data):
        """Stated explicitly so a future edit that guts them fails loudly rather than quietly."""
        phase = _phase_of(case)
        define = {(t.method_id, t.field) for t in data.truths
                  if phase[t.stage_id] == "define" and not t.soft}
        control = {(t.method_id, t.field) for t in data.truths
                   if phase[t.stage_id] == "control" and not t.soft}
        assert define == {("capability.binomial", "avgP"),
                          ("capability.binomial", "processZ"),
                          ("quality.pareto", "topCategoryPct")}
        assert control == {("control_chart.p", "centerLine"),
                           ("control_chart.p", "outOfControlCount"),
                           ("capability.binomial", "avgP"),
                           ("capability.binomial", "processZ")}


# --------------------------------------------------------------------------- V7

class TestEveryTruthIsIndependentlyRederived:
    """Corpus V7 coverage is 99.6% and this case must not be the thing that lowers it."""

    def test_full_verification_coverage(self, case):
        records = validation.verification_coverage(case)
        good, total, frac = validation.verified_fraction(records)
        unverified = [(r.method_id, r.field, r.status, r.detail)
                      for r in records if not r.verified]
        assert unverified == [], unverified
        assert frac == 1.0 and total == len(EXPECTED_PHASE_TABLE) * 0 + total
        assert total >= 20, "the truth set shrank"

    def test_no_truth_binds_a_method_without_a_reference_implementation(self, case, data):
        from dmaic_bench.truth import verifiers
        missing = sorted({t.method_id for t in data.truths}
                         - set(verifiers.REFERENCE_IMPLS))
        assert missing == [], (
            f"{missing} would pass the V7 gate by silence — the gate skips a method it cannot "
            f"recompute, which is exactly how a self-derived truth gets admitted")

    def test_every_hard_truth_carries_a_derivation_and_a_positive_tolerance(self, data):
        for t in data.truths:
            assert t.tol >= 0
            if not t.soft:
                assert t.derivation, f"{t.method_id}.{t.field}"
                if (t.method_id, t.field) != ("control_chart.p", "outOfControlCount"):
                    assert t.tol > 0, (
                        f"{t.method_id}.{t.field}: only an integer count may use tol=0")
            assert t.metric_cue, f"{t.method_id}.{t.field} has no metric_cue — HN cannot see it"

    def test_the_one_zero_tolerance_truth_is_an_integer_count(self, data):
        zero_tol = [t for t in data.truths if t.tol == 0]
        assert [(t.method_id, t.field) for t in zero_tol] == [
            ("control_chart.p", "outOfControlCount")]
        assert float(zero_tol[0].expected).is_integer()


# --------------------------------------------------------------------------- decision points

class TestDecisionPointsAreVisibleToTheScorer:
    def test_one_point_per_phase_with_disjoint_branch_methods(self, case):
        assert sorted(dp.phase for dp in case.meta.decision_points) == sorted(PHASES)
        for dp in case.meta.decision_points:
            branches = dp.branch_evidence
            assert len(branches) >= 2, f"{dp.point_id}: a single branch is not a decision"
            seen = set()
            for name, methods in branches.items():
                assert methods, f"{dp.point_id}/{name} has no evidence method"
                assert not (set(methods) & seen), (
                    f"{dp.point_id}: branches {name} and an earlier one share a method, so "
                    f"branch_evidence cannot tell them apart")
                seen |= set(methods)

    def test_no_branch_uses_a_family_wildcard(self, case):
        """`family:capability` would match both branches of the Define point at once."""
        for dp in case.meta.decision_points:
            for name, methods in dp.branch_evidence.items():
                assert not any(m.startswith("family:") for m in methods), \
                    f"{dp.point_id}/{name}"

    def test_correct_branch_is_on_the_required_path_and_wrong_branches_are_not(self, case):
        """Property 3: `pq._judge_point` marks a point incorrect if any walked branch is wrong.

        A wrong-branch method that some other stage REQUIRES is therefore walked by every
        competent agent, and turns a perfect run into a PQ failure. This is the trap the
        control-phase design records having hit in adb_c17.
        """
        required = {m.method_id for s in case.meta.stages for m in s.methods if m.required}
        assert required == CORRECT_PATH
        for dp in case.meta.decision_points:
            ok = {dp.correct_branch, *dp.acceptable_branches}
            for name, methods in dp.branch_evidence.items():
                if name in ok:
                    assert set(methods) <= required, f"{dp.point_id}/{name} is unreachable"
                else:
                    assert not (set(methods) & required), (
                        f"{dp.point_id}/{name} lists {sorted(set(methods) & required)}, which "
                        f"another stage requires — a correct agent would be scored incorrect")

    def test_every_branch_method_exists_in_the_taxonomy(self, case, tax):
        for dp in case.meta.decision_points:
            for methods in dp.branch_evidence.values():
                for m in methods:
                    assert m in tax, m

    def test_each_point_cites_a_source(self, case):
        for dp in case.meta.decision_points:
            assert len(dp.source) > 30, dp.point_id
            assert len(dp.rule) > 80, dp.point_id


# --------------------------------------------------------------------------- live scoring

def _trace(methods, outputs_by_method=None, route_decisions=()):
    outputs_by_method = outputs_by_method or {}
    steps = []
    for i, m in enumerate(methods):
        steps.append(TraceStep(step_id=i + 1, method_id=m, status="success",
                               outputs=outputs_by_method.get(m, {})))
    return Trace(system_id="test", task_id="t", steps=tuple(steps),
                 route_decisions=tuple(route_decisions))


def _t3(case, seed=1):
    return [t for t in builder.build_tasks(case, seeds=(seed,), tiers=("T3",))][0]


class TestAPerfectRunScoresPerfectly:
    """If a textbook-correct trajectory cannot score 1.0, the case is mis-authored."""

    def test_pq_is_one_for_the_correct_path(self, case, tax):
        task = _t3(case)
        # the correct path, in an order that satisfies every declared order constraint
        ordered = ["capability.binomial", "quality.pareto", "msa.attribute_agreement",
                   "control_chart.laney_p", "basic.normality", "anova.equal_variances",
                   "anova.oneway", "tables.chisquare_assoc", "doe.factorial_analysis",
                   "basic.two_proportions", "control_chart.p", "capability.binomial"]
        out = pq.score(task, _trace(ordered), tax)
        assert out["points_correct"] == 5
        assert out["points_unknown"] == 0
        assert out["order_violations"] == 0
        assert out["score"] == 1.0

    def test_nf_passes_every_truth_when_each_analysis_is_its_own_step(self, case):
        task = _t3(case)
        # capability.binomial carries a truth at TWO stages, so a contestant must write one
        # step per analysis; the merged view would show only the last (nf.step_outputs).
        steps, seen = [], {}
        for t in task.truths:
            key = t.method_id
            seen.setdefault(key, []).append(t)
        step_id = 0
        for method, entries in seen.items():
            groups = {}
            for t in entries:
                groups.setdefault(t.stage_id, {})[t.field] = t.expected
            for _stage, outputs in groups.items():
                step_id += 1
                steps.append(TraceStep(step_id=step_id, method_id=method, status="success",
                                       outputs=outputs))
        trace = Trace(system_id="test", task_id="t", steps=tuple(steps))
        details = nf.check_values(task, trace)
        summary = nf.summarize(details)
        assert summary["failed"] == 0, [d for d in details if d["status"] == "failed"]
        assert summary["not_computed"] == 0
        assert summary["ratio"] == 1.0

    def test_the_two_capability_studies_are_separable(self, case):
        """The cross-phase reuse must be scoreable, not a truth that can never both be hit."""
        task = _t3(case)
        cap = [t for t in task.truths if t.method_id == "capability.binomial"]
        assert {t.stage_id for t in cap} == {"D_Charter", "C_Confirmation"}
        baseline = {t.field: t.expected for t in cap if t.stage_id == "D_Charter"}
        confirmed = {t.field: t.expected for t in cap if t.stage_id == "C_Confirmation"}
        assert baseline["avgP"] != confirmed["avgP"]
        trace = Trace(system_id="test", task_id="t", steps=(
            TraceStep(step_id=1, method_id="capability.binomial", outputs=baseline),
            TraceStep(step_id=2, method_id="capability.binomial", outputs=confirmed)))
        statuses = [d["status"] for d in nf.check_values(task, trace)
                    if d["method_id"] == "capability.binomial"]
        assert set(statuses) == {"passed"}, statuses


class TestAWrongRouteIsCaught:
    @pytest.mark.parametrize("point_id,wrong_method", [
        ("project_y_selection", "capability.normal"),
        ("measurement_study_route", "msa.gage_rr_crossed"),
        ("pallet_source_comparison_route", "nonparametric.kruskal_wallis"),
        ("pilot_confirmation_route", "basic.paired_t"),
        ("sustaining_chart_route", "control_chart.np"),
        ("sustaining_chart_route", "control_chart.imr"),
    ])
    def test_walking_a_wrong_branch_is_scored_incorrect(self, case, tax, point_id, wrong_method):
        task = _t3(case)
        trace = _trace(sorted(CORRECT_PATH) + [wrong_method])
        verdicts = {d["point_id"]: d["verdict"]
                    for d in pq.score(task, trace, tax)["details"]
                    if d["kind"] == "decision_point"}
        assert verdicts[point_id] == "incorrect", (
            f"{wrong_method} is supposed to be observable as the wrong branch of {point_id}")
        others = {k: v for k, v in verdicts.items() if k != point_id}
        assert set(others.values()) == {"correct"}, (
            f"a single wrong turn spilled onto other points: {others}")

    def test_an_explicit_route_decision_beats_evidence(self, case, tax):
        task = _t3(case)
        trace = _trace(sorted(CORRECT_PATH),
                       route_decisions=[RouteDecision(point="sustaining_chart_route",
                                                      chosen_branch="individuals_chart")])
        verdicts = {d["point_id"]: d["verdict"]
                    for d in pq.score(task, trace, tax)["details"]
                    if d["kind"] == "decision_point"}
        assert verdicts["sustaining_chart_route"] == "incorrect"

    def test_silence_is_unknown_and_stays_in_the_denominator(self, case, tax):
        task = _t3(case)
        out = pq.score(task, _trace([]), tax)
        assert out["points_unknown"] == 5
        assert out["points_total"] == 5
        assert out["score"] < 1.0

    def test_running_the_analysis_out_of_order_violates_the_declared_prerequisites(
            self, case, tax):
        task = _t3(case)
        backwards = ["anova.oneway", "basic.normality", "anova.equal_variances",
                     "basic.two_proportions", "doe.factorial_analysis"]
        out = pq.score(task, _trace(backwards), tax)
        assert out["order_violations"] == 3
        assert out["order_total"] == 3


# --------------------------------------------------------------------------- leakage / payload

class TestNothingLeaks:
    def test_context_and_goal_name_no_method(self, case):
        text = case.meta.context + "\n" + case.meta.goal
        for pat in _LEAKAGE_PATTERNS:
            m = re.search(pat, text, re.IGNORECASE)
            assert m is None, f"context/goal leaks {m.group(0)!r}"

    def test_stage_labels_name_no_method(self, case):
        """V3 only scans context/goal; the labels are shown to the agent too."""
        for s in case.meta.stages:
            blob = s.label + " " + " ".join(s.topics)
            for pat in _LEAKAGE_PATTERNS:
                m = re.search(pat, blob, re.IGNORECASE)
                assert m is None, f"{s.stage_id} label/topics leak {m.group(0)!r}"

    def test_no_hard_truth_is_readable_off_its_own_payload(self, case, data):
        """A number the payload states is not a measurement of anything."""
        for t in data.truths:
            if t.soft:
                continue
            flat = nf.flatten(data.blocks[t.stage_id])
            hits = {k: v for k, v in flat.items() if abs(v - t.expected) <= t.tol}
            # An integer count truth of 0 collides with any zero in the payload by arithmetic
            # accident; it is excluded because reading "0" off a data column is not reading the
            # ANSWER off it — the agent still has to build the limits to know the count is zero.
            if (t.method_id, t.field) == ("control_chart.p", "outOfControlCount"):
                continue
            assert not hits, f"{t.method_id}.{t.field} is sitting in {t.stage_id}: {hits}"

    def test_the_charter_states_the_commitment_but_not_the_baseline(self, data):
        charter = data.blocks["D_Charter"]
        assert charter["customerMandate"]["committedLevelPct"] == 96.0
        assert charter["customerMandate"]["stretchLevelPct"] == 98.0
        flat = nf.flatten(charter["customerMandate"])
        assert not any(0.0 < v < 1.0 for v in flat.values()), (
            "the mandate must be a target, never the baseline the agent has to compute")


class TestDeclaredConventions:
    """An undeclared convention has twice shipped a truth the benchmark could not reproduce."""

    def test_the_k_sample_comparison_declares_its_variance_and_centering_reading(self, data):
        b = data.blocks["A_Sources"]
        assert b["assumeEqualVariances"] is True
        assert b["varianceTestCentering"] == "median"
        assert "pooled" in b["distributionCheckScope"]
        assert b["alternativeHypothesis"] == "NOT_EQUAL"

    def test_the_contingency_table_declares_no_continuity_correction(self, data):
        assert data.blocks["A_Stations"]["continuityCorrection"] is False

    def test_the_pilot_declares_tail_correction_error_and_sign(self, data):
        b = data.blocks["I_Pilot"]
        assert b["alternativeHypothesis"] == "NOT_EQUAL"
        assert b["continuityCorrection"] is False
        assert b["standardErrorConvention"] == "pooled"
        assert "before" in b["comparisonOrder"] and "after" in b["comparisonOrder"]

    def test_the_declared_tail_is_one_the_verifier_understands(self, data):
        from dmaic_bench.truth import verifiers
        for sid in ("A_Sources", "I_Pilot"):
            assert verifiers._alternative(data.blocks[sid]) == "two-sided"

    def test_the_design_declares_its_coding_and_its_terms(self, data):
        b = data.blocks["I_Matrix"]
        assert b["coding"] == "coded_units_-1_+1"
        assert len(b["termsInModel"]) == 6
        assert set(b["data"]["pressForce"]) == {-1, 1}

    def test_both_period_charts_declare_the_same_limit_convention(self, data):
        for sid in ("M_Baseline", "C_Released"):
            conv = data.blocks[sid]["limitConvention"]
            assert "pooled" in conv and "three standard errors" in conv
            assert "negative lower limit is reported as zero" in conv

    def test_the_confirmation_declares_that_no_sigma_shift_is_applied(self, data):
        b = data.blocks["C_Confirmation"]
        assert b["sigmaShiftApplied"] is False
        assert "unshifted" in b["sigmaShiftNote"]


# --------------------------------------------------------------------------- cross-phase

class TestControlIsJudgedAgainstWhatDefineCommittedTo:
    def test_the_charter_target_is_carried_into_the_control_payload(self, data):
        committed = data.blocks["D_Charter"]["customerMandate"]["committedLevelPct"]
        confirm = data.blocks["C_Confirmation"]
        assert confirm["charterCommittedLevelPct"] == committed
        assert confirm["charterFailureCeiling"] == pytest.approx(1 - committed / 100.0)
        assert "charter" in confirm["charterSource"]

    def test_a_t2_control_slice_is_solvable_on_its_own(self, case):
        """The coupling must be REWARDED, never REQUIRED — a phase slice never saw Define."""
        tasks = {t.phase: t for t in builder.build_tasks(case, tiers=("T2",))}
        control = tasks["control"]
        assert control.truths, "the control slice carries no truth"
        assert control.decision_points, "the control slice carries no decision point"
        for sid in ("C_Released", "C_Confirmation"):
            assert sid in control.data.blocks
        assert control.data.blocks["C_Confirmation"]["charterFailureCeiling"] > 0, (
            "without the ceiling in its own payload the sliced task is unanswerable")

    def test_every_phase_becomes_its_own_t2_task(self, case):
        phases = {t.phase for t in builder.build_tasks(case, tiers=("T2",))}
        assert phases == set(PHASES), (
            "a phase that carries no methods emits no slice; before this case, Define and "
            "Control slices did not exist at all")

    def test_the_confirmed_level_clears_the_chartered_ceiling(self, case):
        for seed in SPOT_SEEDS:
            d = case.generate(seed)
            by = _by_key(d)
            ceiling = d.blocks["C_Confirmation"]["charterFailureCeiling"]
            confirmed = by[("capability.binomial", "avgP", "C_Confirmation")]
            baseline = by[("capability.binomial", "avgP", "D_Charter")]
            assert confirmed < ceiling - 0.01, (seed, confirmed, ceiling)
            assert baseline - confirmed >= 0.05, (seed, baseline, confirmed)


# --------------------------------------------------------------------------- seed invariants

class TestInvariantsHoldAcrossSeeds:
    """The generator asserts these on every call; re-checking the headline facts here means a
    silent loosening of a guard cannot slip through unnoticed."""

    def test_thirty_seeds_generate(self, case):
        for seed in SPOT_SEEDS:
            case.generate(seed)

    def test_the_branch_conditions_never_flip(self, case):
        for seed in SPOT_SEEDS:
            d = case.generate(seed)
            by = _by_key(d)
            # DEFINE — the baseline stays on the recorded frame
            assert 0.085 < by[("capability.binomial", "avgP", "D_Charter")] < 0.108
            # MEASURE — the judgement is usable and the baseline is clearly overdispersed
            assert by[("msa.attribute_agreement", "kappaMin", "M_Judgement")] > 0.78
            assert by[("control_chart.laney_p", "sigmaZ", "M_Baseline")] > 1.8
            # ANALYZE — the parametric branch's preconditions hold AND the effect is real
            assert by[("basic.normality", "pValue", "A_Sources")] > 0.15
            assert by[("anova.equal_variances", "pValue", "A_Sources")] > 0.15
            assert by[("anova.oneway", "factorPValue", "A_Sources")] < 0.005
            assert by[("tables.chisquare_assoc", "pValue", "A_Stations")] < 0.005
            # IMPROVE
            assert by[("doe.factorial_analysis", "modelPValue", "I_Matrix")] < 0.005
            assert by[("basic.two_proportions", "pValue", "I_Pilot")] < 0.005
            # CONTROL — the sustaining chart route is decided by the data, every seed
            assert by[("control_chart.p", "outOfControlCount", "C_Released")] == 0.0
            sizes = d.blocks["C_Released"]["sampleSizes"]
            assert max(sizes) / min(sizes) >= 1.4

    def test_no_p_value_truth_underflows_to_an_unreportable_zero(self, case):
        """A truth of exactly 0.0 admits any small number and measures nothing."""
        for seed in SPOT_SEEDS:
            for t in case.generate(seed).truths:
                if t.field.lower().endswith("pvalue"):
                    assert t.expected > 0.0, (seed, t.method_id, t.field)

    def test_the_teardown_log_accounts_for_exactly_the_ledger_failures(self, case):
        for seed in SPOT_SEEDS:
            d = case.generate(seed)
            assert sum(d.blocks["D_Scope"]["counts"]) == \
                sum(d.blocks["D_Charter"]["defectCounts"])

    def test_the_seed_actually_changes_the_data(self, case):
        a = json.dumps(case.generate(1).blocks, sort_keys=True)
        b = json.dumps(case.generate(2).blocks, sort_keys=True)
        assert a != b

    def test_generation_is_deterministic(self, case):
        a = json.dumps(case.generate(7).blocks, sort_keys=True)
        b = json.dumps(case.generate(7).blocks, sort_keys=True)
        assert a == b
