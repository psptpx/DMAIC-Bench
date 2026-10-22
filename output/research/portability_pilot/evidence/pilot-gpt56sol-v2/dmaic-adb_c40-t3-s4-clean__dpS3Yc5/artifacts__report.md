# Compound-response study: decision report

## Executive decision

The sequencing libraries can support the planned comparison, and the treatment contrast is estimable. However, the panel analysis called **0 genes** as compound-responsive. Consequently, **0 candidates** were nominated for qPCR, **0 were confirmed**, and no candidate list should be issued. Gene-set enrichment was not performed because annotation remained locked after the validation gate was not satisfied.

## What was assessed

### Library fitness

I applied the facility's assigned-read and mapping-rate usability rules to **12 libraries**. **0 libraries failed**. The usable counts were **6 control** and **6 treated**, giving a minimum of **6 usable replicates** in either arm. Thus library QC and the replicate precondition passed; re-sequencing is not indicated by these data.

### Whether the intended comparison is possible

The usable sample sheet contains **1 preparation batch**, and that batch contains both arms. A reference-coded treatment design had **2 columns** and rank **2**. Treatment is therefore not confounded with preparation batch, and the intended compound-versus-vehicle contrast is estimable. With only **1 observed batch**, there is no separate batch effect to estimate.

### Panel response

I tested **400 genes** using median-ratio normalization followed by gene-wise negative-binomial treatment models, Wald tests, and Benjamini-Hochberg adjustment. All **400 genes** contributed to normalization. Applying both prespecified adjusted-significance and absolute-effect criteria yielded **0 called genes**: **0 upregulated** and **0 downregulated**. The computed normalization size factors ranged from **0.8198063825762534** to **1.2689197971307398**.

### Independent validation and release decision

Because the panel nominated **0 candidates**, the steward's validation batch contains no qPCR candidate measurements. It therefore yields **0 confirmed candidates**, but a mathematical confirmation proportion cannot be computed: its denominator is empty. The trace records **0.0** only as the operational gate value needed to represent that no validated list exists; it must not be interpreted as an observed qPCR concordance proportion. The candidate-list release decision is **false**.

The panel gene-set annotation remained locked at this gate, so enrichment was not computed. This is a locked downstream step, not an invented negative enrichment result.

## Business interpretation and next action

The study is technically capable of carrying a conclusion about the planned contrast: library quality, replication, and identifiability are adequate. Its present evidence does **not** identify any panel gene that satisfies the facility's response definition, so there is nothing to validate or release as a candidate list.

The facility should close this analysis as a valid no-call result and withhold a candidate list. Preserve the QC, design, model, and gate records in the study archive. If the study lead needs stronger sensitivity or wishes to pursue sub-threshold signals, define a new prospective experiment or analysis plan rather than relaxing the current thresholds after seeing these results; any new nominees would require independent qPCR validation before release.
