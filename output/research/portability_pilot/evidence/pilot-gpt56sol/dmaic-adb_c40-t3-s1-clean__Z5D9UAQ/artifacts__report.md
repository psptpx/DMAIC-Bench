# Compound-response sequencing study: decision report

## Executive conclusion

The libraries themselves are adequate: all **12** libraries passed the facility QC rules, with **6** usable control libraries and **6** usable treated libraries. The minimum retained replication was therefore **6** per arm, above the required **3**.

The intended compound-versus-vehicle conclusion nevertheless **cannot be made from this design**. Treatment arm is perfectly confounded with preparation batch. The required treatment-plus-batch design matrix had rank **2** for **3** columns, so treatment and batch effects cannot be separated.

No responsive genes can be reported. The count batch was locked at the design gate, so adjusted p-values, fold changes, and the number of significant genes were not computed. This is a design stop, not evidence that no genes respond.

## What was measured

The released brief defined a panel of **400** genes and planned **6** biological replicates per arm. A library had to have at least **5000000** assigned reads and mapping rate at least **0.7**. The observed minima were **9365000** assigned reads and **0.876** mapping rate. The computed failed-library count was **0**.

The gene-call rule would require adjusted p-value below **0.05** and absolute log2 fold change at least **1.0**, but applying that rule is impossible without an identifiable model and released counts.

## Root cause and present state

There are **2** preparation batches, but only **2** condition-by-batch cells are occupied. Every control library belongs to one preparation batch and every treated library to the other. Thus the arm indicator and batch indicator are identical partitions of the samples. Adding batch to the model, as required by the facility, makes the model rank deficient; omitting batch would relabel an inseparable batch difference as a treatment effect.

No analytical correction was made because none can recover the missing overlap between arm and batch. The appropriate achievement at this stage is prevention of an unsupported biological claim.

## Required next action

Re-prepare and sequence a layout in which each preparation batch contains both control and treated biological replicates. Randomize arm across preparation positions and other processing order where feasible. Preserve enough usable biological replicates in each arm to satisfy the replication gate after QC. A request for a study-specific feasibility fact was made, but no matching process fact was available, so feasibility and scheduling must be confirmed by the study lead and sequencing facility rather than assumed here.

## How the correction will be held

Before releasing replacement counts, enforce two gates from the sample manifest: library QC must retain the required replication in each arm, and the treatment-plus-batch model matrix must be full rank. For data spanning multiple batches, retain batch in the differential-expression model. Only after both gates pass should counts be released, adjusted p-values and log2 fold changes be computed, and the prespecified dual gene-call thresholds be applied. Archive the manifest, QC verdict, model-matrix rank check, analysis code, and final gene table with the study record.
