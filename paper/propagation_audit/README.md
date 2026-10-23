# Exploratory post-fork propagation audit

These files accompany the appendix subsection **Exploratory post-fork result
propagation audit**. They contain a single Codex-assisted annotation pass informed
by the existing expert reviews. **No new independent human adjudication has been
performed.** The original expert labels and population estimates are unchanged.

- `propagation_audit_labels.csv`: all 40 frozen no-go units, eligibility, labels,
  result links, original acted labels and retained sampling weights.
- `propagation_audit_evidence.json`: source trace records, verbatim report
  passages, result-specific links, raw-count summary and the 280 verified frozen
  packet-file hashes. Source paths are relative to the research repository.
- `propagation_audit_methods.md`: definitions, eligibility decisions, limitations
  and metric denominators. `QUARANTINED` denotes restricted description or a valid
  alternative; it does not imply absence of textual reuse.

The summary is descriptive of the sampled units. Of 30 candidate-computation
units, 25 contain confirmed cross-section reuse. Among 14 candidate units not
originally labeled acted, 11 contain such reuse: 10 preserve the restriction and
one remains unresolved. Reuse is not a contamination rate. All 15 explicit
reliance labels overlap the original acted judgments; these are not 15 new errors.

To reproduce in the research repository, run from its root:

```sh
python3 output/research/propagation_audit_20260922/summarize.py
python3 output/research/propagation_audit_20260922/export_paper_support.py
```

The first command validates the frozen evidence hashes and aggregates the fixed
annotations; it is not an independent classifier. Full packets, the annotation
revision history and blank independent-review sheets remain in the research
repository. This compact Overleaf bundle contains selected evidence and hashes,
not all source packets. Blind IDs do not imply that this new annotation pass was
blind to prior study information.
