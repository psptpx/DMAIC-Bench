# Current manuscript figures

This directory contains exactly the 14 figures included by the current manuscript, numbered in compiled order. Asset filenames are stable identifiers; inserting a main-text figure changes displayed appendix numbers without renaming or editing their artwork. Figures 1–5 are in the main text; Figures 6–14 are in the appendix. The manuscript includes the vector **PDF** files. Matching **SVG** files retain the editable artwork; **PNG** previews are rendered from those exact PDFs at 240 dpi.

`manifest.json` records every file, figure label, page, previous stem, and SHA-256 hash. Page numbers refer to the current 54-page review PDF (nine pages of main text).

| Figure | Page | Description | PDF | SVG | PNG |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | Motivation and design of DMAIC-Bench | [figure01_workflow.pdf](figure01_workflow.pdf) | [SVG](figure01_workflow.svg) | [PNG](figure01_workflow.png) |
| 2 | 4 | DMAIC-Bench architecture | [figure02_architecture.pdf](figure02_architecture.pdf) | [SVG](figure02_architecture.svg) | [PNG](figure02_architecture.png) |
| 3 | 5 | Task breakdown | [figure03_task_breakdown.pdf](figure03_task_breakdown.pdf) | [SVG](figure03_task_breakdown.svg) | [PNG](figure03_task_breakdown.png) |
| 4 | 8 | Reward, restraint, and reliability | [figure04_results_summary.pdf](figure04_results_summary.pdf) | [SVG](figure04_results_summary.svg) | [PNG](figure04_results_summary.png) |
| 5 | 9 | Report validity and routing interventions | [figure05_expert_controls.pdf](figure05_expert_controls.pdf) | [SVG](figure05_expert_controls.svg) | [PNG](figure05_expert_controls.png) |
| 6 | 22 | Execution-time and token distributions | [figure06_resource_distributions.pdf](figure06_resource_distributions.pdf) | [SVG](figure06_resource_distributions.svg) | [PNG](figure06_resource_distributions.png) |
| 7 | 23 | Execution time by model and task | [figure07_runtime_by_task.pdf](figure07_runtime_by_task.pdf) | [SVG](figure07_runtime_by_task.svg) | [PNG](figure07_runtime_by_task.png) |
| 8 | 24 | Resources and route correctness on C-stop tasks | [figure08_stop_task_resources.pdf](figure08_stop_task_resources.pdf) | [SVG](figure08_stop_task_resources.svg) | [PNG](figure08_stop_task_resources.png) |
| 9 | 25 | Case 33 and its two reference routes | [figure09_case33_routes.pdf](figure09_case33_routes.pdf) | [SVG](figure09_case33_routes.svg) | [PNG](figure09_case33_routes.png) |
| 10 | 39 | Reward components and evidence sources | [figure10_reward_components.pdf](figure10_reward_components.pdf) | [SVG](figure10_reward_components.svg) | [PNG](figure10_reward_components.png) |
| 11 | 42 | Warranted continuation: A-go tasks | [figure11_heatmap_go.pdf](figure11_heatmap_go.pdf) | [SVG](figure11_heatmap_go.svg) | [PNG](figure11_heatmap_go.png) |
| 12 | 42 | Warranted diversion: B-divert tasks | [figure12_heatmap_divert.pdf](figure12_heatmap_divert.pdf) | [SVG](figure12_heatmap_divert.svg) | [PNG](figure12_heatmap_divert.png) |
| 13 | 43 | Warranted terminal stopping: C-stop tasks | [figure13_heatmap_stop.pdf](figure13_heatmap_stop.pdf) | [SVG](figure13_heatmap_stop.svg) | [PNG](figure13_heatmap_stop.png) |
| 14 | 44 | Correct routes and decision errors | [figure14_decision_outcomes.pdf](figure14_decision_outcomes.pdf) | [SVG](figure14_decision_outcomes.svg) | [PNG](figure14_decision_outcomes.png) |

## Export notes

- Figures 1, 2 and 3 are authored artwork rather than script output; the PDF and SVG are the sources and the PNG is a 240-dpi rendering of the PDF. `scripts/fig_task_breakdown.py` does not reproduce the accepted Figure 3.
- Figure 4 shows 13 agents in panel (a) and nine agents on 97 shared tasks in panel (b); the full 13-agent reliability analysis is in the appendix. `scripts/fig_results_summary.py` writes an alternative to `output/figure_proposals/` and does not overwrite manuscript artwork.
- Figure 5 is the single A/B/C triptych exported by `scripts/fig_expert_controls.py`.
- Figure 10 requires `--export-text-to-path` when exporting its SVG through Inkscape to avoid a font-subset/Cairo truncation problem. The SVG itself remains editable.
- The decision breakdown and the cross-domain evaluation are native LaTeX tables (`tab_decision_breakdown.tex`, `tab_cross_domain.tex`), not manuscript figures.

Use `python3 scripts/check_paper_figures.py` from the repository root to check the inventory, file hashes, and expanded LaTeX inclusion order. After an intentional artwork update, update the corresponding manifest hashes and regenerate the PNG from the PDF.
