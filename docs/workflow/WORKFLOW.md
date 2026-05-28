# V1700 Workflow

This workflow follows the upgraded GPT translation of the external V1.1 authority model.

## One-Time Local Setup

```bash
python -m pip install -e ".[dev]"
python tools/install_predevelopment_hooks.py
python tools/session_start.py
```

The installed hooks block commits or pushes when the GPT predevelopment protocol is violated.

## Core Rule

`session_start.py` is mandatory before:

- planning a proposal or blueprint
- starting a Stage implementation
- doing an integrity repair
- closing a release authority mismatch

## Working Flow

1. Pull or verify the latest GitHub state.
2. Run `python tools/session_start.py`.
3. Run `python tools/run_mandatory_predevelopment_check.py`.
4. Read or update proposal, blueprint, roadmap, and session note.
5. Implement code, tests, docs, manifests, release evidence, gates, and repo doctor recognition together.
6. Run stage gate, main release gate, repo doctor, metadata, asset integrity, and targeted regression.
7. Build ZIP + `.sha256` + `SHA256SUMS.txt` with the canonical checksum flow.
   Use `python tools/regenerate_sha256sums.py` before release-asset validation so text digests stay platform-neutral.
8. Re-extract and verify.
9. Run `python tools/session_end.py`.
10. Push branch, open PR, require green Actions, merge, tag, and publish release assets when release closure is in scope.
