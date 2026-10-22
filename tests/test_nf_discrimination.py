"""The numeric-fidelity axis must be able to FAIL.

Measured starting point, on the English public build: `nf` had standard deviation 0.0000
across all 21 stored T3 trials and was exactly 1.000 on 99.5% of T2 trials — 288 passes
against 2 failures corpus-wide. The mechanism was not a bug in nf.py. It was the corpus:
45 of 118 registry truths were `soft`, and scoring/nf.py puts a soft miss in NEITHER the
numerator NOR the denominator, so on those entries a WRONG number and a SILENT one produce
the same verdict and the same score. A trace whose every reported number was 25 tolerances
off still scored nf = 1.000 on 112 of 366 English tasks.

What this file pins:

  * the corpus-wide soft count, so softness cannot creep back in unexamined;
  * that every remaining soft truth is one of the two DECLARED convention gaps;
  * that a deliberately-wrong trace actually fails, per case and corpus-wide;
  * that `TruthEntry.accepts` is populated and that each populated window is reproduced by
    the reference implementation it names — the alternative-convention machinery was fully
    built, unit-tested, and used by zero truths, which is why hardening had been blocked.

Nothing here asserts a truth VALUE or a TOLERANCE; those are pinned by tools/truth_digest.py.
"""
from __future__ import annotations

from types import SimpleNamespace as NS

import pytest

from dmaic_bench.core import registry
from dmaic_bench.scoring import nf
from dmaic_bench.truth import verifiers as V


#: (case_id, method_id, field) -> why this truth is still warn-only. Anything not on this list
#: must be scoreable; anything on it must have a reason that is about the QUANTITY, never about
#: an unverified field name.
KNOWN_SOFT = {
    ("adb_c02", "basic.normality", "statistic"):
        "Anderson-Darling A-squared and Shapiro-Wilk's W are different quantities on different "
        "scales, so no variant window can admit the second toolchain's answer under the name "
        "`statistic` without admitting an unrelated number.",
    ("adb_c18", "capability.grouped", "ppk"):
        "the payload does not say whether the grouped index is the WORST group, the pooled "
        "one, or the average; on seed 1 those are 1.019 / 1.109 / 1.398. Declaring it would "
        "change the task, so the gap is reported rather than closed by fiat.",
}

#: Corpus totals at seed 1. Hardening moved these from 45/73; they are pinned so that neither
#: a new soft truth nor a lost hard one lands without somebody editing this line on purpose.
EXPECTED_SOFT = 2
#: Two corpora, two floors (docs/HELD_OUT.md). The public release holds 15 of the 24 cases,
#: so it carries fewer hard truths in absolute terms; the guarantee -- that hardening did not
#: silently reverse -- is the same on both. Both are ratchets: they may only go up.
MIN_HARD_FULL = 116
MIN_HARD_PUBLIC = 78


def _min_hard():
    from dmaic_bench.v2.expert_migration import _legacy_bridge_available
    return MIN_HARD_FULL if _legacy_bridge_available() else MIN_HARD_PUBLIC


MIN_HARD = _min_hard()


@pytest.fixture(scope="module")
def corpus():
    return {cid: case.generate(1) for cid, case in sorted(registry.discover().items())}


def _wrong(t):
    """A value far outside the primary window AND every accepted variant window."""
    span = t.tol
    for _, exp_alt, tol_alt in (t.accepts or ()):
        span = max(span, abs(exp_alt - t.expected) + tol_alt)
    return t.expected + 25.0 * max(span, 1e-9)


def _trace(truths, values):
    return NS(steps=[NS(step_id=i, method_id=t.method_id, status="success",
                        outputs={t.field: v})
                     for i, (t, v) in enumerate(zip(truths, values))])


class TestTheAxisCanFail:
    def test_the_soft_count_is_pinned(self, corpus):
        soft = [(cid, t.method_id, t.field)
                for cid, d in corpus.items() for t in d.truths if t.soft]
        assert len(soft) == EXPECTED_SOFT, f"soft truths changed: {soft}"

    def test_every_remaining_soft_truth_is_a_declared_convention_gap(self, corpus):
        soft = {(cid, t.method_id, t.field)
                for cid, d in corpus.items() for t in d.truths if t.soft}
        assert soft == set(KNOWN_SOFT), (
            f"undocumented soft truths {soft - set(KNOWN_SOFT)}; "
            f"closed ones still listed {set(KNOWN_SOFT) - soft}")

    def test_the_corpus_carries_enough_hard_truths(self, corpus):
        hard = sum(1 for d in corpus.values() for t in d.truths if not t.soft)
        assert hard >= MIN_HARD, f"hard truths fell to {hard}"

    def test_a_correct_trace_scores_one(self, corpus):
        for cid, d in corpus.items():
            if not d.truths:
                continue
            trace = _trace(d.truths, [t.expected for t in d.truths])
            s = nf.summarize(nf.check_values(NS(truths=d.truths), trace))
            assert s["ratio"] == pytest.approx(1.0), (cid, s)

    def test_a_deliberately_wrong_trace_fails_every_case_that_has_a_hard_truth(self, corpus):
        survivors = []
        for cid, d in corpus.items():
            if not any(not t.soft for t in d.truths):
                continue
            trace = _trace(d.truths, [_wrong(t) for t in d.truths])
            s = nf.summarize(nf.check_values(NS(truths=d.truths), trace))
            if s["ratio"] > 0.0:
                survivors.append((cid, s))
        assert not survivors, f"nf survived a 25-tolerance error on {survivors}"

    def test_nf_is_measurable_on_all_but_one_case(self, corpus):
        """A case with no hard truth is a case where nf can never say anything."""
        blind = [cid for cid, d in corpus.items() if not any(not t.soft for t in d.truths)]
        # adb_c08 carries no truths at all — a corpus defect recorded elsewhere, not an nf one.
        # It is held out of the public release, so a public checkout has NO blind case, which
        # is the stronger property. Asserting a subset rather than equality states the real
        # guarantee (no case OTHER than the known one is blind) on both corpora, and still
        # fails the moment a new blind case appears.
        assert set(blind) <= {"adb_c08"}, f"a case with no hard truth appeared: {blind}"


class TestAcceptsIsActuallyUsed:
    def test_at_least_one_truth_declares_an_alternative_convention(self, corpus):
        used = [(cid, t.method_id, t.field, t.accepts)
                for cid, d in corpus.items() for t in d.truths if t.accepts]
        assert used, ("TruthEntry.accepts is populated on no truth again — every "
                      "convention-variant quantity is then either soft (unfailable) or "
                      "scores idiomatic R as wrong")

    def test_each_declared_variant_is_reproduced_by_the_reference_it_names(self, corpus):
        """A hand-written variant number would be exactly the defect accepts exists to end."""
        checked = 0
        for cid, case in sorted(registry.discover().items()):
            data = corpus[cid]
            for t in data.truths:
                for name, exp_alt, tol_alt in (t.accepts or ()):
                    impls = dict((n, f) for n, f, _ in
                                 V.CONVENTION_VARIANTS.get(t.method_id, ()))
                    assert name in impls, f"{cid} {t.method_id}: no reference for {name!r}"
                    payload = data.blocks[t.stage_id]
                    got = impls[name](payload)[t.field]
                    assert abs(got - exp_alt) <= max(tol_alt, 1e-9), (cid, name, got, exp_alt)
                    checked += 1
        assert checked, "no variant windows to check"

    def test_a_variant_never_widens_the_primary_window(self, corpus):
        for cid, d in corpus.items():
            for t in d.truths:
                for name, exp_alt, tol_alt in (t.accepts or ()):
                    assert tol_alt <= t.tol, (cid, name, tol_alt, t.tol)
                    gap = abs(exp_alt - t.expected)
                    assert gap > t.tol, (cid, name, "variant is inside the primary window")
                    assert tol_alt + t.tol < gap, (
                        cid, name, "the two windows touch — a value that is neither "
                                   "convention would pass")

    def test_nothing_between_the_two_windows_passes(self, corpus):
        """A variant is admitted at ITS OWN precision, not by widening the primary window.

        Tested where it actually bites: the midpoint of the GAP between the two windows'
        near edges. (The midpoint of the two CENTRES is not the right probe — where a
        primary tolerance is generous the centre-midpoint can legitimately sit inside the
        primary window, which says something about that tolerance, not about `accepts`.)
        """
        for cid, d in corpus.items():
            for t in d.truths:
                for _name, exp_alt, tol_alt in (t.accepts or ()):
                    lo, hi = sorted((t.expected, exp_alt))
                    lo_edge = lo + (t.tol if lo == t.expected else tol_alt)
                    hi_edge = hi - (t.tol if hi == t.expected else tol_alt)
                    assert hi_edge > lo_edge, (cid, "windows touch")
                    probe = 0.5 * (lo_edge + hi_edge)
                    v = nf.check_values(NS(truths=[t]), _trace([t], [probe]))[0]
                    assert v["status"] == "failed", (cid, t.method_id, t.field, probe)


class TestConventionWindows:
    """Unit-level gating rules for the builder that populates accepts."""

    PAYLOAD = {"events1": 15, "trials1": 150, "events2": 4, "trials2": 150}

    def test_a_declared_convention_suppresses_its_variant(self):
        declared = dict(self.PAYLOAD, continuityCorrection=False)
        assert V.convention_windows("basic.two_proportions", "pValue", declared,
                                    0.0065, 0.0045) == ()

    def test_an_undeclared_convention_that_differs_is_admitted(self):
        got = V.convention_windows("basic.two_proportions", "pValue", self.PAYLOAD,
                                   0.0065, 0.0045)
        assert [n for n, _, _ in got] == ["yates_continuity"]
        name, exp, tol = got[0]
        assert exp == pytest.approx(V.two_proportions_yates(self.PAYLOAD)["pValue"])
        assert tol <= 0.0045

    def test_a_variant_inside_the_primary_window_is_dropped(self):
        # A window wide enough to hold both conventions needs no second window.
        assert V.convention_windows("basic.two_proportions", "pValue", self.PAYLOAD,
                                    0.0065, 0.05) == ()

    def test_a_method_with_no_alternative_yields_nothing(self):
        assert V.convention_windows("quality.pareto", "topCategoryPct",
                                    {"counts": [5, 3, 2]}, 50.0, 1.0) == ()

    def test_a_payload_the_reference_refuses_yields_nothing(self):
        assert V.convention_windows("basic.two_proportions", "pValue", {"nonsense": 1},
                                    0.5, 0.01) == ()

    def test_yates_is_a_two_by_two_only_default(self):
        with pytest.raises(V.NotVerifiable):
            V.chisquare_assoc_yates({"table": [[10, 20, 30], [15, 25, 35]]})

    def test_welch_anova_reduces_to_welchs_t_test_on_two_groups(self):
        """The independent check: for k=2 Welch's F is Welch's t squared, same p-value.

        SciPy has no ``f_oneway(equal_var=False)`` at the pinned version, so the reference is
        the identity rather than another call to the same library — which is stronger anyway.
        """
        from scipy import stats
        a = [12.1, 13.4, 11.8, 12.9, 13.1, 12.2]
        b = [15.2, 14.8, 16.1, 15.5, 14.9, 15.8, 16.4]
        got = V.anova_oneway_welch({"groups": {"a": a, "b": b}})
        t = stats.ttest_ind(a, b, equal_var=False)
        assert got["fStatistic"] == pytest.approx(t.statistic ** 2, rel=1e-10)
        assert got["factorPValue"] == pytest.approx(t.pvalue, rel=1e-10)

    def test_welch_f_is_smaller_than_the_classic_f_it_corrects(self):
        groups = {"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6], "c": [3, 4, 5, 6, 7]}
        welch = V.anova_oneway_welch({"groups": groups})["fStatistic"]
        classic = V.anova_oneway({"groups": groups})["fStatistic"]
        assert 0 < welch < classic, "Welch's denominator correction is >= 1 by construction"

    def test_shapiro_declines_a_sample_too_small_to_test(self):
        with pytest.raises(V.NotVerifiable):
            V.normality_shapiro({"data": [1.0, 2.0]})
