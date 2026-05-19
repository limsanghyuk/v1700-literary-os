# Stage135 Proposal — LearningQualityGate & Candidate Registry

## Summary

Stage135 implements the safety layer required before any bounded learning work begins.

## Problem

Stage134 can recommend review or future weight-candidate tracking, but the system needs a deterministic gate that prevents unsafe audit results from becoming learning data.

## Proposal

Add a LearningQualityGate and Candidate Registry. The registry records candidate status only. It cannot trigger runtime training or weight updates.

## Success Criteria

- Stage134 baseline gate passes.
- Review-required cases route to REVIEW_ONLY.
- Learning allowed count remains zero.
- Training triggered count remains zero.
- Mutation count remains zero.
- Provider calls remain zero.
- Stage135 release gate passes.
