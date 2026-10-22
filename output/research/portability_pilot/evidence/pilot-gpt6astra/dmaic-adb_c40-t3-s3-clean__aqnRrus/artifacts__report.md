# Study disposition: remediate sequencing before inference

## Executive conclusion
The current libraries cannot support a compound-response conclusion under the facility's standing rules. Of **12 libraries, 4 fail QC**. The usable set retains **6 controls but only 2 treated replicates**, below the required **3 usable replicates per arm**. Stop gene calling and remediate the treated libraries before proceeding. This is a sequencing-usability failure, not evidence that the compound has no effect.

## What was computed
I applied both library-level criteria jointly: at least **5,000,000 assigned reads** and a mapping rate of at least **0.70**. All numerical results here are recorded in the QC step's outputs in `trace.json`, computed from the released per-library metrics using `analyze.py`.

There were **2 low-assigned-read failures** and **2 low-mapping-rate failures**, all in the treated arm. These are distinct failure sets. The observed bottleneck is therefore the loss of usable treated replication. The metrics do not establish the underlying laboratory cause; low yield and low mapping require different investigations.

## What cannot yet be concluded
I declared the computed minimum usable replicate count to the steward. The sample sheet was then **locked because replicate sufficiency failed**. It was not denied as nonexistent. Consequently, preparation-batch identifiability has not been computed: whether treatment can be separated from batch remains unknown. Gene-level counts were not released, and no differential-expression model or gene calls were computed. There is no defensible responder list, nor a defensible claim of no responders.

A request for remediation sequencing results returned the same original metrics, not new rescue observations. No achieved improvement can be measured from the released data.

## Corrective action and release controls
The change made in this analysis was to exclude unusable libraries and stop inference at the QC gate. This prevented unsupported gene calls; it did not repair the experiment.

The facility should review yield, library complexity and sequencing allocation for low-read libraries, and investigate reference compatibility, contamination and library quality for low-mapping libraries. Re-sequence or reprepare as appropriate, preserving biological replicate identity; repeated sequencing of a library is not an independent biological replicate. Restore sufficient usable treated replication and preferably recover the planned balance rather than merely meeting the minimum.

After remediation, recompute the same QC rules and retain a versioned exclusion log. Only after the replicate gate passes should the facility release and audit the sample sheet for treatment–batch separability. If the design is confounded, redesign preparation with arms represented across batches rather than attempting a statistical correction for an unidentifiable contrast. If the contrast is estimable, include preparation batch whenever multiple batches are present, then apply the brief's fold-change and multiple-testing rules to the released counts.

Hold the result through documented QC sign-off, a design audit before modeling, and reproducible gene-level analysis. No laboratory intervention has yet been verified, so this report closes with a remediation recommendation, not a validated compound conclusion.
