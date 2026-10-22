"""Core-layer tests: taxonomy, registry discovery, onboarding validation, exemplar case."""
import copy

import pytest
import yaml

from dmaic_bench import taxonomy as taxonomy_mod
from dmaic_bench.core import registry, validation
from dmaic_bench.core.models import data_fingerprint

CASES_DIR = registry.CASES_DIR


@pytest.fixture(scope="module")
def tax():
    return taxonomy_mod.load()


@pytest.fixture(scope="module")
def native_cases():
    return registry.discover(include_legacy=False)


class TestTaxonomy:
    def test_covers_all_49_solver_specs(self, tax):
        # 49 solver-backed methods plus one trace-only VARIANT id (anova.welch), which a
        # contestant reaches by labelling a one-way ANOVA as Welch in its step note and which
        # has no solver spec of its own (2026-09-18 expert review, B022).
        # The second-domain portability pilot (dmaic_bench/truth/omics.py) adds fourteen methods in
        # the qc / design / expression / gwas families, none solver-backed; they are counted
        # apart so the quality-engineering vocabulary the paper describes stays pinned at 50.
        pilot = {m for m in tax.methods if m.split(".")[0] in ("qc", "design", "expression", "gwas")}
        assert len(pilot) == 14
        assert len(tax.methods) - len(pilot) == 50
        assert not tax.get("anova.welch").spec_keys
        spec_keys = {k for m in tax.methods.values() for k in m.spec_keys}
        assert len(spec_keys) == 49  # one spec key per solver method, no dangling keys

    def test_spec_key_mapping(self, tax):
        assert tax.method_for_spec_key("solver.anova.one-way.v1") == "anova.oneway"
        assert tax.method_for_spec_key("solver.doe.rsm-canonical.v1") == "doe.rsm_canonical"
        assert tax.method_for_spec_key("no.such.spec") is None

    def test_alias_resolution(self, tax):
        assert tax.resolve_alias("Mann-Whitney") == "nonparametric.mann_whitney"
        assert tax.resolve_alias("pareto analysis") == "quality.pareto"
        assert tax.resolve_alias("anova.oneway") == "anova.oneway"
        assert tax.resolve_alias("astrology") is None

    def test_families_and_applicability(self, tax):
        assert "nonparametric" in tax.families()
        m = tax.get("capability.normal")
        assert m.data_type == "continuous"
        assert "stability_confirmed" in m.prerequisites


class TestRegistry:
    def test_discovers_native_exemplar(self, native_cases):
        assert "adb_c13" in native_cases
        case = native_cases["adb_c13"]
        assert case.meta.parametric is True
        assert len(case.meta.stages) == 5

    def test_template_is_skipped(self, native_cases):
        assert "my_new_case" not in native_cases


class TestExemplarCase:
    def test_validation_clean(self):
        findings = validation.validate_case_dir(f"{CASES_DIR}/adb_c13")
        assert validation.errors(findings) == []

    def test_parametric_seeds_change_data_and_truth(self, native_cases):
        case = native_cases["adb_c13"]
        d1, d2 = case.generate(1), case.generate(2)
        assert data_fingerprint(d1.blocks) != data_fingerprint(d2.blocks)
        t1 = {(t.method_id, t.field): t.expected for t in d1.truths}
        t2 = {(t.method_id, t.field): t.expected for t in d2.truths}
        assert t1 != t2  # Truths are derived from the generated data and change with it.

    def test_same_seed_reproducible(self, native_cases):
        case = native_cases["adb_c13"]
        assert data_fingerprint(case.generate(7).blocks) == data_fingerprint(case.generate(7).blocks)

    def test_invariants_hold_across_seeds(self, native_cases):
        case = native_cases["adb_c13"]
        for seed in range(1, 31):  # full 500-seed sweep lives in the generator __main__
            data = case.generate(seed)
            by = {(t.method_id, t.field): t.expected for t in data.truths}
            assert by[("basic.descriptive_summary", "adPValue")] < 0.05
            assert by[("nonparametric.mann_whitney", "pValue")] < 0.01

    def test_hard_truths_carry_derivation(self, native_cases):
        data = native_cases["adb_c13"].generate(1)
        for t in data.truths:
            if not t.soft:
                assert t.derivation, f"{t.method_id}.{t.field} missing derivation"


class TestValidationGate:
    """The onboarding validator must reject each contract violation class."""

    def _meta_dict(self):
        with open(f"{CASES_DIR}/adb_c13/case.yaml", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_schema_rejects_bad_tier(self):
        raw = self._meta_dict()
        raw["tier"] = "T9"
        assert any(f.check == "V1-schema" for f in validation.validate_yaml_dict(raw))

    def test_leakage_rejected(self, native_cases):
        case = native_cases["adb_c13"]
        leaky_meta = copy.replace(case.meta, context=case.meta.context + "\nPlease start with ANOVA.") \
            if hasattr(copy, "replace") else None
        if leaky_meta is None:  # python<3.13 fallback
            import dataclasses
            leaky_meta = dataclasses.replace(case.meta, context=case.meta.context + "\nPlease start with ANOVA.")
        from dmaic_bench.core.models import Case
        findings = validation.validate_case(Case(meta=leaky_meta, generate=case.generate))
        assert any(f.check == "V3-leakage" for f in findings)

    def test_unknown_method_rejected(self, native_cases):
        import dataclasses
        from dmaic_bench.core.models import Case, Stage, StageMethod
        case = native_cases["adb_c13"]
        bad_stage = Stage(stage_id="N_Summary", phase="measure", label="x",
                          methods=(StageMethod(method_id="alchemy.transmute"),))
        meta = dataclasses.replace(case.meta, stages=(bad_stage,) + case.meta.stages[1:])
        findings = validation.validate_case(Case(meta=meta, generate=case.generate))
        assert any(f.check == "V2-taxonomy" for f in findings)

    def test_template_yaml_passes_schema(self):
        with open(f"{CASES_DIR}/_template/case.yaml", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
        assert validation.validate_yaml_dict(raw) == []
