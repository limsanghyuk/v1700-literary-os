# Stage132 Proposal: Contradiction Classifier + Mystery Exemption

## Executive Summary

Stage132 deepens Stage131. Stage131 established that Gate26 must remain advisory-only. Stage132 defines the evidence rules that decide whether a conflict is a true contradiction, intentional mystery, POV misunderstanding, reveal delay, or no conflict.

## Three-Expert Review

### Principal Architect

A longform literary OS must not destroy mystery just because two facts appear inconsistent. The architecture must separate:

- hard canon conflict
- deliberate mystery
- limited character knowledge
- delayed reveal
- normal causal continuation

The classifier therefore reads narrative evidence instead of raw text and never repairs canon by itself.

### Principal Compiler

The classifier must compile to local deterministic contracts:

- `ContradictionEvidence`
- `ContradictionClassification`
- classifier matrix
- mystery exemption audit
- Stage132 release gate
- Stage132 manifests and evidence

The implementation must run without provider calls and must not mutate shared canon.

### Principal Systems Engineer

The major risk is false repair. A mystery exemption without a reveal lock would let the system excuse real continuity errors. Stage132 therefore requires both a reveal lock and payoff budget before a mystery can be exempted.

## Final Agreement

Stage132 is accepted if it:

- preserves Stage131 advisory-only authority
- routes true contradictions to writer review
- grants mystery exemption only with evidence
- blocks hard Gate26, AutoRepair, canon auto-resolution, provider calls, and cross-project writes
