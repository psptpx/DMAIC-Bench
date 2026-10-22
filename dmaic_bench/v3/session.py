"""MethodBlindSession — the v3 contestant view: the agent is NOT told which method to use.

The briefing gives the business context, the DMAIC policy_doc (the methodology rules that ARE the
grading contract), the raw data on request, and the FULL method vocabulary (~49) as a flat menu —
never a per-node shortlist. The agent must SELECT the method for each decision and DECLARE it, so
Channel-2 (method validity) can grade the selection. This closes the v2 effectiveness hole where
`admissible_methods` handed the answer over (method-selection-gap-analysis.md).
"""
from __future__ import annotations

from dmaic_bench import taxonomy as _tax
from dmaic_bench.v2.blind_session import BlindSession, _flatten_keys


def method_space() -> list:
    """The full flat method menu every contestant sees — same for every case."""
    tax = _tax.load()
    out = []
    for m in sorted(tax.methods):
        fam = m.split(".")[0]
        out.append({"method_id": m, "family": fam})
    return out


_POLICY_DOC = (
    "Six Sigma DMAIC methodology rules (the scoring contract for this project):\n"
    "1. Establish an acceptable measurement system (MSA) before trusting subsequent measurement data.\n"
    "2. Capability analysis is valid only under statistical control (no out-of-control I-MR/control-chart signals); investigate special causes first otherwise.\n"
    "3. Select capability by distribution: approximately normal -> normal capability; significantly nonnormal -> nonnormal (Box-Cox/distribution fitting); nonconforming proportion -> binomial; defect counts -> Poisson. A capability method for the wrong data type is misuse.\n"
    "4. Select control charts by data structure: individual values without rational subgroups -> I-MR; subgroups -> Xbar-R/S; attributes -> P/NP/U/C.\n"
    "5. Select MSA by study type: continuous crossed operator-by-part studies -> crossed Gage R&R; attribute judgments -> attribute agreement (Kappa).\n"
    "6. Group comparisons: two groups -> two-sample/paired t (or nonparametric); three or more -> one-way ANOVA (check equal variance first); nonnormal -> nonparametric (Mann-Whitney/Kruskal-Wallis).\n"
    "7. DOE: screen first (factorial) for significance and curvature; significant curvature -> response-surface (RSM) optimization.\n"
    "Choose the method yourself from each node's data and declare it in the `method` field when reporting."
)


class MethodBlindSession(BlindSession):
    def __init__(self, task, fault: bool = False):
        super().__init__(task, fault=fault)
        self.declared_methods: dict = {}     # node_key -> declared method_id

    def briefing(self) -> dict:
        b = super().briefing()
        # strip the per-node method shortlist — the whole point of v3
        for n in b["nodes"]:
            n.pop("admissible_methods", None)
        b["policy_doc"] = _POLICY_DOC
        b["method_space"] = method_space()      # the full menu, identical for every case
        b["instructions"] = (
            "The environment does not tell you which method to use. Select the appropriate method "
            "from method_space using each node's data and policy_doc. Include the selected method id "
            "in the `method` field of every report. A wrong method is misuse even if the numbers "
            "are correct. Disclose missing data; do not fabricate results.")
        return b

    def report(self, node: str, results: dict, method: str | None = None) -> None:
        if method:
            self.declared_methods[node] = method
        super().report(node, results)

    def record(self):
        from dmaic_bench.core.graph import walk
        rec = super().record()
        rec.declared_methods = dict(self.declared_methods)
        # An agent's route through a guard-based graph is IMPLIED by the values it computed (the
        # edge guards read them). A method-blind agent often reuses already-released data for
        # several nodes and skips explicit visits to pure-router nodes, so the data-release log
        # under-counts the route. Reconstruct the effective trajectory from walk(graph, accepted)
        # and derive branch choices from it — this credits the routing the agent's own conclusions
        # entail (self-consistent), scored for correctness against the oracle walk in score_run.
        if rec.accepted:
            route = walk(self.task.graph, rec.accepted)
            if len(route) > len(rec.trajectory):
                rec.trajectory = route
                rec.choices = {k: route[i + 1] for i, k in enumerate(route[:-1])
                               if self.task.graph.is_branch_point(k)}
        return rec
