"""Gates are derived from what a guard MEANS, not from matching its exact text.

`_GUARD_TO_GATE` was four literal strings. A guard written any other way silently got no
environment enforcement at all, and the difference was invisible: the four distinct-category
tasks guard on `msa.pctSV <= 0.30 and msa.ndc >= 5`, which is in no table, so their process run
was released the moment the gauge study was done — while sibling cases with the single-criterion
form were refused. `spec.PUBLIC_GATES` has carried `msa_ndc` the whole time; the string table
simply could not reach it.

Two properties have to hold together, and the second is the one that makes derivation safe:

* a guard's gates follow from its STRUCTURE, so a conjunction states both of its parts; and
* a gate no correct route can satisfy is never emitted, because that is a padlock on that route
  rather than a precondition. Derivation makes this reachable in a way the string table never
  was: `recipes` in adb_c37 is read by the parametric branch and by the rank branch, so gating
  it on normality padlocks exactly the seeds whose data is not normal.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
for p in (str(_ROOT), str(_ROOT / "harbor" / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pytest                                          # noqa: E402

from dmaic_bench.v2 import registry                    # noqa: E402
from dmaic_harbor import spec, v2_tasks as V           # noqa: E402

CASES = registry.discover()


@pytest.mark.parametrize("expr,expected", [
    ("msa.pctSV <= 0.30", ["msa_pass"]),
    ("msa.pctTol <= 0.30", ["msa_pass"]),
    ("msa.pctSV <= 0.30 and msa.ndc >= 5", ["msa_pass", "msa_ndc"]),
    ("imr.outOfControl == 0", ["stability_pass"]),
    ("xbar.outOfControl == 0", ["stability_pass"]),
    ("pchart.outOfControl == 0", ["stability_pass"]),
    ("normality.pValue >= 0.05", ["normality_pass"]),
    ("screen.modelPValue < 0.05", ["screening_significant"]),
])
def test_a_guard_states_the_gates_its_structure_implies(expr, expected):
    assert V.gates_for_guard(expr) == expected


@pytest.mark.parametrize("expr", [
    "cap.avgP <= 0.0015",                 # a case-specific threshold, not a handbook gate
    "cap1.cpk < cap2.cpk",                # field against field
    "msa.pctSV > 0.30 or msa.ndc < 5",    # a disjunction is not a precondition
    "msa.pctSV <= 0.25",                  # right field, wrong threshold
    "",
])
def test_an_unrecognised_guard_yields_nothing_rather_than_a_guess(expr):
    """A gate enforced on the wrong predicate is worse than one not enforced at all."""
    assert V.gates_for_guard(expr) == []


def test_the_units_are_the_guards_units_not_the_gate_definitions():
    """A v2 guard reads %StudyVariation as a FRACTION; PUBLIC_GATES states it in percent. The
    first version of the atom table used 30.0 and matched nothing at all."""
    assert V.gates_for_guard("msa.pctSV <= 0.30") == ["msa_pass"]
    assert V.gates_for_guard("msa.pctSV <= 30.0") == []
    assert spec.PUBLIC_GATES["msa_pass"]["value"] == 30.0


def test_no_emitted_gate_padlocks_a_route_that_needs_the_batch():
    """The safety property. adb_c37 is the case that proves it is not hypothetical."""
    from dmaic_bench.core.graph import walk
    from dmaic_bench.v2 import harbor_truth as HT
    field_of = V._GATE_ORACLE_FIELD
    bad = []
    for case_id, case in sorted(CASES.items()):
        entries = V.locks(case)
        blocks = V.data_nodes(case)
        for seed in case.seeds:
            _b, res = case.generate(seed)
            needed = {blocks.get(n) for n in walk(case.graph, res) if n in blocks}
            for batch, entry in entries.items():
                if batch not in needed:
                    continue
                for gate in entry["gates"]:
                    if gate not in field_of:
                        continue
                    field, scale = field_of[gate]
                    value = HT._read_dotted(res, field)
                    if value is None:
                        continue
                    d = spec.PUBLIC_GATES[gate]
                    value = float(value) * scale
                    ok = {"<=": value <= d["value"], ">=": value >= d["value"]}.get(d["op"], True)
                    if not ok:
                        bad.append((case_id, seed, batch, gate, round(value, 4)))
    assert not bad, f"gates padlocking a correct route: {bad}"


def test_adb_c37_keeps_the_recipes_batch_ungated():
    """Named, because it is the case the safety property exists for: the rank branch reads the
    same batch as the parametric one and its seeds are non-normal by construction."""
    assert not (V.locks(CASES["adb_c37"]).get("recipes") or {}).get("gates")


@pytest.mark.parametrize("case_id", ["adb_c30", "adb_c31"])
def test_the_distinct_category_traps_opt_out_explicitly(case_id):
    """Their guard now derives both AIAG gates, and enforcing them would make the trap
    unfailable: a contestant that declares ndc = 4 would simply be refused the next batch. The
    opt-out is declared per rule so the choice is reviewable, where it used to be an accident of
    a lookup table that happened not to contain the compound form."""
    case = CASES[case_id]
    opted = [r for r in case.gate_policy if r.get("enforce") is False]
    assert opted, f"{case_id} must declare its non-enforcement rather than rely on a table miss"
    assert not (V.locks(case).get("process_run") or {}).get("gates")


def test_opting_out_does_not_remove_the_obligation():
    """Path Quality still scores the decision the environment declines to enforce."""
    from dmaic_bench.core.graph import walk
    case = CASES["adb_c30"]
    _b, res = case.generate(4)          # a trap seed
    assert "M_msa_fix" in walk(case.graph, res)
