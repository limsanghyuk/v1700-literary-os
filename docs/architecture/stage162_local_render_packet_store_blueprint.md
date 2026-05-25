# Stage162 Blueprint — Local Render Packet Store

## Architecture

Stage162 adds `v1700.local_render_packet_store` as a deterministic, read-only compiler data layer.

```text
Stage161 Rendering Contract
+ Stage159 dry-run trace references
→ samples/stage162_render_packet_store/render_packets.jsonl
→ checksum validation
→ catalog/schema/checksum/projection/lineage evidence
→ Stage162 release gate
```

## Data contract

Each render packet contains stable ids, source rendering contract id, source execution packet ids, source trace ids, surface channel, boundary level, render mode, safe payload summary, Node2 projection summary, checksum, and disabled write policy.

## Safety

The loader blocks checksum mismatch, duplicate ids, enabled render mode, non-disabled write policy, provider handles, write handles, hidden reveal payloads, raw manuscript payloads, learning payloads, and credentials.
