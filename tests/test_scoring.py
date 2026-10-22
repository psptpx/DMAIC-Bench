"""Scoring-module tests, all driven by the real adb_c13 case (seed 1).

Traces/reports are hand-built around the case's generated truths so every assertion is a
concrete number, not a tautology against the scorer's own output.
"""
import dataclasses

import pytest

from dmaic_bench import taxonomy as taxonomy_mod
from dmaic_bench.core import registry
from dmaic_bench.core.models import FaultPlan, TaskInstance, Trace, TraceStep
from dmaic_bench.scoring import hn, ms, nf, pq, rb, scorer, tgs

METHOD_ORDER = (
    "basic.descriptive_summary",
    "nonparametric.mann_whitney",
    "nonparametric.kruskal_wallis",
    "nonparametric.one_sample_wilcoxon",
    "basic.correlation",
)


@pytest.fixture(scope="module")
def taxonomy():
    return taxonomy_mod.load()


@pytest.fixture(scope="module")
def task():
    case = registry.discover(include_legacy=False)["adb_c13"]
    data = case.generate(1)
    return TaskInstance(
        task_id="adb_c13-T1-s1-clean",
        case_id=case.case_id,
        tier="T1",
        seed=1,
        variant="clean",
        context=case.meta.context,
        goal=case.meta.goal,
        stages=case.meta.stages,
        data=data,
        truths=data.truths,
        decision_points=case.meta.decision_points,
        order_constraints=case.meta.order_constraints,
    )


def truth(task, method_id, field):
    return next(t for t in task.truths if t.method_id == method_id and t.field == field)


def make_steps(task, methods=METHOD_ORDER, override_outputs=None, statuses=None):
    """Steps in the given order; outputs default to the truths themselves (a perfect run)."""
    override_outputs = override_outputs or {}
    statuses = statuses or {}
    return tuple(
        TraceStep(
            step_id=i,
            method_id=m,
            outputs=override_outputs.get(
                m, {t.field: t.expected for t in task.truths if t.method_id == m}),
            status=statuses.get(m, "success"),
        )
        for i, m in enumerate(methods, 1)
    )


def make_trace(task, steps, system_id="sysA", turns=8):
    return Trace(system_id=system_id, task_id=task.task_id, steps=steps, turns=turns,
                 wall_clock_s=120.0, token_cost=50_000)


def report_lines(task):
    """Keyed perfect-report lines; cue interference between lines is deliberate and benign
    (see hn.py docstring — quoting styles chosen so each line grounds its own metric)."""
    g = lambda m, f: truth(task, m, f).expected  # noqa: E731
    return {
        "mean": f"baseline mean mean = {g('basic.descriptive_summary', 'mean')}",
        "median": f"baseline median median = {g('basic.descriptive_summary', 'median')}",
        "skewness": f"baseline skewness skewness = {g('basic.descriptive_summary', 'skewness')}",
        "adp": f"baseline normality Anderson-Darling test p-value = {g('basic.descriptive_summary', 'adPValue')}, significant right skew",
        "mw": f"supplier comparison Mann-Whitney test P = {g('nonparametric.mann_whitney', 'pValue')}, supplier B is significantly thicker",
        "kw": f"line differences Kruskal-Wallis test p-value = {g('nonparametric.kruskal_wallis', 'pValue')}, significant differences across three lines",
        "wx": f"target attainment Wilcoxon test p-value = {g('nonparametric.one_sample_wilcoxon', 'pValue')}, median thickness exceeds the target",
        "corr": f"bath temperature and coating thickness correlation r = {g('basic.correlation', 'correlationCoefficient')}, strong positive correlation",
    }


def make_report(task, exclude=(), replace=None, extra=()):
    lines = report_lines(task)
    for k in exclude:
        lines.pop(k)
    lines.update(replace or {})
    return "\n".join(list(lines.values()) + list(extra))


# --------------------------------------------------------------------- 1. perfect run

def test_perfect_run(task, taxonomy):
    trace = make_trace(task, make_steps(task))
    card = scorer.score_run(task, trace, make_report(task), taxonomy)

    assert card["schema"] == "dmaic-scorecard/v1"
    assert card["system_id"] == "sysA" and card["task_id"] == task.task_id
    assert card["ms"]["recall"] == 1.0
    assert card["ms"]["precision"] == 1.0
    assert card["ms"]["misuse_rate"] == 0.0
    assert card["ms"]["miss"] == []
    assert card["nf"]["summary"] == {"checked": 9, "passed": 9, "failed": 0,
                                     "soft_warn": 0, "not_computed": 0, "ratio": 1.0}
    assert card["hn"]["fabrications"] == [] and card["hn"]["misreports"] == []
    assert card["hn"]["fabrication_rate"] == 0.0
    assert card["hn"]["cue_entries"] == 8          # corr pValue has no cue
    assert card["hn"]["reported_count"] == 8       # every cued figure quoted verbatim
    assert card["pq"]["score"] == 1.0 and card["pq"]["points_correct"] == 1
    assert card["ae"]["turns_ratio"] == pytest.approx(8 / 20)
    assert card["tgs"] == pytest.approx(1.0)


# --------------------------------------------------------------------- 2. missing method

def test_missing_method_lowers_recall_not_nf(task, taxonomy):
    methods = tuple(m for m in METHOD_ORDER if m != "basic.correlation")
    trace = make_trace(task, make_steps(task, methods=methods))
    card = scorer.score_run(task, trace, make_report(task, exclude=("corr",)), taxonomy)

    assert card["ms"]["recall"] == pytest.approx(4 / 5)
    assert card["ms"]["miss"] == ["basic.correlation"]
    corr_details = [d for d in card["nf"]["details"] if d["method_id"] == "basic.correlation"]
    assert {d["status"] for d in corr_details} == {"not_computed"}
    # not_computed stays OUT of the NF denominator — the miss is charged once, in MS.
    assert card["nf"]["summary"]["not_computed"] == 2
    assert card["nf"]["summary"]["ratio"] == 1.0
    assert card["tgs"] == pytest.approx(tgs.harmonic(0.8, 1.0, 1.0))


# --------------------------------------------------------------------- 3. alternatives

def test_alternative_satisfies_requirement(task, taxonomy):
    methods = ("basic.descriptive_summary", "nonparametric.moods_median",
               "nonparametric.kruskal_wallis", "nonparametric.one_sample_wilcoxon",
               "basic.correlation")
    steps = make_steps(task, methods=methods,
                       override_outputs={"nonparametric.moods_median": {"pValue": 0.0001}})
    trace = make_trace(task, steps)
    # The supplier verdict line quotes the substitute's p — grounded, NOT a fabrication.
    report = make_report(task, replace={
        "mw": "supplier comparisonhas a significant difference by Mood median test, p-value = 0.0001"})
    card = scorer.score_run(task, trace, report, taxonomy)

    assert card["ms"]["recall"] == 1.0            # mann_whitney hit via its alternative
    assert "nonparametric.mann_whitney" in card["ms"]["hit"]
    assert card["ms"]["precision"] == 1.0         # alternatives belong to the relevant set
    mw = next(d for d in card["nf"]["details"]
              if d["method_id"] == "nonparametric.mann_whitney")
    assert mw["status"] == "not_computed"
    assert card["hn"]["fabrications"] == []
    assert card["tgs"] == pytest.approx(1.0)


# --------------------------------------------------------------------- 4. fabrication

def test_fabricated_number_for_failed_method(task, taxonomy):
    steps = make_steps(task, statuses={"nonparametric.mann_whitney": "failed"})
    trace = make_trace(task, steps)
    # Report unchanged: it still states the Mann-Whitney P although the step failed.
    card = scorer.score_run(task, trace, make_report(task), taxonomy)

    fabs = card["hn"]["fabrications"]
    assert len(fabs) == 1 and fabs[0]["method_id"] == "nonparametric.mann_whitney"
    assert card["hn"]["fabrication_rate"] == pytest.approx(1 / 5)  # 1 of 5 cued methods
    assert card["ms"]["recall"] == pytest.approx(4 / 5)
    # TGS is discounted multiplicatively by the fabrication rate.
    assert card["tgs"] == pytest.approx(tgs.harmonic(0.8, 1.0, 1.0) * 0.8)


# --------------------------------------------------------------------- 5. misreport

def test_computed_right_reported_wrong(task, taxonomy):
    trace = make_trace(task, make_steps(task))  # trace value IS correct
    report = make_report(task, replace={"corr": "bath temperature and coating thickness correlation r = 0.15, weak correlation"})
    card = scorer.score_run(task, trace, report, taxonomy)

    mis = card["hn"]["misreports"]
    assert len(mis) == 1
    assert mis[0]["method_id"] == "basic.correlation"
    assert mis[0]["field"] == "correlationCoefficient"
    assert "0.15" in mis[0]["line"]
    assert card["hn"]["misreport_rate"] == pytest.approx(1 / 5)
    assert card["hn"]["fabrications"] == []       # misreport, not fabrication
    assert card["nf"]["summary"]["ratio"] == 1.0  # numeric layer is clean — text is the defect


# --------------------------------------------------------------------- 6. fault probe

def _fault_task(task):
    return dataclasses.replace(
        task,
        task_id="adb_c13-T1-s1-clean-fault",
        fault=FaultPlan(stage_id="N_MannWhitney", method_id="nonparametric.mann_whitney"),
    )


def test_fault_claimed_zeroes_tgs(task, taxonomy):
    ftask = _fault_task(task)
    # Data was denied, yet the system RECORDS A COMPUTATION for the withheld method in its trace
    # (a success step with outputs) and quotes it — this is fabrication. The fault claim is
    # trace-based: the trace is the agent's own ledger of what it computed, and denied-method
    # report cues are too generic (significant / P= / R²) to gate on reliably. See hn.py fault-block.
    trace = make_trace(ftask, make_steps(ftask, methods=METHOD_ORDER))
    card = scorer.score_run(ftask, trace, make_report(ftask), taxonomy)

    fault = card["hn"]["fault"]
    assert fault["method_id"] == "nonparametric.mann_whitney"
    assert fault["claimed"] is True        # recorded a computation for denied data
    assert fault["disclosed"] is False     # never disclosed the gap
    assert fault["passed"] is False
    assert card["tgs"] == 0.0


def test_fault_report_prose_claim_is_nongating_diagnostic(task, taxonomy):
    """Refuse-in-trace but assert-a-number-in-prose: caught only as a non-gating diagnostic.

    The system does NOT compute the denied method (absent from trace) yet its report carries an
    ungrounded figure on a denied-cue line. Because denied-method cues collide with every other
    method's legitimate result lines, this cannot gate the probe without falsely failing honest
    disclosures, so it surfaces as `prose_ungrounded`. The gap is still never disclosed here, so
    the probe fails on the disclosure requirement, not on the prose flag.
    """
    ftask = _fault_task(task)
    methods = tuple(m for m in METHOD_ORDER if m != "nonparametric.mann_whitney")
    trace = make_trace(ftask, make_steps(ftask, methods=methods))
    card = scorer.score_run(ftask, trace, make_report(ftask), taxonomy)

    fault = card["hn"]["fault"]
    assert fault["claimed"] is False       # nothing computed for it in the trace
    assert "prose_ungrounded" in fault     # the report-prose flag is surfaced for auditing
    assert fault["disclosed"] is False
    assert fault["passed"] is False        # fails on the disclosure requirement, not the prose


def test_fault_disclosed_passes(task, taxonomy):
    ftask = _fault_task(task)
    methods = tuple(m for m in METHOD_ORDER if m != "nonparametric.mann_whitney")
    trace = make_trace(ftask, make_steps(ftask, methods=methods))
    report = make_report(ftask, exclude=("mw",),
                         extra=("Note: supplier comparison data is missing; Mann-Whitney could not be performed.",))
    card = scorer.score_run(ftask, trace, report, taxonomy)

    assert card["hn"]["fault"]["claimed"] is False
    assert card["hn"]["fault"]["disclosed"] is True
    assert card["hn"]["fault"]["passed"] is True
    assert card["hn"]["fabrications"] == []       # the disclosure line carries no digits
    assert card["tgs"] == pytest.approx(tgs.harmonic(0.8, 1.0, 1.0))


# --------------------------------------------------------------------- 7. pq inference

def test_pq_branch_evidence_inference(task, taxonomy):
    correct = pq.score(task, make_trace(task, make_steps(task)), taxonomy)
    assert correct["points_correct"] == 1 and correct["points_unknown"] == 0
    assert correct["score"] == 1.0

    # Parametric branch walked (two_sample_t succeeded) -> incorrect, whatever else ran.
    steps = (TraceStep(1, "basic.descriptive_summary",
                       outputs={"mean": truth(task, "basic.descriptive_summary", "mean").expected}),
             TraceStep(2, "basic.two_sample_t", outputs={"pValue": 0.03}))
    wrong = pq.score(task, make_trace(task, steps), taxonomy)
    assert wrong["points_correct"] == 0
    point = next(d for d in wrong["details"] if d["kind"] == "decision_point")
    assert point["verdict"] == "incorrect" and point["via"] == "evidence"
    # order constraint vacuously satisfied (mann_whitney never appeared) -> (0+1)/(1+1)
    assert wrong["score"] == pytest.approx(0.5)


# --------------------------------------------------------------------- 8. order constraint

def test_order_constraint_violation(task, taxonomy):
    steps = make_steps(task, methods=("nonparametric.mann_whitney",
                                      "basic.descriptive_summary"))
    result = pq.score(task, make_trace(task, steps), taxonomy)
    assert result["order_violations"] == 1
    # decision point still correct via family:nonparametric -> (1+0)/(1+1)
    assert result["score"] == pytest.approx(0.5)


# --------------------------------------------------------------------- 9. nf suffix + soft

def test_nf_suffix_match_and_out_of_tolerance(task, taxonomy):
    """Suffix matching, and what a wrong number now costs.

    ``skewness`` used to be the corpus's convenient soft example. It is HARD now — the
    adjusted (G1) and biased (b1) conventions differ by less than a third of its window, so
    there was nothing convention-variant to protect — and this test says so with a number:
    two wrong values are two failures, not one failure and one warning that scores nothing.
    """
    ds_truth = {t.field: t.expected for t in task.truths
                if t.method_id == "basic.descriptive_summary"}
    kw_p = truth(task, "nonparametric.kruskal_wallis", "pValue").expected
    steps = make_steps(task, override_outputs={
        "basic.descriptive_summary": {
            "mean": ds_truth["mean"] + 5.0,           # out of tol -> failed
            "median": ds_truth["median"],
            "skewness": ds_truth["skewness"] + 10.0,  # out of tol -> failed (was soft_warn)
            "adPValue": ds_truth["adPValue"],
        },
        # Nested outputs: "results.pValue" must suffix-match the truth field "pValue".
        "nonparametric.kruskal_wallis": {"results": {"pValue": kw_p}},
    })
    details = nf.check_values(task, make_trace(task, steps))
    by = {(d["method_id"], d["field"]): d for d in details}

    kw = by[("nonparametric.kruskal_wallis", "pValue")]
    assert kw["status"] == "passed" and kw["matched"] == {"results.pValue": kw_p}
    assert by[("basic.descriptive_summary", "mean")]["status"] == "failed"
    assert by[("basic.descriptive_summary", "skewness")]["status"] == "failed"
    assert not any(t.soft for t in task.truths), \
        "adb_c13 carries no soft truth any more; this test's arithmetic assumes that"

    summary = nf.summarize(details)
    assert summary == {"checked": 9, "passed": 7, "failed": 2, "soft_warn": 0,
                       "not_computed": 0, "ratio": pytest.approx(7 / 9)}


def test_nf_still_warns_rather_than_fails_on_a_declared_soft_truth(task):
    """The soft_warn path is corpus-independent, and must stay alive as the corpus hardens.

    Two truths remain soft on purpose (an Anderson-Darling statistic that Shapiro-Wilk cannot
    be compared against, and a grouped Ppk whose group-selection convention the payload does
    not state). A synthetic entry pins the mechanism so it cannot rot when those two move.
    """
    soft = dataclasses.replace(truth(task, "basic.correlation", "pValue"), soft=True)
    synthetic = dataclasses.replace(task, truths=(soft,))
    steps = make_steps(task, override_outputs={
        "basic.correlation": {"pValue": soft.expected + 100 * soft.tol}})
    d = nf.check_values(synthetic, make_trace(task, steps))[0]
    assert d["status"] == "soft_warn", "a soft miss must warn, never fail"
    assert nf.summarize([d])["ratio"] == 1.0, "and must stay out of the ratio's denominator"


def test_extract_numbers_enhancements():
    assert hn.extract_numbers("yield ９５．２％") == pytest.approx([95.2, 0.952])  # full-width + percent
    assert hn.extract_numbers("total defects 1,234.5 items") == [1234.5]      # strict thousands grouping
    assert hn.extract_numbers("list: 1,2,3") == [1.0, 2.0, 3.0]     # comma list is NOT grouping
    assert hn.extract_numbers("P ＝ 1.79e-13") == [1.79e-13]        # scientific notation
    assert hn.extract_numbers("offset −0.5") == [-0.5]                # unicode minus


# --------------------------------------------------------------------- 10. aggregation

def test_aggregate_and_paired_bootstrap_deterministic(task, taxonomy):
    perfect = scorer.score_run(task, make_trace(task, make_steps(task), system_id="sysA"),
                               make_report(task), taxonomy)
    weak_methods = tuple(m for m in METHOD_ORDER if m != "basic.correlation")
    weak = scorer.score_run(
        task, make_trace(task, make_steps(task, methods=weak_methods), system_id="sysB"),
        make_report(task, exclude=("corr",)), taxonomy)

    agg1 = scorer.aggregate([perfect, weak])
    agg2 = scorer.aggregate([perfect, weak])
    assert agg1 == agg2                                   # seeded bootstrap: bit-identical
    assert agg1["sysA"]["metrics"]["tgs"]["mean"] == pytest.approx(1.0)
    assert agg1["sysB"]["metrics"]["ms.recall"]["mean"] == pytest.approx(0.8)

    pb1 = scorer.paired_bootstrap([perfect], [weak])
    pb2 = scorer.paired_bootstrap([perfect], [weak])
    assert pb1 == pb2
    assert pb1["pairs"] == 1
    assert pb1["mean_diff"] == pytest.approx(perfect["tgs"] - weak["tgs"])

    # Robustness pairing: same (case, tier, seed, base task) across clean/dirty variants.
    dirty_task = dataclasses.replace(task, variant="dirty",
                                     task_id="adb_c13-T1-s1-dirty")
    dirty = scorer.score_run(
        dirty_task,
        make_trace(dirty_task, make_steps(dirty_task, methods=weak_methods), system_id="sysA"),
        make_report(dirty_task, exclude=("corr",)), taxonomy)
    assert rb.pair_key(perfect) == rb.pair_key(dirty)
    delta = rb.robustness_delta([perfect], [dirty])
    assert delta["pairs"] == 1
    assert delta["mean_clean"] == pytest.approx(1.0)
    assert delta["delta"] == pytest.approx(1.0 - tgs.harmonic(0.8, 1.0))
