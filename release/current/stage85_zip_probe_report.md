# Stage85 ZIP Probe Report

Date: 2026-05-13

## Package Under Test

```text
C:\AI_Codex\codex-work\gpt\packages\v1700_stage85\V1700_stage85_gitnexus_density_upgrade_integrated_repository.zip
```

## ZIP Structure Check

```text
entry_count = 534
has_git = false
has_gitnexus = false
has_venv = false
has_stage85_gate = true
has_stage85_manifest = true
has_stage85_report = true
```

## Extraction Probe

Probe extraction:

```text
C:\AI_Codex\codex-work\gpt\analysis\stage85_zip_probe_20260513_131749
```

Repository root:

```text
C:\AI_Codex\codex-work\gpt\analysis\stage85_zip_probe_20260513_131749\gpt\active\v1700\literary_generator
```

## GitNexus Analyze

```text
Repository indexed successfully
3,623 nodes | 5,769 edges | 41 clusters | 166 flows
```

## Gate Results

```text
tools/run_stage85_release_gate.py = pass
tools/run_release_gate.py = pass
```

## Final Judgment

```text
The packaged Stage85 repository can be extracted, indexed with GitNexus, and validated through both Stage85 and main release gates.
GitNexus remains excluded from the runtime package as generated state, while the release evidence and fallback contracts remain included.
```
