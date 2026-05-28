# V1700 Session Protocol

## Session Start

Every V1700 session begins with this order:

```bash
git pull --ff-only origin main
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
```

Then read:

- the latest relevant file in `docs/sessions/`
- the target proposal
- the target blueprint

If the session is a new Stage start, create the working branch only after the checks pass.

## Session End

Every meaningful session ends with this order:

1. Update or add the relevant docs under `docs/`.
2. Update or add a session note under `docs/sessions/` when the work changes authority, roadmap, or release state.
3. Run `python tools/session_end.py`.
4. Commit and push the branch.
5. If release closure is in scope, verify PR, merge, tag, release, and release assets.

## Mandatory Session Notes

Session notes are especially required when:

- a new Stage starts
- a proposal or blueprint changes direction
- a web-developed branch is handed to local Codex for closure
- integrity, checksum, or release authority is repaired

## GPT First-Message Rule

At the start of a new coding conversation, GPT should first verify:

1. GitHub `main` and latest tag state
2. current local branch and HEAD
3. latest relevant session note
4. `python tools/session_start.py` result
5. proposal and blueprint context
