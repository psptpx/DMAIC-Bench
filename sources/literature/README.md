# Literature held for the manuscript

Local copies of the works cited in `paper/iclr/references.bib`, one file per bib key, for
checking a citation against its source. `index.json` maps every bib key to its file, its
origin, and the manuscript claims (`cited_by`, ids from
`output/research/claim_audit_20260926/claims_input.json`) that cite it.

Layout:

- `<bibkey>.pdf`: the source document. 76 of the 77 cited works are held as PDF; the NIST handbook, a web resource, is held as section text.
- `txt/<bibkey>.txt`: text extracted from the PDF with page markers `<<pN>>`, or, for
  works whose PDF could not be obtained, the open-access full text (Europe PMC XML, NIST
  handbook sections). Only the NIST handbook is text-only.
- Every cited work is held as PDF or text. The two Montgomery textbooks are cited in the editions held
  (ISQC 8th ed. 2020, DAOE 8th ed. 2013).
- `aiag1995spc.pdf` is an archival copy of the 1992/1995 AIAG SPC reference manual; it is
  not cited.

The PDFs and extracted texts are git-ignored: several are licensed standards or
subscription articles and must not be redistributed, and the anonymised review release
is built from the tracked tree. Only this README and `index.json` are tracked.

Regenerate `index.json` after adding a file by editing it directly; the audit records in
`output/research/claim_audit_20260926/merged_results.json` hold the per-claim verdicts.
