# V1700 Workflow

This workflow follows the V1.1 authority model.

1. Preflight and design first.
2. Implement code, tests, docs, manifests, release evidence, gates, and repo doctor recognition together.
3. Run stage gate, main release gate, repo doctor, metadata, asset integrity, and targeted regression.
4. Build ZIP + `.sha256` + `SHA256SUMS.txt`.
5. Re-extract and verify.
6. Push branch, open PR, require green Actions, merge, tag, and publish release assets when release closure is in scope.
