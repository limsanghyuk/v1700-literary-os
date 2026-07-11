# Status notice for `claude_drama_analysis_method_manual_stage01_04_v1.md`

Updated: 2026-07-12

The v1 manual remains preserved as an important historical and methodological source. It contains early forensic findings that motivated the anti-gaming rules.

However, later re-audits corrected several early conclusions and aligned GPT and Claude output contracts. New sessions must use the authoritative v2 entrypoint:

```text
docs/drama_analysis/README.md
```

Priority:

```text
docs/drama_analysis/*V2* and current decision log
> docs/external/claude_drama_analysis_method_manual_stage01_04_v1.md
```

Important later corrections:

- the claim that GPT analyzed mismatched drama contents was a false positive;
- the claim of large-scale dangling scene references was a false positive;
- the core Stage02/03 schemas are aligned rather than one side having a richer schema;
- the main remaining interoperability defect was cross-episode causal bridges stored in `LocalEdge`;
- GPT evidence methods now adopted include SourceLock, QuarterAudit, lineage/quarantine, portable validators, fresh-extraction audits, and limited functional holdouts.

Do not delete the v1 file. Read it as historical evidence, then apply the v2 documents for all new authoring and ingestion work.
