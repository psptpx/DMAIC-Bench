"""injection_molding — the canonical data-conditioned DMAIC project (v2).

ONE decision graph; `seed % 4` drives the statistical shape so four seeds walk four distinct
oracle-correct routes (see poc_project for the generator + graph). Wrapped here as a V2Case so the
registry/builder/steward/scorer stack treats it uniformly.
"""
from dmaic_bench.v2 import poc_project as _p
from dmaic_bench.v2.cases import _fixtures as _f
from dmaic_bench.v2.models import V2Case

CASE = V2Case(
    # OPAQUE published id (cases/_template/case.yaml): the module keeps the descriptive name,
    # the published identifier may not carry it -- the task id is read by the agent in
    # instruction.md and written back in trace.json.
    case_id="adb_c25",
    title="Critical fitting dimension: bringing a moulded part back inside its range",
    industry="discrete_manufacturing",
    y_type="continuous",
    graph=_p.PROJECT_GRAPH,
    gate_policy=_p.GATE_POLICY,
    generate=_p.generate,
    # Seed 4 is the gauge-REJECTION seed: it exercises the ``M_msa`` fork's other edge, which no
    # seed reached while the rejection branch was a self-loop the walk could not record.
    seeds=(0, 1, 2, 3, 4),
    shapes={s: _p.SHAPES[_p._shape_for(s)] for s in (0, 1, 2, 3, 4)},
    node_data=_p.NODE_DATA,
    # The denial TEXT is not taken from here when the project is packaged for Harbor: see
    # dmaic_harbor.v2_tasks.build_task, which substitutes the language-appropriate generic
    # message. This string named the withheld analysis, and steward.json is agent-readable.
    fault_targets=(("M_msa", "msa.gage_rr_crossed",
                    "the Gage R&R raw data for this batch was checked and is genuinely not on file"),),
    budget={"max_turns": 24},
    context=(
        "We are the improvement team at a moulding plant. Complaints from the customer's "
        "assembly line about one critical fitting dimension have risen this quarter; the "
        "internally accepted range for it is 12 to 28 mm. The line has kept a piece-by-piece "
        "record in production order, and the archive also holds the study in which the same "
        "pieces were read several times over by several inspectors. Nobody has yet gone "
        "through either of them properly."),
    goal=(
        "Work through the batches the data steward can release and say where this project "
        "stands: whether the recorded readings can be relied on at all, how the line has "
        "behaved over the run, where the dimension sits against its accepted range today, and "
        "what should be done about it next. Every number in your report must come from a "
        "computation you ran on this task; where the data does not support a judgement, say "
        "so instead of making one."),
    blocks_meta={
        "define": {"label": "Project charter and accepted range", "phase": "define",
                   "topics": ("charter", "accepted range", "improvement target")},
        "msa": {"label": "Repeat readings of the same pieces", "phase": "measure",
                "topics": ("repeat readings", "inspector study")},
        "process_run": {"label": "Piece-by-piece production record", "phase": "measure",
                        "topics": ("piece record", "production order")},
    },
    field_map={
        "msa.pctSV": _f.SRC_GRR_PCT, "msa.ndc": _f.SRC_GRR_NDC,
        "imr.outOfControl": _f.SRC_IMR_OOC, "normality.pValue": _f.SRC_NORMALITY,
        "cap.ppk": _f.SRC_PPK, "cap.pp": _f.SRC_PP,
    },
    truth_fields=(
        _f.TRUTH_GRR_PCT,
        {"field": "imr.outOfControl", "method_id": "control_chart.imr",
         "output": "flaggedCount", "scale": 1.0, "tol": 0.0},
        {"field": "normality.pValue", "method_id": "basic.normality",
         "output": "pValue", "scale": 1.0, "tol": 0.01},
        {"field": "cap.ppk", "method_id": "capability.normal",
         "output": "ppk", "scale": 1.0, "tol": 0.01},
        {"field": "cap.pp", "method_id": "capability.normal",
         "output": "pp", "scale": 1.0, "tol": 0.01},
    ),
)
