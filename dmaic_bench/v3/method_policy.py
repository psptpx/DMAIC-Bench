"""Method-selection-under-ambiguity: the v3 core that v2 skipped by feeding `admissible_methods`.

A MethodDecision names, for one analysis decision in a case, which methods are CORRECT / ACCEPTABLE
/ MISUSE *given this data* — with an optional guard so the correct choice can depend on the data
shape (skewed → nonnormal capability; equal-n → P-chart). The agent is NOT told the method; it
declares what it used, and Channel-2 scoring grades whether it selected validly.

This is what makes "picking the right method from ~49 candidates" a graded skill (design doc §3.1,
method-selection-gap-analysis.md). MISUSE is a multiplicative gate in TGPS: a right-looking number
via a statistically invalid method is a trap, not a success.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from dmaic_bench.core.graph import evaluate


@dataclass(frozen=True)
class MethodDecision:
    decision_id: str
    phase: str
    rule: str                       # the methodology rule (policy_doc line) that governs the choice
    correct: tuple                  # method_ids that are the right choice for this data
    acceptable: tuple = ()          # valid-but-suboptimal alternatives (full credit, not misuse)
    misuse: tuple = ()              # statistically invalid choices for this data (gate fires)
    applies_when: str = ""          # guard over observed results; "" = always applies
    source: str = ""                # textbook citation
    stage: str = ""                 # graph node this decision is made at (a node may host several)


def _canon(m: str) -> str:
    """Normalize a declared method id to a taxonomy family.method form (drop solver./version)."""
    m = (m or "").strip().lower().replace("solver.", "").replace("-", "_")
    m = m.split(".v")[0]
    # map dotted spec keys (gage.rr_crossed) and family shorthands to family.method
    return m


def _match(declared: str, pool) -> bool:
    d = _canon(declared)
    for m in pool:
        c = _canon(m)
        if d == c or d.endswith(c) or c.endswith(d) or d.replace(".", "_") == c.replace(".", "_"):
            return True
    return False


def score_method_selection(declared: dict, decisions, observed: dict | None = None) -> dict:
    """`declared`: {decision_id or stage_key -> declared method_id}. Returns MS-sel + misuse.

    A decision is scored only if its `applies_when` guard holds over `observed` (so data-conditioned
    decisions are graded on the branch the data actually took). Silence on an applicable decision
    counts against selection (you must make the call), but is not misuse.
    """
    observed = observed or {}

    def _pool_for(d):
        """All methods the agent declared that could answer this decision (by stage or decision_id).
        Values may be a single id or a list."""
        pool = []
        for key in (d.decision_id, d.stage, d.phase):
            v = declared.get(key)
            if isinstance(v, (list, tuple)):
                pool += list(v)
            elif v:
                pool.append(v)
        return pool

    per, hits, misused, applicable = {}, 0, 0, 0
    for d in decisions:
        if d.applies_when and not evaluate(d.applies_when, observed):
            continue
        applicable += 1
        pool = _pool_for(d)
        ok = any(_match(c, d.correct) or _match(c, d.acceptable) for c in pool)
        mis = any(_match(c, d.misuse) for c in pool)
        hits += int(ok)
        misused += int(mis)
        per[d.decision_id] = {"chosen": pool, "correct": list(d.correct),
                              "ok": ok, "misuse": mis, "rule": d.rule}
    return {"ms_sel": (hits / applicable) if applicable else 1.0,
            "misuse_rate": (misused / applicable) if applicable else 0.0,
            "applicable": applicable, "correct": hits, "misused": misused, "per_decision": per}


# --------------------------------------------------------------------------- adb_c15 policy

# The real method-selection decisions a Black Belt makes on adb_c15 — the ones the v2 briefing
# handed over for free. Correct choices reflect the data: individuals (not subgroups) → I-MR;
# continuous crossed gage study → crossed R&R (NOT attribute agreement); ~normal (AD p=0.42) →
# normal capability (nonnormal is over-engineering=acceptable, binomial/poisson=misuse-wrong-type);
# 3 continuous groups → one-way ANOVA (two-sample t is misuse — can't handle 3 groups).
ADB_C15_DECISIONS = (
    MethodDecision(
        decision_id="stability_chart", phase="measure", stage="M_Baseline",
        rule="individual run-order measurements (no rational subgroups) → I-MR, not Xbar charts",
        correct=("control_chart.imr",),
        misuse=("control_chart.xbar_r", "control_chart.xbar_s"),
        source="Montgomery ISQC 6e §6.4"),
    MethodDecision(
        decision_id="capability_method", phase="measure", stage="M_Baseline",
        rule="choose the capability method by the fitted distribution; AD normality holds → normal",
        correct=("capability.normal",),
        acceptable=("capability.nonnormal",),          # over-engineering, still valid
        misuse=("capability.binomial", "capability.poisson"),   # wrong data type (continuous)
        source="AIAG SPC-2"),
    MethodDecision(
        decision_id="msa_method", phase="measure", stage="M_GRR",
        rule="continuous crossed operator×part study → crossed Gage R&R, NOT attribute agreement",
        correct=("msa.gage_rr_crossed",),
        misuse=("msa.attribute_agreement",),
        source="AIAG MSA-4"),
    MethodDecision(
        decision_id="anova_method", phase="analyze", stage="A_ANOVA",
        rule="3-level factor on a continuous response → one-way ANOVA (two-sample t handles only 2)",
        correct=("anova.oneway",),
        acceptable=("anova.equal_variances", "nonparametric.kruskal_wallis"),
        misuse=("basic.two_sample_t", "basic.paired_t"),
        source="Montgomery DAOE 6e §3"),
    MethodDecision(
        decision_id="doe_screen_method", phase="improve", stage="I_Factorial",
        rule="2-factor experiment with center points → factorial analysis with curvature test",
        correct=("doe.factorial_analysis",),
        acceptable=("regression.ols",),
        source="Montgomery DAOE 6e §6"),
    MethodDecision(
        decision_id="rsm_method", phase="improve", stage="I_CCD",
        rule="curvature significant → central-composite response-surface analysis",
        correct=("doe.rsm_analysis",),
        acceptable=("doe.rsm_canonical",),
        applies_when="doe.curvature_pValue < 0.05",
        source="Montgomery DAOE 6e §11"),
)

# --------------------------------------------------------------------------- injection_molding (D2 trap)
# The capability-method choice is DATA-CONDITIONED and a genuine trap: on the skewed seed the data
# still has a mean/std you *can* plug into the normal formula (it returns a number), so a careless
# agent runs normal capability — MISUSE. Only an agent that runs a normality test first and sees
# p<0.05 correctly switches to non-normal capability. This is where method selection DISCRIMINATES.
INJECTION_DECISIONS = (
    MethodDecision(
        decision_id="stability_chart", phase="measure", stage="M_stability",
        rule="individual run-order data → I-MR",
        correct=("control_chart.imr",),
        misuse=("control_chart.xbar_r", "control_chart.xbar_s"),
        source="Montgomery ISQC 6e §6.4"),
    MethodDecision(
        decision_id="capability_when_normal", phase="analyze", stage="A_cap_normal",
        rule="normality holds (AD p≥0.05) → normal capability",
        correct=("capability.normal",),
        misuse=("capability.nonnormal", "capability.binomial", "capability.poisson"),
        applies_when="normality.pValue >= 0.05",
        source="AIAG SPC-2"),
    MethodDecision(
        decision_id="capability_when_skewed", phase="analyze", stage="A_cap_nonnormal",
        rule="strong non-normality (AD p<0.05) → non-normal capability; normal formula is MISUSE",
        correct=("capability.nonnormal",),
        misuse=("capability.normal",),
        applies_when="normality.pValue < 0.05",
        source="AIAG SPC-2 / Montgomery ISQC 6e §8.5"),
)

# --------------------------------------------------------------------------- capability_trap (D2)
CAP_TRAP_DECISIONS = (
    MethodDecision(
        decision_id="stability_chart", phase="measure", stage="M_stability",
        rule="individual data → I-MR",
        correct=("control_chart.imr",),
        misuse=("control_chart.xbar_r", "control_chart.xbar_s"),
        source="Montgomery ISQC 6e §6.4"),
    MethodDecision(
        decision_id="cap_on_skew", phase="analyze", stage="A_capability",
        rule="AD normality rejected (p<0.05) → NON-normal capability; the normal formula is MISUSE",
        correct=("capability.nonnormal",),
        misuse=("capability.normal",),
        applies_when="normality.pValue < 0.05",
        source="Montgomery ISQC 6e §8.5"),
    MethodDecision(
        decision_id="cap_on_normal", phase="analyze", stage="A_capability",
        rule="normality holds (p≥0.05) → normal capability",
        correct=("capability.normal",),
        acceptable=("capability.nonnormal",),
        applies_when="normality.pValue >= 0.05",
        source="AIAG SPC-2"),
)

# --------------------------------------------------------------------------- smart_mirror (new domain)
SMART_MIRROR_DECISIONS = (
    MethodDecision(
        decision_id="msa_method", phase="measure", stage="M_msa",
        rule="continuous luminance meter, crossed operator×unit → crossed Gage R&R (not attribute)",
        correct=("msa.gage_rr_crossed",),
        misuse=("msa.attribute_agreement",),
        source="AIAG MSA-4"),
    MethodDecision(
        decision_id="stability_chart", phase="measure", stage="M_stability",
        rule="individual per-unit luminance → I-MR",
        correct=("control_chart.imr",),
        misuse=("control_chart.xbar_r", "control_chart.xbar_s"),
        source="Montgomery ISQC 6e §6.4"),
    MethodDecision(
        decision_id="cap_on_skew", phase="analyze", stage="A_cap_nonnormal",
        rule="backlight-decay skew rejects normality (p<0.05) → non-normal capability; normal is MISUSE",
        correct=("capability.nonnormal",),
        misuse=("capability.normal",),
        applies_when="normality.pValue < 0.05",
        source="Montgomery ISQC 6e §8.5"),
    MethodDecision(
        decision_id="cap_on_normal", phase="analyze", stage="A_cap_normal",
        rule="normality holds (p≥0.05) → normal capability",
        correct=("capability.normal",),
        acceptable=("capability.nonnormal",),
        applies_when="normality.pValue >= 0.05",
        source="AIAG SPC-2"),
)

#: Keyed by case_id. The three v2 projects were renamed onto opaque adb_cNN ids when they became
#: publishable Harbor tasks; the working names are kept as aliases so an in-tree caller that
#: still uses them (demo.py, sonnet_harness.py) does not silently get an empty policy.
POLICY = {"adb_c15": ADB_C15_DECISIONS,
          "adb_c25": INJECTION_DECISIONS, "injection_molding": INJECTION_DECISIONS,
          "adb_c29": CAP_TRAP_DECISIONS, "capability_trap": CAP_TRAP_DECISIONS,
          "adb_c28": SMART_MIRROR_DECISIONS, "smart_mirror": SMART_MIRROR_DECISIONS}
