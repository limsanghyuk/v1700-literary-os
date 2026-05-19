# Stage131 Proposal: GIG / Gate26 Advisory Absorption

## Executive Summary

Stage131 promotes the Stage130 deferred Gate26 issue into a safe advisory layer.
The objective is not to let Gate26 hard-block stories. The objective is to classify cross-work canon tension precisely enough that the writer can decide.

## Three-Expert Review

### Principal Architect

Gate26 must not be a blunt contradiction breaker. Longform drama needs several different inconsistency categories:

- True contradiction: mutually exclusive canon facts without an in-story explanation.
- Intentional mystery: a contradiction-like surface that is protected by reveal budget.
- Character misunderstanding: a point-of-view or knowledge-boundary gap.
- Reveal delay: canon truth exists, but the story withholds it for pacing.

The architecture therefore keeps Gate26 advisory-only and routes only true contradictions to writer review.

### Principal Compiler

The implementation must compile into deterministic local contracts:

- `gig_advisory` package
- `stage131` runner
- `stage131_release_gate`
- Stage131 manifests
- Stage131 release evidence
- Stage131 tests

No provider call, training loop, AutoRepair mutation, or canon auto-resolution is allowed.

### Principal Systems Engineer

The risk is overcorrection. If the system automatically resolves every apparent contradiction, it will destroy mystery, unreliable point of view, and delayed reveal. Stage131 therefore preserves writer authority:

- Gate26 hard block stays disabled.
- True contradiction requires writer approval.
- Intentional mystery and reveal delay remain valid.
- Cross-project writes remain blocked.

## Final Agreement

Stage131 should be implemented as:

```text
Stage130 MultiWork Release
  -> Stage131 GIG / Gate26 Advisory Absorption
  -> Stage132 Contradiction Classifier + Mystery Exemption
```

Stage131 is complete only when the advisory layer is connected to tests, manifests, release evidence, main release gate, repo doctor, README, changelog, and GitHub history.
