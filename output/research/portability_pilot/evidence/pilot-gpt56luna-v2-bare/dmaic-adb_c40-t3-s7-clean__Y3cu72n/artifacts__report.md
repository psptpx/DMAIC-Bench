# Sequencing-panel study status

## Executive conclusion

The sequencing libraries support a comparison: the QC computation found **12 usable libraries**, with **6 control** and **6 treated** libraries. The preparation design is identifiable because treatment is represented within **1 preparation batch**. The study can therefore test the planned treated-versus-control question.

The expression computation tested **400 panel genes** using **6 control** and **6 treated** libraries and produced **40 candidates** under the brief's calling rules. The candidate identifiers are:

G0339, G0370, G0215, G0062, G0045, G0055, G0108, G0125, G0153, G0284, G0327, G0372, G0165, G0244, G0314, G0341, G0214, G0387, G0038, G0366, G0173, G0267, G0239, G0265, G0379, G0112, G0060, G0241, G0156, G0169, G0002, G0271, G0005, G0333, G0100, G0263, G0210, G0019, G0247, G0237

## Validation and decision

The qPCR batch covered **10 nominated candidates**, with **0 confirmed**. The computed validation concordance was **0.0**, while the facility gate requires **0.75**. The confirmed-gene list is empty.

Because validation failed the release gate, the facility should **not issue the expression candidate list as validated findings**. The expression result is a screening result, not a validated conclusion.

## What is causing the current stop

Library quality and design are not the limiting factors: all libraries passed the usability computation, and the treatment comparison is not confounded with preparation batch. The limiting factor is lack of qPCR confirmation: none of the nominated candidates met both the direction and significance requirements.

## Annotation and next action

The steward refused the gene-set annotation request because the validation gate was not met. Consequently, no enrichment computation was run and no pathway-level conclusion can be made. The conclusion stops at the failed validation gate; no annotation result is being inferred.

Recommended next steps are to review the nomination and qPCR assay performance, repeat or expand validation for the strongest candidates, and re-evaluate the list only after a new validation computation. If validation later meets the facility gate, request the annotation batch and run enrichment then.

## Holding the improvement

Keep the library usability rules, arm-level replicate check, design-identifiability check, differential-expression computation, and qPCR concordance calculation in the analysis record. Reissue findings only when the validation computation passes the facility gate and the corresponding annotation analysis has actually been run.
