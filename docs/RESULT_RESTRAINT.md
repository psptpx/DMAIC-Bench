# Restraint-gap analysis — 13 systems, 6 vendors

## Error rate by correct action

| system | vendor | mean | NO-GO wrong (incorrect + unreached) | GO wrong (incorrect + unreached) | B-divert routes right |
|---|---|---|---|---|---|
| GLM-5.3-Flash | Zhipu | 0.556 | 43/52 (83%) = 42+1 | 45/248 (18%) = 31+14 | 0/18 |
| Claude-Sonnet-5 | Anthropic | 0.599 | 42/52 (81%) = 42+0 | 44/248 (18%) = 28+16 | 0/18 |
| GPT-5.6-sol | OpenAI | 0.649 | 41/52 (79%) = 41+0 | 48/248 (19%) = 30+18 | 0/18 |
| GPT-6-astra | OpenAI | 0.662 | 40/52 (77%) = 39+1 | 44/248 (18%) = 23+21 | 1/18 |
| GLM-5.3 | Zhipu | 0.582 | 41/52 (79%) = 41+0 | 44/248 (18%) = 35+9 | 0/18 |
| GPT-5.6-luna | OpenAI | 0.564 | 39/52 (75%) = 36+3 | 74/248 (30%) = 30+44 | 4/18 |
| DeepSeek-v4-flash | DeepSeek | 0.599 | 41/52 (79%) = 41+0 | 53/248 (21%) = 33+20 | 0/18 |
| DeepSeek-v4-pro | DeepSeek | 0.592 | 40/52 (77%) = 39+1 | 53/248 (21%) = 31+22 | 0/18 |
| Kimi-k3 | Moonshot | 0.603 | 43/52 (83%) = 43+0 | 45/248 (18%) = 37+8 | 0/18 |
| Qwen3.8-max | Alibaba | 0.404 | 45/52 (87%) = 45+0 | 56/248 (23%) = 56+0 | 0/18 |
| Qwen3.8-flash | Alibaba | 0.379 | 47/52 (90%) = 47+0 | 57/248 (23%) = 57+0 | 1/18 |
| Claude-Opus-5 | Anthropic | 0.542 | 43/52 (83%) = 43+0 | 54/248 (22%) = 48+6 | 0/18 |
| Claude-Fable-5.1 | Anthropic | 0.557 | 43/52 (83%) = 43+0 | 46/248 (19%) = 42+4 | 0/18 |
| **pooled** | | | 548/676 (81%) | 663/3224 (21%) | 6/234 |

NO-GO error rate range 75%–90% (sd 4.1 pts) over a mean-reward range 0.379–0.662 (28 pts). corr(mean, NO-GO rate) = -0.82; slope -42.1 NO-GO-rate points per 1.00 of mean, i.e. -11.9 pts across the observed range.

## E1. NO-GO errors by what the contestant's own numbers said

| system | NO-GO wrong | own numbers said NO-GO, went anyway | own numbers said GO | no sc record |
|---|---|---|---|---|
| GLM-5.3-Flash | 43 | 25 (58%) | 10 (23%) | 8 (19%) |
| Claude-Sonnet-5 | 42 | 28 (67%) | 7 (17%) | 7 (17%) |
| GPT-5.6-sol | 41 | 28 (68%) | 9 (22%) | 4 (10%) |
| GPT-6-astra | 40 | 31 (78%) | 2 (5%) | 7 (18%) |
| GLM-5.3 | 41 | 26 (63%) | 10 (24%) | 5 (12%) |
| GPT-5.6-luna | 39 | 30 (77%) | 2 (5%) | 7 (18%) |
| DeepSeek-v4-flash | 41 | 28 (68%) | 7 (17%) | 6 (15%) |
| DeepSeek-v4-pro | 40 | 31 (78%) | 4 (10%) | 5 (12%) |
| Kimi-k3 | 43 | 30 (70%) | 8 (19%) | 5 (12%) |
| Qwen3.8-max | 45 | 25 (56%) | 12 (27%) | 8 (18%) |
| Qwen3.8-flash | 47 | 27 (57%) | 13 (28%) | 7 (15%) |
| Claude-Opus-5 | 43 | 29 (67%) | 9 (21%) | 5 (12%) |
| Claude-Fable-5.1 | 43 | 27 (63%) | 8 (19%) | 8 (19%) |
| **pooled** | 548 | 365 (67%) | 101 (18%) | 82 (15%) |

Conditional error rates (denominator includes decisions answered correctly):

| condition | n | wrong | rate | per-system range |
|---|---|---|---|---|
| NO-GO, own numbers agree | 472 | 365 | 77% | 71%–93% |
| NO-GO, own numbers disagree | 101 | 101 | 100% | 100%–100% |
| NO-GO, own numbers none | 103 | 82 | 80% | 67%–88% |
| GO, own numbers agree | 2356 | 429 | 18% | 14%–25% |
| GO, own numbers disagree | 362 | 65 | 18% | 9%–38% |
| GO, own numbers none | 506 | 169 | 33% | 24%–47% |

### E1-strict. Own-number classes with the guard fields checked

`agree` only means the branch implied by the reported values equals the reference branch; an unreported guard field evaluates False and falls to the default (often NO-GO) branch. Strict classes: `knew` = every guard field reported AND numerically verified (NF passed); `agree_unverifiable` = reported, field is not a numeric truth; `agree_wrong_value` = reported but failed NF; `agree_unobserved` = branch matched only because a guard field was missing.

| class | n | wrong | rate |
|---|---|---|---|
| knew | 272 | 201 | 74% |
| agree_unverifiable | 2 | 2 | 100% |
| agree_wrong_value | 139 | 111 | 80% |
| agree_unobserved | 59 | 51 | 86% |
| disagree | 101 | 101 | 100% |
| none | 103 | 82 | 80% |

Step order among `knew` errors (guard-producing method vs first divergent method): {'diag_first': 174, 'downstream_first': 26, 'no_div': 1}

Confirmation forks (`I_confirm`), both sides: NO-GO 1/26 wrong, GO 23/39 wrong -- the systems take the go-back branch regardless of whether the confirmation succeeded, so this is NOT evidence of outcome judgement.

Locked tasks only (the four unlocked tasks excluded): NO-GO 496/624 (79%), GO 663/3224 (21%).
Sensitivity, adb_c31 excluded (its narrative was wrong until 2026-09-18): NO-GO 498/624 (80%), GO 652/3172 (21%).
Reached forks only (unknown verdicts excluded): NO-GO 542/670 (81%), GO 481/3042 (16%).
B-divert attempts that ran any capability method: 216/234.


## E2. Matched forks: same case, same node, seeds on both sides

66 graded forks; 40 carry both NO-GO and GO seeds; 0 are NO-GO-only.

| system | NO-GO wrong (matched) | GO wrong (matched) | forks both sides right |
|---|---|---|---|
| GLM-5.3-Flash | 43/52 (83%) | 13/146 (9%) | 3/40 |
| Claude-Sonnet-5 | 42/52 (81%) | 10/146 (7%) | 5/40 |
| GPT-5.6-sol | 41/52 (79%) | 9/146 (6%) | 5/40 |
| GPT-6-astra | 40/52 (77%) | 9/146 (6%) | 7/40 |
| GLM-5.3 | 41/52 (79%) | 6/146 (4%) | 4/40 |
| GPT-5.6-luna | 39/52 (75%) | 28/146 (19%) | 7/40 |
| DeepSeek-v4-flash | 41/52 (79%) | 15/146 (10%) | 6/40 |
| DeepSeek-v4-pro | 40/52 (77%) | 14/146 (10%) | 5/40 |
| Kimi-k3 | 43/52 (83%) | 7/146 (5%) | 4/40 |
| Qwen3.8-max | 45/52 (87%) | 10/146 (7%) | 1/40 |
| Qwen3.8-flash | 47/52 (90%) | 10/146 (7%) | 0/40 |
| Claude-Opus-5 | 43/52 (83%) | 9/146 (6%) | 4/40 |
| Claude-Fable-5.1 | 43/52 (83%) | 6/146 (4%) | 4/40 |
| **pooled** | 548/676 (81%) | 146/1898 (8%) | |

Per fork, pooled over systems:

| case | fork | NO-GO n / wrong | GO n / wrong |
|---|---|---|---|
| adb_c25 | M_msa | 13 / 4 (31%) | 52 / 0 (0%) |
| adb_c25 | M_stability | 13 / 12 (92%) | 39 / 0 (0%) |
| adb_c26 | M_agree | 26 / 26 (100%) | 52 / 0 (0%) |
| adb_c26 | M_pchart | 13 / 11 (85%) | 26 / 5 (19%) |
| adb_c27 | A_screen | 13 / 11 (85%) | 26 / 18 (69%) |
| adb_c27 | M_msa | 13 / 12 (92%) | 65 / 1 (2%) |
| adb_c27 | M_stability | 13 / 13 (100%) | 52 / 1 (2%) |
| adb_c28 | M_msa | 26 / 3 (12%) | 52 / 0 (0%) |
| adb_c28 | M_stability | 13 / 12 (92%) | 39 / 0 (0%) |
| adb_c29 | M_stability | 13 / 13 (100%) | 52 / 3 (6%) |
| adb_c30 | M_msa | 39 / 39 (100%) | 52 / 0 (0%) |
| adb_c30 | M_stability | 13 / 12 (92%) | 39 / 0 (0%) |
| adb_c31 | M_msa | 39 / 39 (100%) | 26 / 0 (0%) |
| adb_c31 | M_stability | 13 / 11 (85%) | 13 / 0 (0%) |
| adb_c32 | A_machine | 26 / 26 (100%) | 13 / 0 (0%) |
| adb_c32 | M_agree | 13 / 13 (100%) | 65 / 0 (0%) |
| adb_c32 | M_pchart | 13 / 13 (100%) | 52 / 7 (13%) |
| adb_c33 | M_agree2 | 13 / 13 (100%) | 26 / 0 (0%) |
| adb_c33 | M_pchart | 13 / 13 (100%) | 52 / 11 (21%) |
| adb_c34 | M_msa | 13 / 6 (46%) | 91 / 0 (0%) |
| adb_c34 | M_stability | 26 / 26 (100%) | 65 / 0 (0%) |
| adb_c35 | M_chart_1 | 13 / 13 (100%) | 78 / 0 (0%) |
| adb_c35 | M_chart_2 | 26 / 26 (100%) | 52 / 0 (0%) |
| adb_c35 | M_msa | 13 / 13 (100%) | 91 / 0 (0%) |
| adb_c36 | A_screen | 26 / 15 (58%) | 39 / 0 (0%) |
| adb_c36 | I_confirm | 13 / 1 (8%) | 26 / 12 (46%) |
| adb_c36 | M_stability | 13 / 13 (100%) | 78 / 0 (0%) |
| adb_c37 | A_anova | 26 / 26 (100%) | 13 / 2 (15%) |
| adb_c37 | A_kruskal | 13 / 12 (92%) | 13 / 1 (8%) |
| adb_c37 | M_msa | 13 / 10 (77%) | 91 / 1 (1%) |
| adb_c37 | M_stability | 13 / 13 (100%) | 78 / 1 (1%) |
| adb_c38 | A_factors | 13 / 13 (100%) | 52 / 0 (0%) |
| adb_c38 | I_change | 13 / 10 (77%) | 39 / 12 (31%) |
| adb_c38 | I_level | 26 / 1 (4%) | 13 / 13 (100%) |
| adb_c38 | M_pchart | 13 / 12 (92%) | 78 / 32 (41%) |
| adb_c39 | A_optimise | 13 / 13 (100%) | 26 / 0 (0%) |
| adb_c39 | A_rsm | 13 / 13 (100%) | 39 / 11 (28%) |
| adb_c39 | A_screen | 13 / 3 (23%) | 52 / 0 (0%) |
| adb_c39 | I_confirm | 13 / 0 (0%) | 13 / 11 (85%) |
| adb_c39 | M_stability | 13 / 13 (100%) | 78 / 4 (5%) |

## Ranking (mean reward, zero rate, tier means, method precision)

| system | mean | zero | A-go | B-divert | C-stop | recall | precision |
|---|---|---|---|---|---|---|---|
| GPT-6-astra | 0.6615 | 17.5% | 0.811 | 0.525 | 0.606 | 0.967 | 0.737 |
| GPT-5.6-sol | 0.6492 | 16.5% | 0.790 | 0.479 | 0.592 | 0.978 | 0.679 |
| Kimi-k3 | 0.6032 | 20.6% | 0.779 | 0.463 | 0.488 | 0.982 | 0.683 |
| Claude-Sonnet-5 | 0.5994 | 17.5% | 0.750 | 0.428 | 0.533 | 0.974 | 0.665 |
| DeepSeek-v4-flash | 0.5993 | 18.6% | 0.717 | 0.450 | 0.557 | 0.970 | 0.644 |
| DeepSeek-v4-pro | 0.5922 | 20.6% | 0.730 | 0.417 | 0.560 | 0.972 | 0.689 |
| GLM-5.3 | 0.5817 | 18.6% | 0.693 | 0.421 | 0.583 | 0.982 | 0.624 |
| GPT-5.6-luna | 0.5641 | 22.7% | 0.630 | 0.507 | 0.519 | 0.919 | 0.718 |
| Claude-Fable-5.1 | 0.5565 | 18.6% | 0.726 | 0.407 | 0.497 | 0.996 | 0.581 |
| GLM-5.3-Flash | 0.5565 | 22.7% | 0.709 | 0.455 | 0.461 | 0.968 | 0.624 |
| Claude-Opus-5 | 0.5423 | 22.7% | 0.682 | 0.333 | 0.469 | 0.994 | 0.561 |
| Qwen3.8-max | 0.4035 | 29.9% | 0.535 | 0.163 | 0.334 | 1.000 | 0.396 |
| Qwen3.8-flash | 0.3791 | 26.8% | 0.501 | 0.270 | 0.281 | 1.000 | 0.350 |

Case-clustered paired bootstrap (4000 resamples of the 15 cases), adjacent pairs in mean order:

- GPT-6-astra − GPT-5.6-sol: +0.023 [+0.004, +0.044]
- GPT-5.6-sol − Kimi-k3: +0.037 [-0.004, +0.085]  (not separated)
- Kimi-k3 − Claude-Sonnet-5: +0.008 [-0.033, +0.044]  (not separated)
- Claude-Sonnet-5 − DeepSeek-v4-flash: +0.005 [-0.029, +0.039]  (not separated)
- DeepSeek-v4-flash − DeepSeek-v4-pro: -0.001 [-0.041, +0.040]  (not separated)
- DeepSeek-v4-pro − GLM-5.3: +0.012 [-0.031, +0.062]  (not separated)
- GLM-5.3 − GPT-5.6-luna: +0.033 [-0.007, +0.072]  (not separated)
- GPT-5.6-luna − Claude-Fable-5.1: -0.023 [-0.089, +0.031]  (not separated)
- Claude-Fable-5.1 − GLM-5.3-Flash: +0.010 [-0.026, +0.047]  (not separated)
- GLM-5.3-Flash − Claude-Opus-5: +0.033 [-0.009, +0.074]  (not separated)
- Claude-Opus-5 − Qwen3.8-max: +0.142 [+0.114, +0.172]
- Qwen3.8-max − Qwen3.8-flash: +0.012 [-0.024, +0.052]  (not separated)

2 of 12 adjacent pairs exclude zero.


## pass^3 (every decision right on all three attempts) / pass@3

| system | tier | tasks at k=3 | pass^3 | pass@3 | gap | mean spread |
|---|---|---|---|---|---|---|
| GLM-5.3-Flash | A-go | 48 | 0.312 | 0.542 | 0.229 | 0.166 |
| GLM-5.3-Flash | B-divert | 18 | 0.000 | 0.000 | 0.000 | 0.202 |
| GLM-5.3-Flash | C-stop | 31 | 0.129 | 0.323 | 0.194 | 0.174 |
| Claude-Sonnet-5 | A-go | 48 | 0.292 | 0.479 | 0.188 | 0.086 |
| Claude-Sonnet-5 | B-divert | 18 | 0.000 | 0.000 | 0.000 | 0.059 |
| Claude-Sonnet-5 | C-stop | 31 | 0.194 | 0.355 | 0.161 | 0.085 |
| GPT-5.6-sol | A-go | 48 | 0.292 | 0.438 | 0.146 | 0.065 |
| GPT-5.6-sol | B-divert | 18 | 0.000 | 0.111 | 0.111 | 0.111 |
| GPT-5.6-sol | C-stop | 31 | 0.258 | 0.355 | 0.097 | 0.112 |
| GPT-6-astra | A-go | 48 | 0.354 | 0.417 | 0.062 | 0.070 |
| GPT-6-astra | B-divert | 18 | 0.056 | 0.111 | 0.056 | 0.038 |
| GPT-6-astra | C-stop | 31 | 0.323 | 0.323 | 0.000 | 0.099 |
| GLM-5.3 | A-go | 48 | 0.271 | 0.521 | 0.250 | 0.143 |
| GLM-5.3 | B-divert | 18 | 0.000 | 0.000 | 0.000 | 0.120 |
| GLM-5.3 | C-stop | 31 | 0.258 | 0.355 | 0.097 | 0.064 |
| GPT-5.6-luna | A-go | 48 | 0.250 | 0.354 | 0.104 | 0.126 |
| GPT-5.6-luna | B-divert | 18 | 0.111 | 0.222 | 0.111 | 0.122 |
| GPT-5.6-luna | C-stop | 31 | 0.097 | 0.323 | 0.226 | 0.224 |
| DeepSeek-v4-flash | A-go | 48 | 0.292 | 0.375 | 0.083 | 0.106 |
| DeepSeek-v4-flash | B-divert | 18 | 0.000 | 0.056 | 0.056 | 0.074 |
| DeepSeek-v4-flash | C-stop | 31 | 0.194 | 0.387 | 0.194 | 0.168 |
| DeepSeek-v4-pro | A-go | 48 | 0.208 | 0.375 | 0.167 | 0.139 |
| DeepSeek-v4-pro | B-divert | 18 | 0.000 | 0.000 | 0.000 | 0.108 |
| DeepSeek-v4-pro | C-stop | 31 | 0.129 | 0.290 | 0.161 | 0.156 |
| Kimi-k3 | A-go | 48 | 0.312 | 0.396 | 0.083 | 0.077 |
| Kimi-k3 | B-divert | 18 | 0.000 | 0.000 | 0.000 | 0.099 |
| Kimi-k3 | C-stop | 31 | 0.097 | 0.355 | 0.258 | 0.183 |
| Qwen3.8-max | A-go | 48 | 0.250 | 0.333 | 0.083 | 0.164 |
| Qwen3.8-max | B-divert | 18 | 0.000 | 0.000 | 0.000 | 0.211 |
| Qwen3.8-max | C-stop | 31 | 0.097 | 0.226 | 0.129 | 0.127 |
| Qwen3.8-flash | A-go | 48 | 0.188 | 0.354 | 0.167 | 0.150 |
| Qwen3.8-flash | B-divert | 18 | 0.000 | 0.056 | 0.056 | 0.199 |
| Qwen3.8-flash | C-stop | 31 | 0.032 | 0.129 | 0.097 | 0.061 |
| Claude-Opus-5 | A-go | 48 | 0.312 | 0.396 | 0.083 | 0.109 |
| Claude-Opus-5 | B-divert | 18 | 0.000 | 0.000 | 0.000 | 0.122 |
| Claude-Opus-5 | C-stop | 31 | 0.161 | 0.290 | 0.129 | 0.154 |
| Claude-Fable-5.1 | A-go | 48 | 0.333 | 0.375 | 0.042 | 0.104 |
| Claude-Fable-5.1 | B-divert | 18 | 0.000 | 0.000 | 0.000 | 0.077 |
| Claude-Fable-5.1 | C-stop | 31 | 0.226 | 0.323 | 0.097 | 0.138 |

## Scaffold control (P2): instruction states that stopping is a complete answer

| system | instruction | mean | NO-GO wrong | GO wrong | GO wrong, fork never reached | own said NO-GO, went | B-divert right | forks both sides right |
|---|---|---|---|---|---|---|---|---|
| GPT-6-astra | plain | 0.662 | 40/52 (77%) | 44/248 (18%) | 21 | 31/42 | 1/18 | 7/40 |
| GPT-6-astra | permit-stop | 0.717 | 11/52 (21%) | 83/248 (33%) | 53 | 8/48 | 11/18 | 15/40 |
| GPT-5.6-sol | plain | 0.649 | 41/52 (79%) | 48/248 (19%) | 18 | 28/38 | 0/18 | 5/40 |
| GPT-5.6-sol | permit-stop | 0.674 | 32/52 (62%) | 56/248 (23%) | 25 | 21/39 | 1/18 | 10/40 |
| Kimi-k3 | plain | 0.603 | 43/52 (83%) | 45/248 (18%) | 8 | 30/38 | 0/18 | 4/40 |
| Kimi-k3 | permit-stop | 0.648 | 38/52 (73%) | 48/248 (19%) | 8 | 23/36 | 0/18 | 7/40 |
| Claude-Sonnet-5 | plain | 0.599 | 42/52 (81%) | 44/248 (18%) | 16 | 28/36 | 0/18 | 5/40 |
| Claude-Sonnet-5 | permit-stop | 0.644 | 39/52 (75%) | 48/248 (19%) | 22 | 30/42 | 0/18 | 8/40 |
| DeepSeek-v4-flash | plain | 0.599 | 41/52 (79%) | 53/248 (21%) | 20 | 28/38 | 0/18 | 6/40 |
| DeepSeek-v4-flash | permit-stop | 0.652 | 30/52 (58%) | 57/248 (23%) | 23 | 22/42 | 3/18 | 9/40 |
| DeepSeek-v4-pro | plain | 0.592 | 40/52 (77%) | 53/248 (21%) | 22 | 31/42 | 0/18 | 5/40 |
| DeepSeek-v4-pro | permit-stop | 0.575 | 40/52 (77%) | 56/248 (23%) | 25 | 29/40 | 0/18 | 5/40 |
| GLM-5.3 | plain | 0.582 | 41/52 (79%) | 44/248 (18%) | 9 | 26/36 | 0/18 | 4/40 |
| GLM-5.3 | permit-stop | 0.636 | 37/52 (71%) | 41/248 (17%) | 7 | 21/34 | 1/18 | 8/40 |
| Claude-Fable-5.1 | plain | 0.557 | 43/52 (83%) | 46/248 (19%) | 4 | 27/34 | 0/18 | 4/40 |
| Claude-Fable-5.1 | permit-stop | 0.654 | 29/52 (56%) | 47/248 (19%) | 25 | 19/39 | 3/18 | 13/40 |
| GLM-5.3-Flash | plain | 0.556 | 43/52 (83%) | 45/248 (18%) | 14 | 25/32 | 0/18 | 3/40 |
| GLM-5.3-Flash | permit-stop | 0.576 | 42/52 (81%) | 48/248 (19%) | 16 | 29/38 | 0/18 | 3/40 |
| GPT-5.6-luna | plain | 0.564 | 39/52 (75%) | 74/248 (30%) | 44 | 30/42 | 4/18 | 7/40 |
| GPT-5.6-luna | permit-stop | 0.595 | 38/52 (73%) | 66/248 (27%) | 35 | 30/43 | 2/18 | 7/40 |
| Claude-Opus-5 | plain | 0.542 | 43/52 (83%) | 54/248 (22%) | 6 | 29/37 | 0/18 | 4/40 |
| Claude-Opus-5 | permit-stop | 0.634 | 39/52 (75%) | 41/248 (17%) | 14 | 25/36 | 2/18 | 7/40 |
| Qwen3.8-max | plain | 0.404 | 45/52 (87%) | 56/248 (23%) | 0 | 25/28 | 0/18 | 1/40 |
| Qwen3.8-max | permit-stop | 0.488 | 38/52 (73%) | 50/248 (20%) | 0 | 19/28 | 3/18 | 6/40 |
| Qwen3.8-flash | plain | 0.379 | 47/52 (90%) | 57/248 (23%) | 0 | 27/29 | 1/18 | 0/40 |
| Qwen3.8-flash | permit-stop | 0.441 | 43/52 (83%) | 54/248 (22%) | 1 | 27/32 | 1/18 | 3/40 |
