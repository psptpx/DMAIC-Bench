# Limitations

Paper-table references below describe the separately distributed manuscript;
they are not files bundled in this code repository. See [Publication](PUBLICATION.md)
and [Reproducing results](REPRODUCING_RESULTS.md).

What this benchmark and the measurements in this repository cannot support. Every item is a
limit of the current corpus (v2, `adb_c25` to `adb_c39`, 15 cases, 97 tasks) and of the
campaigns run on it: 13 systems from six providers, three complete attempts per task under the
plain instruction, plus the permit-stop, permit-paraphrase, normative and remind instruction
conditions on the 32 paired control tasks (`paper/iclr/tab_control.tex`,
`paper/iclr/tab_ctlrep.tex`). The v1 corpus this file once described is retired.

## Of the measurement

**Thirteen systems, one harness.** Enough to show that the restraint gap belongs to the task and
not to one vendor: among the eleven frontier systems, no-go accuracy stays between 16% and 25%
while mean reward spans 12 points, and the two Qwen systems are lower on both sides. It is not a
leaderboard, and the paper makes no ranking claim. Case-clustered intervals on adjacent pairs
are in `paper/iclr/tab_boot.tex`.

**Three attempts per task.** Every system has three complete attempts; the spread over attempts
is at most 0.027 in mean reward and 5.1 points in no-go accuracy. Three attempts bound the
run-to-run variance, they do not estimate it precisely, and every pass^3 statement in
`RESULT_PASSK.md` rests on three draws.

**Failures are correlated across systems.** The corpus measures one dimension far better than it
measures thirteen. On the 18 B-divert tasks, six routes were correct out of 234 attempts across
all systems: what a system gets wrong there, every system gets wrong. A leaderboard over many
systems would rest on the minority of tasks that separate them.

**No human-run baseline on this corpus.** Human black belts did not run the 97 tasks. The human
row in the README is the blind expert reading of 60 forks in the second review study (39 of 40
no-go labels confirmed, 16 of 20 go twins), which fixes what the correct action was and whether
the report acted against it. It is not a human score on the tasks. `archive/HUMAN_BASELINE.md`
anchors one narrow question on a different corpus of project reports.

**Instruction controls on two systems.** The replicated control (five conditions, three
attempts, 960 trials) was run on GPT-6-astra and DeepSeek-v4-pro only. The permit-stop
comparison in `paper/iclr/tab_control.tex` covers all thirteen systems; the paraphrase,
normative and remind conditions do not.

## Of the corpus

**15 cases.** Eight extracted from real black-belt closure reports, seven self-authored. The
industrial provenance is what supplied the stop decisions; it also means the corpus is small,
and its industry mix (four groups: discrete manufacturing, electronics, process industry,
services) is not a census of anything.

**The held-out half is easier.** Drawn on structural criteria with a published seed and not
re-drawn: on the two systems measured at the time of the draw, the 32 held-out tasks scored
0.026 and 0.063 higher than the 65 public ones (`HELD_OUT_V2.md`). A held-out figure is
optimistic by about that margin. No campaign here is a held-out result: all thirteen systems ran
over all 97 tasks before publication.

**English only.** English is the canonical case language and the default build language. Some
cases were migrated from earlier Chinese authoring, and some case structures draw on
Chinese-language project reports; English canonical text does not change that provenance. No
maintained Chinese arm ships. A future Chinese extension would require separate versioning,
validation and experimental evidence.

**Synthetic data.** Every batch regenerates from a seed. Real process data has structure a
generator does not (autocorrelation, missingness, transcription error), and a system that
handles generated data may not handle a plant's.

## Of the scoring

**The gate term never fires.** `gate_hard_passed` is 1 for every trial of every campaign
because the steward makes protocol violation impossible rather than penalising it. That is the
right design for the data, and it means the axis carries no information about any system. It is
reported as an integrity statement, not a score.

**Branch inference reads behaviour, not intent.** A fork's node key is private, so the scorer
infers which branch was taken from which analyses ran. A system that took the correct branch
and then, for its own reasons, also ran an analysis that belongs to the wrong one is scored as
having taken the wrong one. This is deliberate, since running the inadmissible analysis is the
error, but it means the scorer cannot distinguish a wrong turn from a right turn followed by
curiosity.

**The route metric is an upper bound on acting on invalid evidence.** A wrong route shows that
the disqualifying analysis was run; whether the report then asserted a conclusion the evidence
forbade is a separate question, answered here only by the expert reading of a 60-fork sample
(47% of no-go-side reports acted on the invalid evidence, 95% interval 31 to 61). No automatic
report reader has been validated.

**Nine scoring defects were found in this project, each of which produced publishable-looking
numbers before it was caught** (`SCORING.md`). A reference solution at 1.000 and a null agent at
0.000 are necessary and were not sufficient; each defect survived them. The scorer has been
validated to the extent that thirteen campaigns, their controls and their re-scoring have
exercised it, and no further.
