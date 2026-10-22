# Seal-strength improvement report

## Executive position

The original line was orderly but not capable of delivering the product commitment. Its mean was **51.197 N**, versus the **55 N** committed level and **45 N** engineering minimum. The confirmation seals made at the recommended settings averaged **59.873 N**. Their observed mean improvement over baseline was **8.676 N**.

The change is successful as a confirmation result, but production release should remain controlled: the response-surface experiment predicted a much lower local maximum than the later confirmation batch achieved, so the exact settings and other process conditions must be locked and reconciled before assuming transferability.

## Baseline behavior and requirement

The ordered baseline had mean **51.197 N**, median **51.420 N**, and standard deviation **4.359 N**. Distributional normality was not rejected by Anderson-Darling (**p = 0.444**).

The individuals chart center was **51.197 N**, with limits **37.816 N** and **64.579 N** and **0** points beyond them. The runs-test result (**p = 0.435**) also did not identify nonrandom ordering. Thus there is no detected point or run signal, but stability does not imply adequacy.

The one-sided mean test against **55 N** gave **t = -6.758**, **p = 3.47e-09**: baseline strength was below the commitment. There were **4** observed results below **45 N** and **50** below **55 N**. Lower one-sided capability at the engineering minimum was **Cpk = 0.463** and **Ppk = 0.474**. Cp and Pp cannot be computed because no upper specification was provided.

## Which settings account for strength

The replicated screening factorial model was significant (**p = 0.0037**) and explained **88.08%** of observed variation. Moving bond angle from coded low to high increased fitted strength by **4.628 N** (**p = 0.0003**); moving bead spacing from low to high increased it by **3.082 N** (**p = 0.0036**). Cure temperature's fitted effect was **0.597 N** (**p = 0.454**) and was not significant. The bond-angle-by-spacing interaction was also not significant (**p = 0.068**). This supports carrying bond angle and bead spacing—not cure temperature—into design work.

## What the composite design supports

The quadratic response-surface model was significant (**p = 0.0005**) with **R-squared = 93.57%**. Lack of fit was not detected (**p = 0.963**), but residual normality was rejected (**p = 0.012**), so model inference should be treated cautiously.

The stationary point was at coded bond angle **0.241** and bead spacing **0.234**. Both curvature eigenvalues were negative (**-3.196**, **-2.403**), supporting a local maximum. The fitted strength there was only **48.362 N**, with an individual prediction interval from **46.912 N** to **49.813 N**—below the product commitment. The design therefore locates a local optimum in its studied region but, by itself, does not demonstrate the required margin.

## What the change achieved

At the recommended settings the confirmation mean was **59.873 N**, with standard deviation **1.708 N** and minimum **57.530 N**. There were **0** observed results below **55 N** and **0** below **45 N**. A one-sided test against the commitment gave **t = 12.762**, **p = 4.55e-11**.

The confirmation individuals chart had **0** points beyond limits, and normality was not rejected (**p = 0.211**). Against **55 N**, lower one-sided capability was **Cpk = 0.882** and **Ppk = 0.951**. The variance test rejected equality (**p = 0.000251**), so a Welch comparison was used; it found an increase of **8.676 N** (**t = 12.758**, **p = 1.45e-20**).

## Recommended next action and control

Approve the recommended settings for a controlled production trial, not unconditional closure. Freeze the bond-angle and bead-spacing recipes, record cure temperature as a controlled background condition, and verify material, equipment, and measurement conditions that differed between the composite experiment and confirmation production. The large gap between the model prediction and confirmation mean must be reconciled.

Continue ordered seal-strength monitoring with an individuals/moving-range chart and react to special-cause signals. Review lower one-sided capability against the committed level after a longer production run; do not report bilateral capability until an upper specification exists. Maintain reaction plans for any seal below the engineering minimum or the committed level, and periodically verify the measurement system and recipe adherence.
