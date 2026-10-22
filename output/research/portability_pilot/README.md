# Portability pilot: run evidence

This directory holds the primary evidence of the second-domain portability pilot, the
sixteen-task life-sciences extension reported in the portability appendix of the paper
(`paper/iclr/app_portability.tex`, `paper/iclr/tab_portability.tex`) and in the cross-domain
subsection of the experiments (`paper/iclr/tab_cross_domain.tex`). The pilot builds two cases
outside DMAIC on the unchanged task contract: `adb_c40` (bulk RNA-seq under library-batch
structure) and `adb_c41` (case-control GWAS under cohort structure), eight seeds each. Design
and rationale are in `docs/PORTABILITY_PILOT.md`; every count is in
`docs/RESULT_PORTABILITY_PILOT.md`.

Unlike the 97-task campaigns, whose per-trial artifacts are distributed as an archive with the
tagged release, the pilot's per-trial evidence is checked in here.

## Contents

| path | what it is |
|---|---|
| `evidence/<job>/<trial>/` | one directory per trial: `artifacts/trace.json`, `artifacts/report.md`, `artifacts/steward-audit.jsonl`, `verifier/` and `verifier-rescored/` scorecards, `config.json`, `result.json`. Trial directory names are Harbor's (`dmaic-<case>-t3-s<seed>-clean__<id>`). Identity strings and non-English text were removed before export. |
| `evidence/MANIFEST.json` | trial and file counts, the per-trial files kept and dropped (terminal recordings and turn records are not included), and the two scrub checks (`identity_strings_remaining`, `han_text_remaining`, both empty) |
| `trials.json` | one row per trial: system, job, task, seed, tier, attempt, reward and its axes (`pq`, `nf`, `ms_recall`, `ms_precision`, `ms_misuse`, `sc`), analyses attempted. Written by `scripts/pilot_portability_analysis.py` from `evidence/`. |
| `forks.json` | one row per graded fork: the correct branch, the branch chosen, the verdict, and whether the agent's own reported numbers agreed with the stop. Written by the same script. |
| `e2e/`, `e2e-v2/` | reference-solution runs of the built pilot tasks (`harbor/scripts/e2e.sh`): one log per task and a `summary.txt` showing reward 1.000 with `pq = nf = 1.0` on every task and zero truth values reachable in the agent image. `e2e/` is the first build (`adb_c41` only); `e2e-v2/` is the sixteen-task build. |

## Job names

Jobs are named `pilot-<system>[-v2][-bare][-fill]`. The systems are `gpt6astra` (GPT-6-astra),
`gpt56sol` (GPT-5.6-sol) and `gpt56luna` (GPT-5.6-luna).

| suffix | meaning |
|---|---|
| none (`pilot-gpt6astra`, `pilot-gpt56sol`) | the first build, v1: seeds 0 to 5, two forks per task, twelve tasks, run on two systems under the protocol brief. Its trials are kept beside the rest and are not reported separately. |
| `-v2` | the extended sixteen-task build: seeds 6 add a headline check that passes while a second criterion fails; seeds 7 put the stop at the end of a five-analysis project. Protocol brief (the instruction states each precondition and its consequence), three attempts per task. These jobs are the reported result. |
| `-v2-bare` | the same build under the thresholds-only brief, which states the thresholds and not the consequence of failing them. One attempt per task. |
| `-v2-bare-fill` | a one-trial job that re-ran a `-v2-bare` trial lost to a gateway error, so that the bare condition is complete. |

Every `-v2` and `-v2-bare` trial is re-scored against the `portability-pilot-v2r` and
`portability-pilot-v2r-bare` dataset builds (identical data; the builds carry the boolean-output
scorer fix described in `docs/PORTABILITY_PILOT.md`), and the analysis reads
`verifier-rescored/` where it exists.

## Scripts that read or write this directory

| script | role |
|---|---|
| `scripts/pilot_portability_analysis.py` | reads `evidence/`, writes `trials.json`, `forks.json`, `docs/RESULT_PORTABILITY_PILOT.md` and the paper's portability table |
| `scripts/fig_cross_domain.py` | reads `trials.json`, `forks.json` and the `e2e-v2/` logs for the cross-domain figure data |
| `scripts/rescore.py --dataset harbor/datasets/portability-pilot-v2r --apply` | recomputes the route axis into `verifier-rescored/` for a job directory |
| `scripts/pilot_export_release.py` | wrote `evidence/` and `MANIFEST.json` from the job directories; it carries the identity patterns it scrubs and is not in the review copy |
| `scripts/run-pilot-campaigns.sh`, `run-pilot-v2-campaigns.sh`, `run-pilot-bare-campaigns.sh`, `run-pilot-fill.sh`, `run-pilot-v2-orchestrate.sh` | the campaign runners that produced the jobs; they log to this directory |

Campaign logs and raw trajectory directories beside these files, where present, are working
material and are not part of the release.
