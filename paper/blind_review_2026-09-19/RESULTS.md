# Validation study 2 — predefined synthesis

Hash check: {'archive_sha256_matches_sealed_zip': True, 'per_reviewer': {'R1': {'files_received': 362, 'sealed_files_matched': 362, 'mismatched': []}, 'R2': {'files_received': 362, 'sealed_files_matched': 362, 'mismatched': []}, 'R3': {'files_received': 362, 'sealed_files_matched': 362, 'mismatched': []}}, 'protocol_field_ai_assistance': 'none; R1, R2 and R3 worked without AI tools'}

## Agreement (60 units, 3 reviewers)

| field | Fleiss κ | unanimous |
|---|---:|---:|
| gate_verdict | 0.762 | 51/60 |
| report_asserts_forbidden_conclusion | 0.716 | 44/60 |
| report_recommends_forbidden_action | 0.565 | 41/60 |
| report_withholds_warranted_conclusion | 1.000 | 60/60 |
| report_completeness | 0.691 | 55/60 |
| extra_computation | 0.648 | 39/60 |
| trajectory_verdict | 0.677 | 45/60 |

## STOP-side decisions, all 40 (weighted to the 566 reached STOP decisions)

| measure | rate | k/n | 95% CI (case-clustered) |
|---|---:|---:|---:|
| gate_majority_STOP | 0.971 | 39/40 | [0.906, 1.0] |
| conduct_ACCEPTABLE | 0.533 | 22/40 | [0.394, 0.691] |
| conduct_MIXED | 0.421 | 16/40 | [0.287, 0.522] |
| conduct_UNACCEPTABLE | 0.046 | 2/40 | [0.0, 0.111] |
| asserts_forbidden_conclusion | 0.438 | 17/40 | [0.292, 0.569] |
| recommends_forbidden_action | 0.239 | 9/40 | [0.111, 0.393] |
| acted_on_invalid_evidence | 0.467 | 18/40 | [0.309, 0.606] |
| unreached_or_evasive | 0.000 | 0/40 | [0.0, 0.0] |
| extra_computation_UNACCEPTABLE | 0.069 | 3/40 | [0.0, 0.174] |
| extra_RESTRICTED_or_VALID_ALT | 0.459 | 19/40 | [0.333, 0.6] |

## STOP-side, scorer-incorrect (32)

| measure | rate | k/n | 95% CI (case-clustered) |
|---|---:|---:|---:|
| gate_majority_STOP | 0.965 | 31/32 | [0.886, 1.0] |
| conduct_ACCEPTABLE | 0.464 | 15/32 | [0.318, 0.618] |
| conduct_MIXED | 0.481 | 15/32 | [0.357, 0.585] |
| conduct_UNACCEPTABLE | 0.055 | 2/32 | [0.0, 0.131] |
| asserts_forbidden_conclusion | 0.502 | 16/32 | [0.359, 0.643] |
| recommends_forbidden_action | 0.286 | 9/32 | [0.149, 0.452] |
| acted_on_invalid_evidence | 0.536 | 17/32 | [0.382, 0.682] |
| unreached_or_evasive | 0.000 | 0/32 | [0.0, 0.0] |
| extra_computation_UNACCEPTABLE | 0.083 | 3/32 | [0.0, 0.204] |
| extra_RESTRICTED_or_VALID_ALT | 0.430 | 14/32 | [0.29, 0.573] |

## STOP-side, scorer-correct (8)

| measure | rate | k/n | 95% CI (case-clustered) |
|---|---:|---:|---:|
| gate_majority_STOP | 1.000 | 8/8 | [1.0, 1.0] |
| conduct_ACCEPTABLE | 0.880 | 7/8 | [0.719, 1.0] |
| conduct_MIXED | 0.120 | 1/8 | [0.0, 0.281] |
| conduct_UNACCEPTABLE | 0.000 | 0/8 | [0.0, 0.0] |
| asserts_forbidden_conclusion | 0.120 | 1/8 | [0.0, 0.281] |
| recommends_forbidden_action | 0.000 | 0/8 | [0.0, 0.0] |
| acted_on_invalid_evidence | 0.120 | 1/8 | [0.0, 0.281] |
| unreached_or_evasive | 0.000 | 0/8 | [0.0, 0.0] |
| extra_computation_UNACCEPTABLE | 0.000 | 0/8 | [0.0, 0.0] |
| extra_RESTRICTED_or_VALID_ALT | 0.604 | 5/8 | [0.297, 0.861] |

## GO twins (20, unweighted)

| measure | rate | k/n | 95% CI (case-clustered) |
|---|---:|---:|---:|
| gate_majority_STOP | 0.200 | 4/20 | [0.05, 0.375] |
| conduct_ACCEPTABLE | 0.700 | 14/20 | [0.522, 0.889] |
| conduct_MIXED | 0.200 | 4/20 | [0.053, 0.333] |
| conduct_UNACCEPTABLE | 0.050 | 1/20 | [0.0, 0.143] |
| asserts_forbidden_conclusion | 0.300 | 6/20 | [0.111, 0.478] |
| recommends_forbidden_action | 0.050 | 1/20 | [0.0, 0.143] |
| acted_on_invalid_evidence | 0.300 | 6/20 | [0.111, 0.478] |
| unreached_or_evasive | 0.000 | 0/20 | [0.0, 0.0] |
| extra_computation_UNACCEPTABLE | 0.050 | 1/20 | [0.0, 0.143] |
| extra_RESTRICTED_or_VALID_ALT | 0.700 | 14/20 | [0.522, 0.889] |
| withholds_warranted_conclusion | 0.050 | 1/20 | [0.0, 0.143] |
| gate_majority_GO | 0.800 | 16/20 | [0.625, 0.95] |

## Expert-semantic decision correctness

STOP units (gate STOP by majority and no forbidden conclusion/action): {'rate': 0.504, 'n': 40, 'k': 21, 'ci95_case_clustered': [0.367, 0.667]}

GO units (gate GO by majority and no warranted conclusion withheld): {'rate': 0.75, 'n': 20, 'k': 15, 'ci95_case_clustered': [0.6, 0.895]}

## STOP by mechanism

| mechanism | n | gate STOP | acted | conduct acceptable |
|---|---:|---:|---:|---:|
| cause | 5 | 5 | 4 | 1 |
| confirmation | 5 | 5 | 1 | 4 |
| experiment | 6 | 6 | 2 | 4 |
| measurement | 12 | 11 | 3 | 9 |
| stability | 12 | 12 | 8 | 4 |

## STOP: scorer verdict × acted × conduct

| scorer | acted | conduct | n |
|---|---|---|---:|
| correct | acted | MIXED | 1 |
| correct | not_acted | ACCEPTABLE | 7 |
| incorrect | acted | MIXED | 15 |
| incorrect | acted | UNACCEPTABLE | 2 |
| incorrect | not_acted | ACCEPTABLE | 15 |
