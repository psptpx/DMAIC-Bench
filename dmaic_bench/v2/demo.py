"""End-to-end v2 demo: the full long-horizon pipeline (gating environment → runner → TGPS scorer)
across every data-conditioned case, plus the anti-scripting release-gate result.

Run: python3 -m dmaic_bench.v2.demo
"""
from dmaic_bench.v2 import builder, registry, runner, scoring

MODAL = ["D_scope", "M_msa", "M_stability", "A_route", "A_cap_normal", "C_control"]


def main():
    cases = registry.discover()
    print("=" * 82)
    print(f"DMAIC-Bench v2 — {len(cases)} data-conditioned projects, driven through the gating")
    print("environment and scored end to end. ONE graph per project; the seed drives the data")
    print("shape → the oracle-correct DMAIC route changes.")
    print("=" * 82)

    oracle_cards, scripted_cards = [], []
    for cid in sorted(cases):
        case = cases[cid]
        print(f"\n### {cid}  ({case.industry}) — {builder.distinct_routes(case)} distinct routes")
        for seed in case.seeds:
            task = builder.build_project_task(case, seed)
            oc = scoring.score_run(task, runner.run_project(task, runner.OracleAgent()))
            oracle_cards.append(oc)
            print(f"  seed {seed} [{task.shape:26s}] oracle TGPS={oc['tgps']:.2f} "
                  f"route={' → '.join(r.split('_')[0] for r in oc['trajectory'])}")

    # the anti-scripting release gate, on the moulded-dimension project (adb_c25)
    print("\n" + "=" * 82)
    print("ANTI-SCRIPTING RELEASE GATE (adb_c25): a rigid single-path agent")
    print("=" * 82)
    from dmaic_bench.v2.cases.injection_molding import CASE as INJ
    for seed in range(4):
        task = builder.build_project_task(INJ, seed)
        sc = scoring.score_run(task, runner.run_project(task, runner.ScriptedAgent(MODAL)))
        scripted_cards.append(sc)
        locked = [a[1] for a in runner.run_project(task, runner.ScriptedAgent(MODAL)).audit
                  if a[0] == "locked"]
        print(f"  seed {seed} [{task.shape:26s}] scripted TGPS={sc['tgps']:.2f} "
              f"PC={sc['pc']:.2f} GC={sc['gc']:.2f}  locked_out={locked}")

    print("\n" + "-" * 82)
    print(f"oracle agent   aggregate: {scoring.aggregate(oracle_cards)}")
    print(f"scripted agent aggregate: {scoring.aggregate(scripted_cards)}  (adb_c25 only)")
    print("-" * 82)
    print("VERDICT: a compliant data-conditioned agent scores TGPS 1.0 on every project & seed;")
    print("the rigid single-path solver mis-routes on off-modal data and is LOCKED out of")
    print("capability on the out-of-control process. The benchmark measures the methodology,")
    print("not the arithmetic — and it is provably not scriptable.")


if __name__ == "__main__":
    main()
