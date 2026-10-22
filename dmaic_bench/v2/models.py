"""v2 task-model contract: V2Case (a data-conditioned DMAIC project) and ProjectTask (a runnable
(case, seed) instance). Every v2 case module exposes a module-level `CASE: V2Case`; the registry
discovers them and the builder resolves them into ProjectTasks.

A ProjectTask freezes the generated data blocks and the oracle-computed results, so the
data-conditioned correct trajectory is `walk(graph, oracle_results)`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

from dmaic_bench.core.graph import DecisionGraph, walk


@dataclass(frozen=True)
class V2Case:
    """A data-conditioned DMAIC project definition.

    generate(seed) -> (blocks, oracle_results): blocks are the staged data the steward hands out
    (keyed by DMAIC phase / stage), oracle_results are the truth statistics computed FROM those
    blocks by the real verifiers. `seeds` are the canonical seeds proven to force distinct routes;
    `shapes` maps seed -> a human label of the statistical shape.
    """
    #: OPAQUE, per cases/_template/case.yaml: an ``adb_cNN`` code that names no company, place,
    #: industry or statistical method. The descriptive name stays on the Python module; the
    #: published identifier may not carry it, because the task id reaches the agent in
    #: instruction.md and comes back in trace.json.
    case_id: str
    title: str
    #: One of the four COARSE public values: process_industry | electronics |
    #: discrete_manufacturing | services. A fine-grained industry is itself an identifier.
    industry: str
    graph: DecisionGraph
    gate_policy: tuple
    generate: Callable[[int], tuple]
    #: continuous | attribute_proportion | attribute_count_rate | mixed. Read by the MS-misuse
    #: term, which asks whether an attempted method's data type conflicts with this task's y.
    y_type: str = "continuous"
    provenance: str = "SIMULATED"
    seeds: tuple = (0, 1, 2, 3)
    shapes: dict = field(default_factory=dict)
    node_data: dict = field(default_factory=dict)   # node_key -> blocks key the steward serves
    fault_targets: tuple = ()          # (stage_key, method_id, denial_message) honesty probes
    budget: dict = field(default_factory=lambda: {"max_turns": 24})
    # "route" = data-conditioned decision-graph case (≥2 distinct routes expected); "method" = v3
    # method-selection trap (linear route on purpose — the graded variable is the method, not the path)
    discriminator: str = "route"
    #: ``fork_node -> methods`` that count as neither a wrong turn nor evidence of the correct
    #: branch at that fork: a statistically defensible alternative the reference route does not
    #: take. Declared by the case author with a citation; the 2026-09-18 expert review added the
    #: first one (Welch ANOVA where variances differ, adb_c37). Reported, never inferred.
    accepted_methods: dict = field(default_factory=dict)

    # ----------------------------------------------------------------- Harbor packaging
    # Everything below is consumed by ``dmaic_harbor.v2_tasks`` when this project is packaged as
    # a Harbor task. None of it changes ``walk``/``oracle_route``; a case that is never packaged
    # can leave it empty.

    #: The brief the agent reads. MUST NOT name a statistical method — choosing the method is
    #: the measured capability, and ``build.assert_no_method_leak`` fails the build on a hit.
    context: str = ""
    goal: str = ""

    #: ``block_key -> {"label", "topics", "phase"}`` for the steward. A Harbor stage is a BATCH
    #: OF DATA, not a graph node: several nodes legitimately analyse the same batch, and the
    #: steward routes free-text requests onto batches. Labels and topics are agent-visible, so
    #: they name the data, never the analysis to run on it.
    blocks_meta: dict = field(default_factory=dict)

    #: ``dotted_result_field -> tuple[dict]`` — how a contestant's OWN trace reveals a field the
    #: guards read. Each entry is ``{"method_id", "output", "scale"}``: the trace output
    #: ``output`` of ``method_id``, multiplied by ``scale``, is that contestant's observation of
    #: this field. Candidates are tried in order, so ``cap.ppk`` can name the normal and the
    #: non-normal producer and resolve to whichever the contestant actually ran. This is what
    #: makes Self-Consistency computable: it re-walks the graph on the agent's own numbers.
    field_map: dict = field(default_factory=dict)

    #: ``tuple[(dotted_field, method_id, output_name, tol)]`` — the numeric truths to publish for
    #: this project. Deliberately explicit rather than derived from ``produces``: a field is only
    #: a fair truth when the quantity the case computed and the quantity a competent contestant
    #: computes are the SAME statistic. Measured counter-example kept out of this tuple: the
    #: non-normal Ppk, where this corpus uses the ISO percentile index and the reference solution
    #: fits a Weibull — 1.058 against 0.406 on the same data. Pinning one would score the
    #: convention, not the competence.
    truth_fields: tuple = ()

    #: ``node_key -> tuple[{"when": guard, "methods": (...)}]`` — a DATA-CONDITIONED method
    #: choice at one node, for a case whose route is constant on purpose and whose graded
    #: variable is the method (``discriminator == "method"``). First matching clause wins; a
    #: clause with no ``when`` is the default. Absent → ``node.methods``.
    method_policy: dict = field(default_factory=dict)

    #: ``dotted_field -> {"node", "key", "kind"}`` -- a STRUCTURAL observation of a released
    #: batch that no statistical method reports. "Are the subgroup sizes constant?" decides which
    #: attribute chart is admissible; an analyst answers it by looking at the batch, and nothing
    #: in the taxonomy emits it. Declaring it here lets the reference solution make the
    #: observation at run time instead of falling through to the default branch on every seed.
    batch_facts: dict = field(default_factory=dict)

    def methods_at(self, node_key: str, results: dict) -> tuple:
        """The admissible methods at ``node_key`` GIVEN ``results`` (see :attr:`method_policy`)."""
        clauses = self.method_policy.get(node_key)
        if not clauses:
            node = self.graph.node(node_key)
            return tuple(node.methods) if node is not None else ()
        from dmaic_bench.core.graph import evaluate
        default = None
        for clause in clauses:
            when = clause.get("when")
            if not when:
                default = clause
                continue
            if evaluate(when, results):
                return tuple(clause.get("methods", ()))
        return tuple((default or {}).get("methods", ()))

    def oracle_route(self, seed: int) -> list:
        _, res = self.generate(seed)
        return walk(self.graph, res)


@dataclass(frozen=True)
class ProjectTask:
    """A concrete runnable instance: one (case, seed) with data + oracle frozen."""
    task_id: str
    case_id: str
    seed: int
    shape: str
    graph: DecisionGraph
    gate_policy: tuple
    blocks: dict
    oracle_results: dict
    node_data: dict = field(default_factory=dict)
    fault_targets: tuple = ()
    budget: dict = field(default_factory=lambda: {"max_turns": 24})

    def oracle_route(self) -> list:
        return walk(self.graph, self.oracle_results)


def build_project_task(case: V2Case, seed: int, variant: str = "clean") -> ProjectTask:
    blocks, oracle_results = case.generate(seed)
    shape = case.shapes.get(seed, oracle_results.get("_shape", f"seed{seed}"))
    return ProjectTask(
        task_id=f"{case.case_id}-P-s{seed}-{variant}",
        case_id=case.case_id, seed=seed, shape=shape,
        graph=case.graph, gate_policy=case.gate_policy,
        blocks=blocks, oracle_results=oracle_results,
        node_data=case.node_data, fault_targets=case.fault_targets, budget=case.budget,
    )
