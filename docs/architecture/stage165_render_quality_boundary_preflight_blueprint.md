# Stage165 Blueprint — Render Quality and Boundary Preflight

## Inputs

- Stage164 surface draft dry-run report
- Stage164 dry-run trace
- Stage164 Node2 surface projection matrix

## Outputs

- quality metric matrix
- boundary preflight matrix
- render quality scorecard
- Node2 quality projection matrix
- blocked render operation registry
- Stage166 entry criteria
- regression snapshot

## Algorithm

1. Load Stage164 dry-run surface draft evidence.
2. Validate stable unit order, trace alignment, checksum uniqueness, and render type coverage.
3. Scan draft text and Node2 summaries for forbidden hidden/provider/write/raw tokens.
4. Produce a deterministic quality score and quality boundary checksum.
5. Block Stage166 entry if any quality, boundary, provider-zero, or write-zero invariant fails.

## Invariants

- provider generation disabled
- runtime rendering disabled
- render writes disabled
- Node2 hidden payload access zero
- raw manuscript leakage zero
- credential leakage zero
