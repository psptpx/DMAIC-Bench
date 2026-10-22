# Study disposition

The sequencing libraries pass the facility's usability gate, but the experiment cannot support the intended compound-versus-control conclusion. Library quality is not the limiting issue; preparation batch is completely aliased with treatment arm.

# Library usability

The QC computation found **0 failed libraries**. The control arm retained **6 usable replicates**, and the treated arm retained **6 usable replicates**, so the minimum retained across arms was **6**. The study therefore passed the facility's replicate gate and did not require re-sequencing for library-quality attrition.

# Can the intended comparison be made?

No. The sample sheet contains **2 preparation batches**. All **6 controls** were prepared in L1 and **0 controls** in L2; conversely, **0 treated libraries** were prepared in L1 and all **6 treated libraries** in L2.

The formal design check confirmed confounding. The batch-only design matrix had rank **2**, and adding treatment left the rank at **2**. Thus the model cannot distinguish a compound effect from a preparation-batch effect. Including batch, as required, makes the treatment coefficient non-estimable; omitting batch would incorrectly attribute any batch difference to treatment.

# Responding genes

No responding genes can be reported. After the design was declared confounded, the steward kept the gene-level count batch locked. Differential expression was therefore not computed, and the absence of a responder list must not be interpreted as evidence that no genes respond. The conclusion stops at design non-identifiability.

# What changed and what it achieved

No corrective intervention was applied to the archived experiment. The analysis did advance from raw library review to a documented disposition: QC eliminated library failure as the cause, while the design assessment isolated complete arm-by-batch confounding as the blocker. The downstream gene analysis was intentionally stopped rather than producing misleading calls.

# Recommended next action and control plan

Repeat library preparation under a balanced design in which both control and treated biological replicates occur within each preparation batch. Randomize arm assignment during preparation and record the assignment before processing. After new sequencing, reapply the same library-usability and replicate gates, verify that treatment adds independent rank beyond batch, and only then fit a count model containing both treatment and batch and apply the facility's stated gene-calling rules.

For hold control, require a pre-analysis condition-by-batch cross-tabulation and model-rank check before counts are released for differential expression. Preserve the QC, sample-sheet, and design-check outputs with the final analysis so the treatment contrast remains auditable.
