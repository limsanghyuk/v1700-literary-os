# Web Fallback Development Blueprint

Status: active blueprint
Created: 2026-05-30
Scope: development while local GitNexus is unavailable

## 1. Purpose

This blueprint allows web-side development to continue when local Codex or GitNexus cannot run.

It does not replace GitNexus. It creates temporary evidence that can be checked later.

## 2. Core status

Use this status while GitNexus is unavailable:

```text
PASS_WITH_APPROVED_FALLBACK_PENDING_GITNEXUS
```

Do not use this status until GitNexus output is actually committed:

```text
PASS_WITH_GITNEXUS_OUTPUT
```

## 3. Architect and compiler consensus

The chief architect requires continuity.

The chief compiler requires structured evidence.

Consensus:

```text
Web development may continue if every stage records parent, successor, inherited source, required files, and release result.
```

## 4. Required fallback files

For any target N, create:

```text
release/fallback/{N}/fallback_index_report.md
release/fallback/{N}/contract_coverage_report.md
release/fallback/{N}/successor_trace_report.md
release/fallback/{N}/invariant_check_report.md
release/current/{N}_fallback_evidence_report.md
```

If JSON is easy to write, JSON may also be used.

## 5. Required checks

Each fallback pass checks:

```text
stage order
required contracts
required reports
page inheritance
successor handoff
pending GitNexus warning
Page09 mapping reference
Page10 packet dependency
```

## 6. Development rule

Web may build contract-first stages today.

Local GitNexus must later confirm or repair the fallback result.

No page should be treated as final GitNexus-backed evidence until the GitNexus files are committed.

## 7. Page11 use

Page11 may start as fallback-backed scaffold using Page10 outputs.

The Page11 release gate should keep the pending evidence warning until local GitNexus is available.
