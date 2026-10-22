# Compound expression study: PI decision

## Bottom line
The libraries and design support a treatment comparison. The panel analysis calls 39 genes, and independent qPCR confirms all 10 nominated candidates. Concordance is 1.00, exceeding the facility gate of 0.75. Issue the nominated, independently supported candidate list; distinguish it from the broader panel-only discovery list. These results support expression responses, not a claim of therapeutic efficacy or mechanism.

## Library quality and design
All 12 libraries pass: 0 fail the joint assigned-read and mapping rules. The computed pass rule uses assigned reads at least 5,000,000 and mapping rate at least 0.70. Each arm retains 6 usable replicates against a requirement of 3. No exclusions or resequencing are needed on these metrics.

The usable libraries occupy 1 preparation batch, containing both arms. The treatment design has rank 2 for 2 columns. Treatment is not confounded with preparation batch. A redundant constant batch term was not fitted; a between-batch variance fraction cannot be estimated in this design. Randomization and other potential confounders were not established by the supplied sheet.

## Panel analysis
All 400 panel genes were tested. I used median-of-ratios library normalization, log-base-two normalized counts with pseudocount 1, independent two-sided Welch tests, and Benjamini–Hochberg correction across the panel. Calls require adjusted p < 0.05 and absolute log-base-two effect >= 1.0. Effects are differences in mean transformed expression, not fitted negative-binomial coefficients. This is an exploratory log-scale analysis; a count-aware, dispersion-moderated sensitivity analysis should precede publication, especially for borderline calls. Normalization assumes most panel genes are stable and does not establish absolute global expression changes.

### Panel-responsive genes
These are discovery calls; only the nominated subset below has independent validation.

|Gene|Log-base-two effect|BH adjusted p|
|---|---:|---:|
|G0006|1.9872|0.00251173|
|G0007|1.4759|0.00972368|
|G0010|2.0965|0.000436405|
|G0037|1.6527|0.000302091|
|G0039|2.2193|0.00222985|
|G0052|-2.1467|0.000170353|
|G0061|2.4538|0.000123846|
|G0101|2.0832|9.91648e-05|
|G0107|1.8814|0.000261721|
|G0110|2.0384|0.000125673|
|G0114|-1.3805|0.000516081|
|G0115|-2.1952|5.78786e-05|
|G0118|2.0162|0.00149903|
|G0124|-2.3894|0.000179529|
|G0131|2.5321|7.46051e-05|
|G0149|-1.4079|0.0116593|
|G0153|1.8747|0.000349559|
|G0154|-2.3309|0.000478354|
|G0155|-1.7906|0.00730432|
|G0187|-2.4663|0.000170353|
|G0194|1.9916|0.000101724|
|G0212|1.4535|0.00375706|
|G0247|-2.3326|7.46051e-05|
|G0260|1.9499|0.000701775|
|G0276|-2.4610|0.000181026|
|G0277|3.0078|7.46051e-05|
|G0279|2.1448|7.46051e-05|
|G0280|-1.6525|0.0018552|
|G0287|2.1640|7.46051e-05|
|G0293|2.2188|0.0011138|
|G0299|-2.8670|0.000122656|
|G0310|2.2098|0.000155153|
|G0311|-2.4575|0.00522944|
|G0314|-2.6218|9.91648e-05|
|G0331|2.4549|0.000563829|
|G0372|-2.1405|0.0233887|
|G0374|1.9381|0.00311027|
|G0383|1.3345|0.00745304|
|G0394|-1.3021|0.00559529|

## Independent validation
Two-sided Welch tests on the supplied independent qPCR expression measurements were combined with agreement with the computed panel direction. The facility uses nominal p < 0.05 for this gate, not multiplicity-adjusted validation p. The nominated subset confirms as follows:

|Gene|qPCR effect|p value|Confirmed|
|---|---:|---:|---|
|G0299|-1.9305|0.000221657|Yes|
|G0277|2.9565|5.5518e-05|Yes|
|G0314|-1.5515|0.00023871|Yes|
|G0311|-2.0188|0.000442734|Yes|
|G0276|-1.7477|4.79963e-05|Yes|
|G0187|-1.6000|0.000395465|Yes|
|G0124|-1.6353|0.000587964|Yes|
|G0154|-2.0038|0.000101102|Yes|
|G0247|-2.1048|7.23749e-05|Yes|
|G0115|-2.0773|1.91451e-06|Yes|

Confirmation covers 10 of 10 nominated genes, not every discovery call. No missing data batch was denied. The complete gene-level results and validation results are preserved in the accompanying CSV files.

## Biological context
Panel-background upper-tail hypergeometric tests, BH-corrected across 12 supplied sets, find 1 significant sets at adjusted p < 0.05. The background is the 400 tested panel genes, not the genome. The annotation provides generic set identifiers, so a named biological mechanism cannot be inferred.

|Set|Discovery overlap|Set size|BH adjusted p|
|---|---:|---:|---:|
|SET01|5|30|0.372448|
|SET02|2|30|0.815874|
|SET03|20|30|5.44133e-15|
|SET04|5|30|0.372448|
|SET05|4|30|0.499763|
|SET06|6|30|0.235104|
|SET07|3|30|0.694261|
|SET08|2|30|0.815874|
|SET09|3|30|0.694261|
|SET10|4|30|0.499763|
|SET11|6|30|0.235104|
|SET12|4|30|0.499763|

## Action and control plan
No experimental rescue or process change was made. The analytical changes were library normalization, multiplicity control, and independent directional validation; they convert raw differences into a qualified, independently supported candidate list. There is no measured before-and-after process improvement to claim.

Release the confirmed nominated candidates with their directions and uncertainty, and label other panel calls as discovery-only. Before downstream investment, review assay specificity, sample identity, randomization and potential non-batch confounding; rerun a count-aware sensitivity analysis and extend independent validation to additional candidates. Do not infer a genome-wide pathway effect from this targeted panel.

Hold the result through a frozen sample sheet, versioned analysis scripts, retained raw counts and qPCR records, and a documented sign-off of the same QC, estimability, multiplicity and concordance gates. Future experiments should randomize both arms within each preparation batch and include batch in the model whenever multiple batches occur. Track library failures and validation concordance prospectively rather than assuming this study establishes long-term process capability.
