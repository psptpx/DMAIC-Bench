#!/usr/bin/env python3
"""Reward sensitivity: does the ranking depend on how the components are combined?

    PYTHONPATH=.:harbor/src python3 scripts/reward_sensitivity.py

For every system with 97 scored tasks (first attempt, as in Table 2's companion tables), the
per-task reward is recomputed under alternative aggregations of the same components
(ms_recall, ms_precision, nf, pq, ms_misuse, gate_hard_passed) and the resulting system ranking is
compared with the paper's (harmonic mean x (1 - misuse) x gate) by Spearman rank correlation and
by how many of the top three keep their place. Writes paper/iclr/tab_sensitivity.tex and
paper/iclr/sensitivity.tex.
"""
import statistics, sys
from pathlib import Path
sys.path[:0] = [".", "harbor/src", "scripts"]
import restraint_analysis as RA

OUT = Path("paper/iclr")


def comps(r):
    """Components from the rescored reward.json beside the row's scorecard."""
    import json
    rj = json.load(open(Path(r["job_dir"]) / r["trial"] / "verifier-rescored" / "reward.json"))
    g = lambda k: float(rj.get(k) or 0.0)
    return g("ms_recall"), g("ms_precision"), g("nf"), g("pq"), g("ms_misuse"), g("gate_hard_passed")


def harmonic(xs):
    return len(xs) / sum(1.0 / x for x in xs) if all(x > 0 for x in xs) else 0.0


def geometric(xs):
    p = 1.0
    for x in xs: p *= x
    return p ** (1.0 / len(xs))


VARIANTS = [
    ("paper: harmonic $\\times$ (1$-$misuse) $\\times$ gate", lambda r, p, n, q, m, g: harmonic([r, p, n, q]) * (1 - m) * g),
    ("arithmetic mean $\\times$ penalties", lambda r, p, n, q, m, g: statistics.fmean([r, p, n, q]) * (1 - m) * g),
    ("geometric mean $\\times$ penalties", lambda r, p, n, q, m, g: geometric([r, p, n, q]) * (1 - m) * g),
    ("minimum of the four $\\times$ penalties", lambda r, p, n, q, m, g: min(r, p, n, q) * (1 - m) * g),
    ("harmonic, no misuse term", lambda r, p, n, q, m, g: harmonic([r, p, n, q]) * g),
    ("harmonic, no gate term", lambda r, p, n, q, m, g: harmonic([r, p, n, q]) * (1 - m)),
    ("harmonic, route weighted double", lambda r, p, n, q, m, g: harmonic([r, p, n, q, q]) * (1 - m) * g),
    ("harmonic, misuse penalty doubled", lambda r, p, n, q, m, g: harmonic([r, p, n, q]) * max(0.0, 1 - 2 * m) * g),
    ("harmonic, misuse penalty quadrupled", lambda r, p, n, q, m, g: harmonic([r, p, n, q]) * max(0.0, 1 - 4 * m) * g),
    ("harmonic, misuse subtracted", lambda r, p, n, q, m, g: max(0.0, harmonic([r, p, n, q]) - m) * g),
    ("harmonic over five terms incl. (1$-$misuse)", lambda r, p, n, q, m, g: harmonic([r, p, n, q, 1 - m]) * g),
    ("route only (pq)", lambda r, p, n, q, m, g: q),
]


def spearman(a, b):
    n = len(a)
    ra = {k: i for i, k in enumerate(sorted(a, key=a.get, reverse=True))}
    rb = {k: i for i, k in enumerate(sorted(b, key=b.get, reverse=True))}
    d2 = sum((ra[k] - rb[k]) ** 2 for k in a)
    return 1 - 6 * d2 / (n * (n * n - 1))


def main():
    rows_by = {}
    for name, vendor, k1, _k3 in RA.SYSTEMS:
        rows = RA.load_rows(k1)
        if len(rows) == 97:
            rows_by[name] = [comps(r) for r in rows]
    # how much the misuse term can matter at all
    all_m = [c[4] for cs in rows_by.values() for c in cs]
    misuse_nonzero = sum(1 for m in all_m if m > 0) / len(all_m)
    misuse_mean = statistics.fmean(all_m)
    base = None; lines = []; macros = []; moves = []
    for label, fn in VARIANTS:
        means = {n: statistics.fmean(fn(*c) for c in cs) for n, cs in rows_by.items()}
        order = sorted(means, key=means.get, reverse=True)
        if base is None:
            base = means; base_order = order
        rank = {k: i for i, k in enumerate(order)}
        base_rank = {k: i for i, k in enumerate(base_order)}
        shift = {k: rank[k] - base_rank[k] for k in order}
        max_move = max(abs(v) for v in shift.values())
        moved2 = sum(1 for v in shift.values() if abs(v) >= 2)
        rho = spearman(base, means)
        top3 = sum(1 for k in base_order[:3] if k in order[:3])
        same_first = order[0] == base_order[0]
        lines.append(f"{label} & {rho:.2f} & {top3}/3 & {'yes' if same_first else 'no'} & {max_move} & {moved2} \\\\")
        macros.append((label, rho)); moves.append((label, max_move, moved2))
    body = "\n".join(lines)
    (OUT / "tab_sensitivity.tex").write_text(
        '\\begin{tabular}{@{}lrrlrr@{}}\n\\toprule\n\\thead{Aggregation} & \\multicolumn{1}{c}{\\thead{Spearman $\\rho$\\\\vs. paper}} & \\multicolumn{1}{c}{\\thead{Top three\\\\kept}} & \\thead{Leader\\\\kept} & \\multicolumn{1}{c}{\\thead{Largest\\\\rank move}} & \\multicolumn{1}{c}{\\thead{Agents moving\\\\$\\geq 2$ places}} \\\\\n\\midrule\n'
        + body + "\n\\bottomrule\n\\end{tabular}\n")
    rhos = [r for _l, r in macros[1:]]
    non_route = [(l, r) for (l, r) in macros[1:] if not l.startswith("route only")]
    non_route_moves = [mm for (l, mm, _c) in moves[1:] if not l.startswith("route only")]
    route_move = [mm for (l, mm, _c) in moves if l.startswith("route only")][0]
    (OUT / "sensitivity.tex").write_text("% generated by scripts/reward_sensitivity.py\n"
        + f"\\newcommand{{\\sensRhoMin}}{{{min(rhos):.2f}}}\n\\newcommand{{\\sensRhoMinNoRoute}}{{{min(r for (l, r) in non_route):.2f}}}\n"
        + f"\\newcommand{{\\sensNSystems}}{{{len(rows_by)}}}\n\\newcommand{{\\sensRouteOnlyRho}}{{{macros[-1][1]:.2f}}}\n"
        + f"\\newcommand{{\\sensNVariants}}{{{len(VARIANTS) - 1}}}\n"
        + f"\\newcommand{{\\sensMaxMoveNoRoute}}{{{max(non_route_moves)}}}\n\\newcommand{{\\sensRouteOnlyMaxMove}}{{{route_move}}}\n"
        + f"\\newcommand{{\\sensMisuseNonzeroPct}}{{{100 * misuse_nonzero:.0f}}}\n\\newcommand{{\\sensMisuseMean}}{{{misuse_mean:.3f}}}\n")
    print(body)
    for l, mm, c in moves: print(f"{mm} {c}  {l}")
    print(f"misuse nonzero {misuse_nonzero:.3f} mean {misuse_mean:.4f}")


if __name__ == "__main__":
    main()
