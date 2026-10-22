# Compound-response study: decision report

## Executive conclusion

The library set retains enough usable biological replication to continue to a design check, but it **cannot support the compound-versus-vehicle conclusion requested**. After QC, treatment arm and preparation batch are perfectly confounded. Consequently, the compound effect cannot be separated from a batch effect under the required model.

The gene-count batch was therefore locked at the design-identifiability gate. No valid differential-expression calculation was possible, no responsive genes can be named, and no candidate list should be issued. The qPCR and gene-set stages are downstream of that blocked analysis and likewise could not be evaluated.

## Library quality and replication

I applied both standing library-usability criteria to all **12** libraries. **4** failed overall: **2** failed the assigned-read criterion and **2** failed the mapping-rate criterion. This left **8** usable libraries, split evenly as **4** control and **4** treated libraries. The minimum retained replication in either arm was therefore **4**, so the library-replication gate passed.

This means poor library quality alone does not stop the study. Filtering did, however, determine which preparation batches remained represented within each arm.

## Design identifiability

The usable libraries span **2** preparation batches. Every usable control library is from one batch, while every usable treated library is from the other. For the required intercept-plus-batch-plus-condition design, the model matrix had **3** columns but rank **2**. It is rank deficient: the treatment indicator is indistinguishable from the batch indicator.

An unadjusted arm comparison would attribute the combined arm-and-batch difference to compound exposure and would violate the facility rule requiring batch adjustment. It is not an acceptable workaround.

## Gene response, validation, and interpretation

The steward refused release of gene-level counts because the declared design is confounded. Therefore adjusted treatment effects, adjusted significance values, fold changes, and a significant-gene count were **not computed**. The correct answer to “which genes respond?” is currently **not estimable**, not an empty result and not a negative biological finding.

Independent qPCR validation is downstream of nominated panel candidates. Because no defensible candidates could be nominated, validation concordance and confirmation count could not be computed. The validation requirement for issuing a list therefore has not been demonstrated, and the list must be withheld.

Gene-set annotation was also not released on this blocked route, so pathway enrichment could not be computed. This does not change the primary conclusion: pathway interpretation cannot repair a non-identifiable treatment contrast.

## What should happen next

Reprepare or resequence libraries so that usable control and treated samples coexist within preparation batches. A balanced blocked layout is preferable: distribute both arms across each preparation batch rather than assigning an arm to a batch. Randomize future library preparation order and preserve the arm-by-batch crossing after QC.

After replacement data are available, repeat the following release controls in order:

- reapply read-depth and mapping QC;
- confirm adequate usable replication in each arm;
- verify full rank of the batch-adjusted design matrix;
- fit the required batch-adjusted gene model and apply the prespecified call rules;
- validate the resulting nominations independently before releasing any candidate list;
- perform gene-set interpretation only after the candidate and validation gates pass.

The facility should hold the study at the design gate until these checks succeed. Existing sequencing data may remain useful for troubleshooting library preparation, but they cannot establish the compound effect.
