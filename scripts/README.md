# scripts/

Every script runs from the repository root. Python scripts that import the package or the
Harbor port need `PYTHONPATH=.:harbor/src` (some also need `:scripts`; each docstring says).
The analysis scripts expect the pinned analysis environment in `pyproject.toml`.

## Analysis inputs

Two kinds of input are not in the tracked tree:

- `harbor/jobs/` holds the per-trial run artifacts (traces, reports, steward audit logs,
  scorecards). It is gitignored and distributed as the results archive that
  `export_results.py` packs. Scripts that read it stop with a `missing input` message when
  it is absent.
- `output/research/control-replication-20260922.json` and
  `output/research/appendix_diagnostics/*.csv` are derived from `harbor/jobs/` by
  `control_replicated.py` and `fig_appendix_diagnostics.py`. They travel with the results
  archive; the figure scripts that read them stop with the same message when they are absent.

Everything else the analysis scripts read is tracked (`docs/*.json`, `paper/blind_review_*/`,
`output/research/portability_pilot/`).

## Analysis (regenerate numbers, tables, figures)

| Script | Purpose |
|---|---|
| `appendix_case33.py` | Case 33 appendix material: route graph, two timelines of one system, both reports. |
| `check_paper_figures.py` | Validate the canonical figure files and their order against `paper/iclr/figures/manifest.json`. |
| `construction_qc_inventory.py` | Map sealed expert-study checkpoints to the case/seed registry (`docs/CONSTRUCTION_QC.md`). |
| `control_replicated.py` | Replicated instruction control: `tab_ctlrep.tex`, `ctlrep.tex` and the control-replication JSON. |
| `export_results.py` | Pack the compact per-trial results archive from `harbor/jobs/`. |
| `fig_appendix_diagnostics.py` | Appendix diagnostic figures and the `appendix_diagnostics` CSV ledgers. |
| `fig_breakdown.py` | Decision-breakdown table and macros (`tab_decision_breakdown.tex`, `breakdown.tex`). |
| `fig_cross_domain.py` | Cross-domain (portability pilot) figure from the frozen pilot results. |
| `fig_expert_controls.py` | Figure 5 panels A to C from the expert study and the control replication. |
| `fig_instruction_controls.py` | Compact panel for the replicated instruction controls. |
| `fig_results_summary.py` | Figure 4 proposal and the comparison tables (`tab_main_results.tex`, `tab_control.tex`). |
| `fig_reward.py` | Reward components figure. |
| `fig_runtime_analysis.py` | Runtime and token analysis figure plus `tab_runtime_summary.tex`. |
| `fig_study2.py` | Study 2 figure and `study2_route_metrics.tex`. |
| `fig_task_breakdown.py` | Task breakdown figure (Figure 3) from the manuscript corpus table and the case registry. |
| `figure_pair_style.py` | Shared size and typography for Figures 5 and 6 (imported, not run). |
| `figure_palette.py` | Shared heatmap palette (imported, not run). |
| `listing_layout.py` | Reflow printed Markdown listings for the appendix (imported, not run). |
| `llm_reader_agreement.py` | Agreement of LLM readers with the human majority (`tab_llmreader.tex`, `llmreader.tex`). |
| `lockability.py` | Which preconditions the steward can lock (`tab_locks.tex`, `locks.tex`). |
| `matched_bootstrap.py` | Case-clustered bootstrap intervals for the matched-fork accuracies and deltas. |
| `pilot_portability_analysis.py` | Grade the portability pilot jobs and write `docs/RESULT_PORTABILITY_PILOT.md`. |
| `pq_scoping_delta.py` | Verdict transitions under the fork-scoped evidence rule (`scoping.tex`). |
| `rescore.py` | Re-score finished trials from their retained artifacts, no model calls. |
| `restraint_analysis.py` | Section 6 restraint-gap analysis: `numbers.tex` and `docs/RESULT_RESTRAINT.md`. |
| `review_audit_intervals.py` | Alternative interval families for the study 2 acted rate. |
| `review_confirm_forks.py` | Confirmation-fork decisions per agent and seed with error codes. |
| `review_coverage_sim.py` | Coverage simulation of the case-clustered bootstrap at 12 and 15 clusters. |
| `review_extract_dec.py` | Dump the per-decision records that `restraint_analysis.py` builds. |
| `review_lock_distinct.py` | Distinct lockable no-go forks per precondition type. |
| `review_main_intervals.py` | t and wild-bootstrap intervals for the main-campaign pooled rates. |
| `reward_sensitivity.py` | Ranking stability under alternative reward aggregations (`tab_sensitivity.tex`). |
| `select_control_pairs.py` | Pre-registered selection of the 32 paired control tasks (`docs/control_pairs_2026-09-19.json`). |
| `study2_agent_sensitivity.py` | Study 2 stratum table and sensitivity of the acted rate to the agent mix. |
| `study2_rescoring.py` | Study 2 audit sample under three assessment criteria. |

## Campaign (run model campaigns)

| Script | Purpose |
|---|---|
| `run-campaign.sh` | Run one campaign after checking disk, base images and the buildx builder. |
| `build-verifier-base.sh` | Build the verifier base image once so per-task builds run offline. |
| `campaign-env.sh` | Source the campaign credentials from a file outside the repository. |
| `agent-env.sh` | Export the per-provider variables the agent needs, derived from `providers.json`. |
| `llm_reader_pilot.py` | Run an LLM reader over the study 2 packets through an OpenAI-compatible endpoint. |

Operator configuration for these scripts, all environment variables:

| Variable | Meaning | Default |
|---|---|---|
| `DMAIC_ENV_FILE` | Credential file sourced before a campaign. | `~/.config/dmaic/campaign.env` |
| `DMAIC_PROVIDERS_FILE` | Provider table read by `agent-env.sh`. | `~/.config/dmaic/providers.json` |
| `DOCKER_HOST` | Container runtime socket. | The rootless podman machine socket |
| `BUILDX_BUILDER` | Named docker-container buildx builder that can reach the registry. | `proxied` |
| `PIP_PROXY` | Proxy passed to `pip` inside the verifier base build only. | unset |
| `DMAIC_PILOT_PROVIDER` | Provider id, in `providers.json`, used by the pilot runners below. | required, no default |

## Operations (author-side infrastructure)

One-off runners and release tooling written for the authors' hosts. They assume local job
configs (`campaign-*.local.yaml`, gitignored), a specific container VM and provider
gateways, and are kept for the record; a reader does not need them to regenerate any
number in the paper.

| Script | Purpose |
|---|---|
| `run-pilot-campaigns.sh` | Sequential runner for the three pilot campaigns on the life-sciences dataset. |
| `run-pilot-v2-campaigns.sh` | Sequential runner for the six extended pilot campaigns. |
| `run-pilot-v2-orchestrate.sh` | Wait for a running campaign, validate the trap tasks end to end, hand over to the v2 runner. |
| `run-pilot-bare-campaigns.sh` | Thresholds-only control of the pilot, run after the main pilot campaigns. |
| `run-pilot-fill.sh` | Re-run one pilot trial lost to a gateway error. |
| `deficit_fill.py` | Emit a fill campaign for tasks with no scored trial in the given job directories. |
| `ctl_deficit_fill.py` | Per-deficit fills that bring every control task to three scored attempts. |
| `kimi_deficit_fill.py` | Per-deficit fills across one system's job directories. |
| `qwen_deficit_fill.py` | One-attempt fill for the tasks of one system still short of three attempts. |
| `make-fill.py` | Fill campaign for the trials of one job that ended in an exception. |
| `qwen_pick_provider.py` | Pick the first configured gateway that currently serves a model. |
| `authors.py` | Generate the camera-ready author block from a gitignored author file. |
| `push-overleaf.sh` | Sync the manuscript and figures to the authors' Overleaf project. |
| `make_anon_release.sh` | Build the anonymised review copy of this repository. |
| `pilot_export_release.py` | Pack the portability pilot evidence into the tree, anonymised. |

Not in the public release: `deficit_fill.py`, `ctl_deficit_fill.py`, `kimi_deficit_fill.py`, `qwen_deficit_fill.py`, `make-fill.py`, `qwen_pick_provider.py` (repairs for interrupted campaigns on the authors' infrastructure), `authors.py`, `push-overleaf.sh`, `make_anon_release.sh` and `pilot_export_release.py` (manuscript and release tooling).
