# 2026-05-28 Workflow V1.1 GPT Stage Authority Upgrade

## Summary

- translated the external `literary-os` workflow model into a stronger V1700 GPT-native predevelopment authority system
- added explicit session start and session end tooling
- added installable hooks for pre-commit and pre-push enforcement
- upgraded the mandatory predevelopment checker to require the new docs and tools
- aligned README and CONTRIBUTING with the Stage184 authority baseline

## New Required Commands

```bash
python tools/install_predevelopment_hooks.py
python tools/session_start.py
python tools/run_mandatory_predevelopment_check.py
python tools/session_end.py
```

## Rationale

The old V1.1 adaptation inside V1700 was useful, but it was still mostly a document-level reminder. The new translation makes the workflow executable and testable before planning, before stage work, and before release closure.
