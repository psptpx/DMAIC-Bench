"""Tests for task construction (perturb/fault/builder) and the harness (steward/runner)."""
import dataclasses

import pytest

from dmaic_bench.core.models import (Case, CaseData, CaseMeta, FaultPlan, FaultTarget,
                                         RunResult, Stage, StageMethod, TaskInstance, Trace,
                                         TruthEntry)
from dmaic_bench.core import i18n
from dmaic_bench.core.registry import discover
from dmaic_bench.harness import runner
from dmaic_bench.harness.steward import DataSteward
from dmaic_bench.tasks import builder, fault, perturb


@pytest.fixture(scope="module")
def mini_case():
    return discover(include_legacy=False)["adb_c13"]


# --------------------------------------------------------------------------- helpers

def _iter_leaves(node):
    if isinstance(node, dict):
        for v in node.values():
            yield from _iter_leaves(v)
    elif isinstance(node, list):
        for v in node:
            yield from _iter_leaves(v)
    else:
        yield node


def _fake_t3_case():
    stages = (
        Stage(stage_id="S_M", phase="measure", label="measurement system analysis", topics=("measurement", "msa"),
              methods=(StageMethod("gage.rr"),), summary_fact="MSA passed (%GRR=8%)"),
        Stage(stage_id="S_A", phase="analyze", label="line comparison", topics=("difference", "comparison"),
              methods=(StageMethod("anova.oneway"),)),  # no summary_fact -> label fallback
        Stage(stage_id="S_C", phase="control", label="control chart monitoring", topics=("control", "monitoring"),
              methods=(StageMethod("controlchart.imr"),)),
    )
    meta = CaseMeta(
        case_id="fake_t3", title="fake T3 case", tier="T3", industry="test",
        provenance="SIMULATED", y_type="continuous", context="A factory background.", goal="Complete the improvement.",
        stages=stages,
        fault_targets=(FaultTarget("S_A", "anova.oneway"),),
    )

    def gen(seed):
        blocks = {
            "S_M": {"data": [float(i) for i in range(10)]},
            "S_A": {"group1": [1.0] * 10, "group2": [2.0] * 10},
            "S_C": {"data": [float(i) for i in range(12)]},
        }
        truths = (
            TruthEntry("gage.rr", "grrPercent", 8.0, 0.5, stage_id="S_M"),
            TruthEntry("anova.oneway", "pValue", 0.001, 0.001, stage_id="S_A"),
            TruthEntry("controlchart.imr", "ucl", 13.0, 0.1, stage_id="S_C"),
        )
        return CaseData(seed=seed, blocks=blocks, truths=truths)

    return Case(meta=meta, generate=gen)


def _full_task(mini_case, seed=1, fault_plan=None):
    data = mini_case.generate(seed)
    return TaskInstance(
        task_id="adb_c13-full", case_id="adb_c13", tier="T3", seed=seed,
        variant="clean", context=mini_case.meta.context, goal=mini_case.meta.goal,
        stages=tuple(mini_case.meta.stages), data=data, truths=data.truths,
        fault=fault_plan,
    )


# --------------------------------------------------------------------------- 1. T1 build

@pytest.mark.parametrize("language,suffix", [("en", "-en")])
def test_t1_build_one_task_per_stage(mini_case, language, suffix):
    """The official English build retains the historical English task identifiers."""
    tasks = builder.build_tasks(mini_case, seeds=(1,), languages=(language,))
    assert len(tasks) == 5
    assert len(builder.build_tasks(mini_case, seeds=(1, 2), languages=(language,))) == 10

    stage_ids = [s.stage_id for s in mini_case.meta.stages]
    localized = i18n.localize_meta(mini_case.meta, language)
    for t, sid, stage in zip(tasks, stage_ids, localized.stages):
        assert t.tier == "T1" and t.max_turns == 4
        assert t.language == language
        assert [s.stage_id for s in t.stages] == [sid]
        assert set(t.data.blocks) == {sid}
        assert t.truths and all(tr.stage_id == sid for tr in t.truths)
        assert t.task_id == f"adb_c13-T1-{sid}-s1-clean{suffix}"
        assert t.context == localized.context
        assert t.stages[0].label in t.goal
        assert t.stages[0].label == stage.label

    # decision_points kept only where branch_evidence overlaps the stage's methods
    by_stage = {t.stages[0].stage_id: t for t in tasks}
    assert [dp.point_id for dp in by_stage["N_MannWhitney"].decision_points] == ["normality_gate"]
    assert by_stage["N_Correlation"].decision_points == ()


def test_build_all(mini_case):
    """The default build equals an explicitly requested English build."""
    explicit = builder.build_all({"adb_c13": mini_case}, seeds=(1,), languages=("en",))
    default = builder.build_all({"adb_c13": mini_case}, seeds=(1,))
    assert len(default) == len(explicit) == 5
    assert default == explicit
    assert {t.language for t in default} == {"en"}
    with pytest.raises(i18n.OverlayError, match="Unsupported language"):
        builder.build_all({"adb_c13": mini_case}, seeds=(1,), languages=("zh",))


# --------------------------------------------------------------------------- 2. dirty variant

def test_dirty_blocks_deterministic_and_bounded(mini_case):
    data = mini_case.generate(1)
    d1 = perturb.dirty_blocks("adb_c13", data.blocks, seed=1)
    d2 = perturb.dirty_blocks("adb_c13", data.blocks, seed=1)
    assert d1 == d2, "same (case_id, seed) must reproduce byte-identical perturbation"
    assert d1 != data.blocks

    # original blocks untouched (deep copy)
    assert all(v is not None for v in data.blocks["N_Summary"]["data"])

    # protected semantic scalar: rename allowed, value must survive non-None
    wil = d1["N_Wilcoxon"]
    med = [v for k, v in wil.items() if "hypothesized" in k.lower().replace("_", "")]
    assert med == [8.0]

    # at least one perturbation actually happened (holes or renames)
    has_hole = any(v is None for v in _iter_leaves(d1))
    renamed = any(set(d1[k]) != set(data.blocks[k]) for k in data.blocks)
    assert has_hole or renamed

    # dirty task built through the builder carries UNCHANGED truths
    for language, suffix in (("en", "-en"),):
        dirty_tasks = builder.build_tasks(mini_case, seeds=(1,), variants=("dirty",),
                                          languages=(language,))
        clean_tasks = builder.build_tasks(mini_case, seeds=(1,), variants=("clean",),
                                          languages=(language,))
        for dt, ct in zip(dirty_tasks, clean_tasks):
            assert dt.variant == "dirty" and dt.task_id.endswith("-dirty" + suffix)
            assert dt.truths == ct.truths
        assert dt.data.blocks != ct.data.blocks

    text = perturb.preview("adb_c13", data.blocks, 1)
    assert "N_Summary" in text and "N_Correlation" in text


# --------------------------------------------------------------------------- 3. fault plan

def test_plan_fault_deterministic(mini_case):
    f1 = fault.plan_fault(mini_case.meta, 1)
    f2 = fault.plan_fault(mini_case.meta, 1)
    assert f1 == f2
    targets = {(t.stage_id, t.method_id) for t in mini_case.meta.fault_targets}
    assert (f1.stage_id, f1.method_id) in targets
    assert fault.plan_fault(dataclasses.replace(mini_case.meta, fault_targets=()), 1) is None


# --------------------------------------------------------------------------- 4. T2/T3/faults

def test_t1_case_yields_no_fault_instances(mini_case):
    tasks = builder.build_tasks(mini_case, with_faults=True)
    assert not any(t.fault for t in tasks)
    assert not any(t.task_id.endswith("-fault") for t in tasks)


def test_t3_case_t2_slicing_and_fault_instance():
    case = _fake_t3_case()
    tasks = builder.build_tasks(case, with_faults=True)
    t3 = [t for t in tasks if t.tier == "T3" and t.fault is None]
    t2 = [t for t in tasks if t.tier == "T2"]
    ft = [t for t in tasks if t.fault is not None]

    assert len(t3) == 1
    assert t3[0].max_turns == 20 and len(t3[0].truths) == 3 and len(t3[0].stages) == 3
    assert t3[0].task_id == "fake_t3-T3-s1-clean-en"

    # one T2 slice per method-bearing phase, in PHASES order
    assert [t.phase for t in t2] == ["measure", "analyze", "control"]
    measure, analyze, control = t2
    assert measure.prior_facts == ""
    assert analyze.prior_facts == "MSA passed (%GRR=8%)"
    assert control.prior_facts == "MSA passed (%GRR=8%); Completed: line comparison"  # label fallback
    assert analyze.goal.startswith("(This task covers the analyze phase only.)")
    assert [tr.stage_id for tr in analyze.truths] == ["S_A"]
    assert set(analyze.data.blocks) == {"S_A"}
    assert all(t.max_turns == 8 for t in t2)
    assert analyze.task_id == "fake_t3-T2-analyze-s1-clean-en"

    # fault instance: T3-clean twin with "-fault" suffix, fault-stage truths RETAINED
    assert len(ft) == 1
    assert ft[0].task_id == "fake_t3-T3-s1-clean-en-fault"
    assert ft[0].tier == "T3"
    assert ft[0].fault == FaultPlan(stage_id="S_A", method_id="anova.oneway")
    assert any(tr.stage_id == "S_A" for tr in ft[0].truths)


# --------------------------------------------------------------------------- 5. steward

def test_steward_routing_denial_exhaustion(mini_case):
    task = _full_task(mini_case, fault_plan=FaultPlan(
        stage_id="N_Correlation", method_id="basic.correlation"))
    st = DataSteward(task)

    # topic routing
    r1 = st.request("Please provide the two suppliers data")
    assert r1.kind == "data" and r1.stage_id == "N_MannWhitney"
    assert r1.message.startswith("[Thickness from the two chemistry suppliers]\n")
    assert "group1" in r1.message and "Supplier A" in r1.message

    # continuation -> earliest unreleased in declaration order
    r2 = st.request("next batch")
    assert r2.kind == "data" and r2.stage_id == "N_Summary"

    # neither topic nor continuation -> unavailable, listing remaining labels
    r3 = st.request("Please show the financial statements")
    assert r3.kind == "unavailable" and r3.stage_id is None
    assert "Thickness from the three plating lines" in r3.message and "That data is unavailable" in r3.message

    # fault stage -> denied and consumed
    r4 = st.request("Please provide bath temperature paired readings")
    assert r4.kind == "denied" and r4.stage_id == "N_Correlation"
    assert r4.message == task.fault.denial_message
    assert "N_Correlation" not in st.remaining()

    r5 = st.request("continue")
    r6 = st.request("what comes next")
    assert {r5.stage_id, r6.stage_id} == {"N_KruskalWallis", "N_Wilcoxon"}
    assert st.remaining() == []

    r7 = st.request("next batch")
    assert r7.kind == "exhausted"

    log = st.audit_log()
    assert [e["kind"] for e in log] == ["data", "data", "unavailable", "denied",
                                        "data", "data", "exhausted"]
    assert [e["turn"] for e in log] == list(range(1, 8))
    assert log[0]["request_text"] == "Please provide the two suppliers data"
    assert log[3]["stage_id"] == "N_Correlation"


# --------------------------------------------------------------------------- 6. runner smoke

class _ScriptedAdapter:
    system_id = "fake-scripted"

    def __init__(self):
        self.received = []
        self.finalized = False

    def start(self, task):
        self.initial = runner.initial_prompt(task)
        return "Please provide baseline data"

    def send(self, message):
        self.received.append(message)
        return "next batch"

    def finalize(self):
        self.finalized = True
        return RunResult(trace=Trace(system_id=self.system_id, task_id="adb_c13-full"),
                         report="Final report")


class _CluelessAdapter:
    system_id = "fake-clueless"

    def __init__(self):
        self.received = []

    def start(self, task):
        return "What is the meaning of the universe"

    def send(self, message):
        self.received.append(message)
        return "What is the meaning of the universe"

    def finalize(self):
        return RunResult(trace=Trace(system_id=self.system_id, task_id="t"), report="")


def test_run_task_smoke(mini_case):
    task = _full_task(mini_case)
    adapter = _ScriptedAdapter()
    result = runner.run_task(adapter, task)
    assert isinstance(result, RunResult) and adapter.finalized
    assert result.report == "Final report"
    # 5 data batches then the closing instruction
    assert len(adapter.received) == 6
    assert adapter.received[0].startswith("[Baseline thickness record]")
    assert adapter.received[-1] == runner.CLOSING_INSTRUCTION
    # initial prompt carries context + goal + on-demand data protocol
    assert mini_case.meta.context.strip() in adapter.initial
    assert "Task goal" in adapter.initial and "on demand" in adapter.initial


def test_run_task_breaks_after_two_unavailable(mini_case):
    task = _full_task(mini_case)
    adapter = _CluelessAdapter()
    result = runner.run_task(adapter, task)
    assert isinstance(result, RunResult)
    assert len(adapter.received) == 1  # one unavailable notice, then break
    assert "That data is unavailable" in adapter.received[0]
