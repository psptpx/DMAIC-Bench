# Compound-response study report

## Executive conclusion

The sequencing libraries can support a conclusion: all **12** libraries passed the facility usability rules, with **0** failures. The control arm retained **6** usable libraries and the treated arm retained **6**, so the minimum retained replication was **6**.

The intended comparison is estimable. There was **1** preparation batch, and it contained **6** control and **6** treated libraries. The design was not confounded: its rank increased from **1** without treatment to **2** with treatment.

The differential-expression analysis tested **400** genes. At adjusted p-value **0.05** and absolute log2 fold-change **1.0**, **0** genes met both requirements; consequently there were **0** called increases and **0** called decreases. The study therefore provides no gene-level evidence, under the prespecified rule, that the compound changes expression on this panel.

## What was done

Library usability was computed from the supplied assigned-read and mapping-rate records using the facility brief. No library was removed. The sample sheet was then checked for treatment/batch identifiability. Because the experiment used a single preparation batch containing both arms, a simple treatment model was used rather than adding a redundant batch term.

Counts were normalized with median-ratio size factors, whose observed range was **0.8198063825762534** to **1.2689197971307398**. Each gene was fit with a negative-binomial generalized linear model containing treatment, with a normalization offset and gene-wise dispersion; Wald p-values were adjusted over the full panel by the Benjamini–Hochberg procedure. Calls required both prespecified cutoffs.

## Business interpretation

Where the study stands: library quality and replication are adequate, and the planned treatment contrast is supported by the design. The absence of called genes is an analysis result, not a QC or confounding failure. It does not prove that every biological effect is exactly zero; it says none cleared both prespecified evidence and effect-size requirements in these data.

What caused the disposition: no quality attrition occurred and no preparation-batch separation blocked the contrast. The final disposition is driven solely by the gene-level statistical and effect-size criteria.

What changed and what it achieved: no corrective intervention or data alteration was made. Normalization and multiplicity adjustment were analytical controls rather than changes to the experiment; after those controls, the called set remained empty.

## Recommended next actions and control plan

Do not nominate a responder gene from this run. Archive the sample-level QC verdict, sample sheet, model specification, complete gene-level results, and software script together so the decision is reproducible. For future runs, retain the same pre-analysis gates: apply library QC before modeling, verify that each arm retains the required replication, and verify treatment/batch estimability before releasing a gene list. If stronger sensitivity is scientifically necessary, plan a new powered experiment or independent validation rather than relaxing thresholds after seeing these results; keep both arms represented within every preparation batch.
