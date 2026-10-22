# Study disposition

## Executive conclusion

The sequencing libraries pass facility QC, but the study cannot support the intended compound-versus-control conclusion. Treatment arm is perfectly confounded with preparation batch. A compound effect therefore cannot be distinguished from a batch effect.

The gene-level count batch was not released after this failed design gate. No differential-expression result was computed, no responding genes can be named, and no candidate list should be issued. The downstream qPCR data were consequently unavailable, so validation concordance and the number confirmed could not be computed.

## Library QC

I applied the brief's usability cutoffs of **5,000,000** assigned reads and **0.7** mapping rate to **12** libraries. **0** libraries failed. The control and treated arms each retained **6** usable libraries, making the minimum retained arm count **6**, above the required **3**. Library quality and replicate retention therefore are not the reasons this study stops.

## Design assessment

The usable libraries occupy **2** preparation batches, but allocation is completely separated by arm: **6** controls and **0** treated libraries are in one batch, while **0** controls and **6** treated libraries are in the other. For a model containing an intercept, treatment, and batch, the design matrix rank is **2** for **3** columns. The model is not full rank, and a treatment coefficient adjusted for batch is not estimable.

A simple arm-only comparison would combine the compound effect with the preparation-batch effect. It would not answer the study question and was not used as a substitute.

## Expression and validation status

The steward locked gene-level counts because the design-identifiability condition failed. The number of significant genes could not be computed, and there is no defensible list of compound-responsive genes.

Because count analysis and nomination could not occur, the qPCR validation batch was also unavailable. Concordance and confirmation could not be computed. This is a hard stop: the candidate list is withheld rather than treating unavailable validation as success or failure.

## Cause, correction, and control

The cause is experimental allocation, not sequencing quality: arm and preparation batch encode the same split. No analytical adjustment can recover two separate effects from this layout.

The facility should prepare and sequence additional material with control and treated libraries represented within each preparation batch. After obtaining a crossed allocation, it should repeat library QC, verify that the treatment-plus-batch model is full rank, fit the batch-adjusted expression model, apply the prespecified gene-call rules, and then perform independent qPCR validation before issuing any list.

To hold the correction, the sample-sheet review should become a pre-sequencing release gate: both arms must be represented across preparation batches, model-matrix identifiability must be checked before count analysis, and candidate-list release must remain blocked until independent validation satisfies the facility rule.
