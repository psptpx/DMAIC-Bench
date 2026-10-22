# Compound-expression study: decision report

## Executive decision

The sequencing libraries can carry the planned comparison: all **12** libraries passed the prespecified usability rules, leaving **6** usable control replicates and **6** usable treated replicates. The arm comparison is identifiable because both conditions were prepared in the same **1** batch; treatment is not separated from batch. A distinct batch effect cannot be estimated.

The panel analysis tested **400** genes and called **0** genes at adjusted *p* below **0.05** together with absolute log2 fold change of at least **1.0**. The facility should therefore issue **no compound-responsive gene list** from this experiment. This is a prespecified null call, not proof that every biological effect is exactly absent.

Independent validation cannot support a gene list: **0** candidates were nominated, **0** qPCR records exist, and **0** candidates were confirmed. Concordance is undefined rather than zero because there is no denominator. It was not imputed, and the required concordance of **0.75** cannot be assessed.

## What was measured and what it means

### Library readiness

Usability required at least **5000000** assigned reads and mapping rate at least **0.70**. There were **0** failed libraries. The minimum retained replication in either arm was **6**, against a required minimum of **3**. Thus no library exclusion changed the planned arm sizes, and sample adequacy does not stop the study.

### Design validity

The usable sample sheet contains **2** conditions and **1** preparation batch across **12** usable samples. Both conditions occur within that batch. Consequently, the treated-versus-control contrast can be made without treatment–batch confounding. Because only **1** batch exists, this study cannot quantify reproducibility across preparation batches or estimate a separate batch variance.

### Expression result

Counts were normalized by median-of-ratios size factors. For each of **400** genes, a two-sided Welch comparison was run on log2 normalized abundance, followed by Benjamini–Hochberg correction across the panel. A call required both adjusted *p* below **0.05** and absolute log2 fold change at least **1.0**. Exactly **0** genes met both requirements, so there are no gene names to report as responders.

### Validation and annotation boundary

The released validation batch explicitly contains **0** nominees and **0** qPCR measurements. Confirmation required directional agreement at *p* below **0.05**, but no candidate could be scored. The concordance calculation is therefore undefined, and its **0.75** release criterion cannot be evaluated. The gene-set annotation remained locked behind that numeric criterion; no annotation data were released and no enrichment analysis was performed. Nothing was guessed to bridge this gap. This missing downstream step does not create a responder list where the panel analysis found none.

## Recommended next actions and control plan

1. Do not issue a compound-responsive gene list from the current panel.
2. Do not describe the empty qPCR batch as successful validation; record validation as not applicable because there were no nominees.
3. If a positive candidate list is operationally required, plan a new, prospectively powered experiment rather than relaxing the current thresholds after seeing the data. Include more than **1** preparation batch with both conditions represented within each batch so that batch robustness can be estimated.
4. For the next run, retain the same pre-release controls: library QC, at least **3** usable replicates per arm, explicit condition-by-batch identifiability, multiplicity-adjusted panel testing, and directional qPCR confirmation before release.
5. Amend the facility procedure to define how validation concordance and downstream annotation are handled when the nominee count is **0**. Until that rule exists, preserve the result as undefined rather than assigning a passing value.
