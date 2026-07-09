# KMN Stage01~04 Next Chat Handoff

## Current canonical state

- Work: 결혼못하는남자
- Scope: EP01~EP16
- Stages completed: Stage01 SceneCard, Stage02 SequenceBlueprint, Stage03 Arc/Edge, Stage04 Season Wiring
- Final decision: `PASS_FINAL_STAGE01_04_PRECISION_AUDIT`
- Developer delivery SHA256: `488ae8f23dc5c598836c8896ef421d8603cae3649a7f78f6364a55f8bc6c3755`
- Precision audit SHA256: `e90e4dff2438cc2997a7a21efa74e1070d838a619b063d7c47f23682ae1ebd1c`

## What to read first

1. `docs/analysis/kdrama/kmn_stage01_04_full_analysis_operating_report.md`
2. `release/current/drama_close_reading/kmn/stage01_04_final_delivery_manifest.json`
3. `release/current/drama_close_reading/kmn/stage01_04_precision_audit_summary.json`
4. `docs/development/kmn_stage01_04_next_chat_handoff.md`

## Hard rules

- Do not use raw script export.
- Do not generate Stage01 meaning fields with Python/template functions.
- Use 1 episode × 4Q as the stable production unit.
- Stage02 is feedback layer, not post-hoc summary.
- Any template residue blocks PASS.
- If Stage01/2 contamination is found, rebuild Stage03/4.
- GitHub repo stores metadata/report/manifest. Binary artifacts are tracked by SHA and should be managed as release assets or local/private package.

## Canonical objects

Stage01:
`authored/*.seqcard.jsonl`

Stage02:
`authored_seq/*.seqblueprint.jsonl`

Stage03:
`authored_chararc`, `authored_relarc`, `authored_edges`, `authored_payoff`, `authored_series`

Stage04:
`season_wiring/*`

## Next drama execution template

```text
source inventory
→ episode scene lock
→ EPn Q1 Stage01 + partial Stage02
→ Q1 validation/rewrite
→ Q2/Q3/Q4 repeat
→ EPn integrated Stage01/Stage02
→ episode validation + ZIP
→ full season Stage01/2 audit
→ Stage03 Arc/Edge build
→ Stage04 Season Wiring build
→ developer package
→ precision audit
```
