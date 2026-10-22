# Case-control candidate-panel report

## Executive conclusion
The plate can carry a conclusion: the computed discovery sample-failure fraction was 0.0125, below the protocol ceiling of 0.1. After discovery QC, 139 variants were retained. The discovery scan nominated rs070008, but the independent replication does not support reporting it under the protocol because its replication p-value was 0.5374794553122432, which is not below 0.05, even though its direction was the same as discovery.

## Protocol and data
The protocol set participant and variant call-rate thresholds at 0.95, MAF at 0.01, control HWE p at 1e-6, a plate failure ceiling of 0.1, Bonferroni-corrected 0.05 for discovery, and replication p < 0.05 with the same direction. The discovery batch contained 240 participants and 150 panel variants; the replication batch contained 120 participants and 1 nominated candidate.

## Discovery QC and comparison
3 discovery participants failed the participant call-rate rule, leaving 237 participant records meeting it. The fraction failing was 0.0125, so the plate passed the protocol ceiling. Variant QC retained 139 variants and excluded 11. The retained set was: rs070001, rs070002, rs070003, rs070004, rs070005, rs070006, rs070007, rs070008, rs070009, rs070010, rs070011, rs070012, rs070014, rs070015, rs070016, rs070017, rs070018, rs070019, rs070020, rs070021, rs070022, rs070024, rs070026, rs070027, rs070028, rs070029, rs070030, rs070031, rs070032, rs070033, rs070034, rs070035, rs070036, rs070037, rs070038, rs070039, rs070040, rs070041, rs070042, rs070043, rs070044, rs070045, rs070046, rs070048, rs070050, rs070051, rs070052, rs070053, rs070054, rs070055, rs070056, rs070057, rs070058, rs070059, rs070060, rs070061, rs070062, rs070063, rs070064, rs070065, rs070066, rs070067, rs070068, rs070070, rs070071, rs070072, rs070073, rs070074, rs070075, rs070076, rs070077, rs070078, rs070079, rs070080, rs070081, rs070082, rs070083, rs070084, rs070085, rs070086, rs070087, rs070088, rs070089, rs070090, rs070091, rs070092, rs070093, rs070094, rs070095, rs070096, rs070097, rs070098, rs070100, rs070101, rs070102, rs070103, rs070104, rs070105, rs070106, rs070107, rs070108, rs070109, rs070110, rs070111, rs070112, rs070113, rs070115, rs070116, rs070117, rs070118, rs070119, rs070120, rs070121, rs070122, rs070123, rs070124, rs070125, rs070126, rs070127, rs070128, rs070129, rs070130, rs070132, rs070134, rs070135, rs070136, rs070137, rs070138, rs070139, rs070140, rs070141, rs070142, rs070143, rs070144, rs070145, rs070146, rs070147, rs070149, rs070150.

The affected and unaffected groups were available for comparison, with 120 affected and 120 unaffected participants. The discovery association analysis found 1 Bonferroni-significant variant at threshold 0.00035971223021582735: rs070008. Its odds ratio was 2.403020306872863, in the risk direction. The genomic-control lambda estimate was 0.9141523793512716.

## Replication
In replication, 0 participants failed the 0.95 call-rate rule, a fraction of 0.0. The nominated rs070008 candidate had call rate 0.9916666666666667. Its replication association p-value was 0.5374794553122432, and the direction matched discovery. However, 0 candidate replicated under the prespecified rule, so the discovery signal is not supported for reporting as replicated.

## What changed, what it achieved, and control
The analysis applied the steward-provided QC filters before discovery testing, used the retained-variant Bonferroni threshold, nominated only the resulting discovery hit, and then tested that hit once in the independent cohort. This achieved a QC-qualified discovery result but no protocol-qualified replicated finding. The result should be held by preserving the steward batches, the analysis scripts, the computed result JSON files, and this trace; any future conclusion should use the same thresholds and require an independent cohort to meet both replication conditions.

## Next action
Do not report rs070008 as a replicated association. Treat it as a discovery-only lead and seek additional independent data or a new prespecified replication analysis before making a confirmatory claim.
