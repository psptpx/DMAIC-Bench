# Discovery plate decision

## Executive conclusion

The current discovery plate cannot support a genetic-association conclusion. Participant quality control found **31 failed samples among 240**, a failure fraction of **0.12916666666666668**. The protocol permits at most **0.1**, so the plate fails its mandatory viability gate and must be re-genotyped before anything downstream is analyzed.

This is a plate-level stop, not evidence for or against association. Affected and unaffected participants cannot validly be compared using this plate. No variant association can be declared, and replication support cannot be assessed because there are no protocol-valid discovery candidates to nominate.

## Participant quality control

The participant screen used the protocol call-rate threshold of **0.95** across **150** panel variants. It produced:

- failed participants: **31**;
- participants passing the individual screen provisionally: **209**;
- observed failure fraction: **0.12916666666666668**;
- minimum observed participant call rate: **0.5066666666666667**;
- plate acceptance result: **false**.

The failed participant identifiers are:

`P004`, `P005`, `P022`, `P028`, `P035`, `P036`, `P051`, `P057`, `P060`, `P062`, `P067`, `P071`, `P077`, `P092`, `P102`, `P103`, `P120`, `P123`, `P126`, `P128`, `P130`, `P136`, `P139`, `P146`, `P153`, `P156`, `P162`, `P211`, `P217`, `P229`, and `P240`.

The **209** other participants passed the individual call-rate screen, but they are only provisional passers. The plate-level rule prevents treating them as an analysis cohort until re-genotyping resolves the excess failures.

## Variant retention and cohort comparability

Variant quality control was not run. Consequently:

- no variants have been validly retained or excluded under the variant call-rate, minor-allele-frequency, and unaffected-participant Hardy-Weinberg rules;
- ancestry structure was not computed;
- whether affected and unaffected participants overlap ancestrally could not be established;
- no decision about principal-component covariate adjustment could be made.

An initial attempt to prepare the ancestry calculation failed because an optional PCA library was absent, but this had no effect on the conclusion: after replacing that dependency, the rerun reached the participant gate and stopped as the protocol requires. No ancestry result is claimed.

## Association and replication status

Association testing was not permitted. Therefore the number of discovery associations, genomic inflation, effect estimates, and nominated variants could not be computed. The independent replication cohort was deliberately not requested or tested because a failed discovery plate cannot generate valid candidates. Replication neither supports nor refutes any variant at this stage.

## Required next action and control plan

Re-genotype the complete discovery plate and restart the analysis from participant call-rate quality control. Do not carry the provisional participant set or any unvalidated variant result forward. Once a replacement plate passes the participant-failure gate, apply variant quality control, establish ancestry comparability before testing, include leading ancestry axes if overlapping structure is present, apply the protocol's panel-wide correction, and send only valid discovery hits to the independent same-direction replication check.

Retain the participant-failure gate as a hard automated stop in the rerun so that variant testing cannot execute when `plateAcceptable` is **false**.
