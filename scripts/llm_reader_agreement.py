#!/usr/bin/env python3
"""Agreement of LLM readers with the human majority on the 60 study-2 units.

    python3 scripts/llm_reader_agreement.py <model> [<model> ...]   -> paper/iclr/tab_llmreader.tex, llmreader.tex

Each reader answered the experts' protocol on the sealed packets (scripts/llm_reader_pilot.py).
Agreement is against the majority of the three black belts; "acted" means the report asserts a
forbidden conclusion or recommends a forbidden action. Contestant readers are also split into
the units that carry their own reports and the rest. The 60 units were never used to tune any
scoring rule, so this is a held-out comparison.
"""
import json, sys
from pathlib import Path

ROOT = Path("paper/blind_review_2026-09-19"); OUT = Path("paper/iclr")
units = {u["blind_id"]: u for u in json.load(open(ROOT / "coordinator" / "results_study2.json"))["units"]}
system_of = {u["blind_id"]: u["model"] for u in json.load(open(ROOT / "coordinator" / "manifest_sealed.json"))["units"]}
fleiss = json.load(open(ROOT / "coordinator" / "results_study2.json"))["fleiss_kappa"]
# reader model id -> (display name, contestant system name or None)
READERS = {"gpt-6-astra": ("GPT-6-astra", "GPT-6-astra"), "deepseek-v4-pro": ("DeepSeek-v4-pro", "DeepSeek-v4-pro"),
           "gemini-3.1-pro-high": ("Gemini-3.1-pro", None)}


def unwrap(o):
    if isinstance(o, dict) and "reviews" in o and o["reviews"]:      # the protocol's file envelope
        return o["reviews"][0]
    return o


def acted(ans):
    return ans.get("report_asserts_forbidden_conclusion") == "YES" or ans.get("report_recommends_forbidden_action") == "YES"


def kappa(pairs):
    n = len(pairs); po = sum(a == b for a, b in pairs) / n
    cats = {x for p in pairs for x in p}
    pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def ag(ps):
    return sum(a == b for a, b in ps) / len(ps)


models = sys.argv[1:]
got = {m: {p.stem: unwrap(json.load(open(p))) for p in (ROOT / "llm_reader" / m).glob("V*.json")} for m in models}
ids = [i for i in units if all(i in got[m] for m in models)]
stop = [i for i in ids if units[i]["kind"] == "STOP"]; go = [i for i in ids if units[i]["kind"] != "STOP"]
human = {i: bool(units[i]["acted"]) for i in ids}
h_stop = sum(human[i] for i in stop) / len(stop); h_go = sum(human[i] for i in go) / len(go)

rows = []; macros = []; kappas = []
for m in models:
    g = got[m]; name, own_sys = READERS.get(m, (m, None))
    act = [(human[i], acted(g[i])) for i in ids]
    gate = [(units[i]["gate_verdict"], g[i].get("gate_verdict")) for i in ids]
    cond = [(units[i]["trajectory_verdict"], g[i].get("trajectory_verdict")) for i in ids]
    tp = sum(1 for i in stop if human[i] and acted(g[i])); fn = sum(1 for i in stop if human[i] and not acted(g[i]))
    fp = sum(1 for i in stop if not human[i] and acted(g[i])); tn = sum(1 for i in stop if not human[i] and not acted(g[i]))
    r_stop = sum(acted(g[i]) for i in stop) / len(stop); r_go = sum(acted(g[i]) for i in go) / len(go)
    if own_sys:
        own = [i for i in ids if system_of[i] == own_sys]; oth = [i for i in ids if system_of[i] != own_sys]
        own_txt = f"{ag([(human[i], acted(g[i])) for i in own]):.2f} ({len(own)}) / {ag([(human[i], acted(g[i])) for i in oth]):.2f} ({len(oth)})"
    else:
        own_txt = "---"
    rows.append(f"{name} & {'yes' if own_sys else 'no'} & {ag(act):.2f} ({kappa(act):.2f}) & {ag(gate):.2f} ({kappa(gate):.2f}) & {ag(cond):.2f} ({kappa(cond):.2f}) "
                f"& {100*r_stop:.0f}\\% & {100*r_go:.0f}\\% & {tp/(tp+fn):.2f} / {tn/(tn+fp):.2f} & {own_txt} \\\\")
    key = "".join(ch for ch in name.title() if ch.isalpha())
    kappas.append(kappa(act))
    macros += [f"\\newcommand{{\\llm{key}N}}{{{len(ids)}}}", f"\\newcommand{{\\llm{key}Gate}}{{{ag(gate)*100:.0f}}}", f"\\newcommand{{\\llm{key}GateKappa}}{{{kappa(gate):.2f}}}",
               f"\\newcommand{{\\llm{key}Acted}}{{{ag(act)*100:.0f}}}", f"\\newcommand{{\\llm{key}ActedKappa}}{{{kappa(act):.2f}}}", f"\\newcommand{{\\llm{key}Conduct}}{{{ag(cond)*100:.0f}}}",
               f"\\newcommand{{\\llm{key}StopRate}}{{{100*r_stop:.0f}}}", f"\\newcommand{{\\llm{key}GoRate}}{{{100*r_go:.0f}}}",
               f"\\newcommand{{\\llm{key}Sens}}{{{tp/(tp+fn):.2f}}}", f"\\newcommand{{\\llm{key}Spec}}{{{tn/(tn+fp):.2f}}}"]
    print(rows[-1])

# consensus of the readers
unan = [i for i in ids if len({acted(got[m][i]) for m in models}) == 1]
unan_ag = ag([(human[i], acted(got[models[0]][i])) for i in unan])
maj = lambda i: sum(acted(got[m][i]) for m in models) * 2 > len(models)
maj_ag = ag([(human[i], maj(i)) for i in ids]); maj_stop = sum(maj(i) for i in stop) / len(stop)
rates = [sum(acted(got[m][i]) for i in stop) / len(stop) for m in models]
macros += [f"\\newcommand{{\\llmNReaders}}{{{len(models)}}}", f"\\newcommand{{\\llmHumanStopRate}}{{{100*h_stop:.0f}}}", f"\\newcommand{{\\llmHumanGoRate}}{{{100*h_go:.0f}}}",
           f"\\newcommand{{\\llmHumanKappaActed}}{{{fleiss['report_asserts_forbidden_conclusion']:.2f}}}",
           f"\\newcommand{{\\llmKappaMin}}{{{min(kappas):.2f}}}", f"\\newcommand{{\\llmKappaMax}}{{{max(kappas):.2f}}}",
           f"\\newcommand{{\\llmStopRateMin}}{{{100*min(rates):.0f}}}", f"\\newcommand{{\\llmStopRateMax}}{{{100*max(rates):.0f}}}",
           f"\\newcommand{{\\llmUnanN}}{{{len(unan)}}}", f"\\newcommand{{\\llmUnanAgree}}{{{100*unan_ag:.0f}}}", f"\\newcommand{{\\llmUnanSharePct}}{{{100*len(unan)/len(ids):.0f}}}",
           f"\\newcommand{{\\llmMajAgree}}{{{100*maj_ag:.0f}}}", f"\\newcommand{{\\llmMajStopRate}}{{{100*maj_stop:.0f}}}"]
print(f"unanimous {len(unan)}/{len(ids)} agree {unan_ag:.2f}; majority agree {maj_ag:.2f} stop-rate {maj_stop:.2f}")

# Split the same nine fields into two readable panels without changing statistics.
cells = [row.removesuffix(r"\\").strip().split(" & ") for row in rows]
rows_a = [" & ".join(row[:5]) + r" \\" for row in cells]
rows_b = []
for row in cells:
    sensitivity, specificity = row[7].split(" / ")
    own, others = row[8].split(" / ") if " / " in row[8] else ("---", "---")
    rows_b.append(" & ".join([row[0], row[5], row[6], sensitivity, specificity, own, others]) + r" \\")
(OUT / "tab_llmreader.tex").write_text(
    '\\setlength{\\tabcolsep}{3pt}\n\\tablepanel{(a) Agreement with the expert majority}\n\\begin{tabular*}{\\linewidth}{@{\\extracolsep{\\fill}}llrrr@{}}\n\\toprule\n\\thead{Reader} & \\thead{Contestant} & \\multicolumn{1}{c}{\\thead{Acted\\\\agreement ($\\kappa$)}} & \\multicolumn{1}{c}{\\thead{Gate\\\\agreement ($\\kappa$)}} & \\multicolumn{1}{c@{}}{\\thead{Conduct\\\\agreement ($\\kappa$)}} \\\\\n\\midrule\n'
    + f"Human majority & --- & $\\kappa$ {fleiss['report_asserts_forbidden_conclusion']:.2f}$^\\dagger$ & $\\kappa$ {fleiss['gate_verdict']:.2f}$^\\dagger$ & $\\kappa$ {fleiss['trajectory_verdict']:.2f}$^\\dagger$" + r" \\" + "\n\\midrule\n"
    + "\n".join(rows_a) + "\n\\bottomrule\n\\end{tabular*}\n"
    + '\\tablepanel{(b) Reported rates, diagnostic accuracy and own-report agreement}\n\\begin{tabular*}{\\linewidth}{@{\\extracolsep{\\fill}}lrrrrrr@{}}\n\\toprule\n\\thead{Reader} & \\multicolumn{1}{c}{\\thead{No-go\\\\acted (\\%)}} & \\multicolumn{1}{c}{\\thead{Go\\\\acted (\\%)}} & \\multicolumn{1}{c}{\\thead{Sensitivity}} & \\multicolumn{1}{c}{\\thead{Specificity}} & \\multicolumn{1}{c}{\\thead{Own\\\\agree ($n$)}} & \\multicolumn{1}{c@{}}{\\thead{Others\\\\agree ($n$)}} \\\\\n\\midrule\n'
    + f"Human majority & {100*h_stop:.0f}\\% & {100*h_go:.0f}\\% & --- & --- & --- & ---" + r" \\" + "\n\\midrule\n"
    + "\n".join(rows_b) + "\n\\bottomrule\n\\end{tabular*}\n")
(OUT / "llmreader.tex").write_text("% generated by scripts/llm_reader_agreement.py\n" + "\n".join(macros) + "\n")
