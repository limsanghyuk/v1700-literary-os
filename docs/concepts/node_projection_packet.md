# Node Projection Packet

GraphNexus exposes role-safe graph packets.

- Node1 may receive canon, timeline, and blast-radius context.
- Node2 receives only `Node2GraphSurfacePacket`.
- Node3 receives critic and leakage-risk context.

Node2 must never receive raw graph secrets, unrevealed reveal contents, or unapproved canon candidates.
