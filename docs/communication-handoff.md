# Frank ↔ Gemma communication design — proposal, not deployed

## Actors and boundaries

Frank owns LoopyLogic research in a distinct execution environment. Gemma is the mobile ChatGPT voice relay for NES. Jim owns this runtime atlas and is not authorized to modify the LoopyLogic repository during this investigation.

Existing LoopyLogic briefing channels, as described to Jim:
- Frank outbound: briefs/chatgpt-to-eve.md (legacy filename retained).
- Gemma inbound: briefs/mobile-to-chatgpt.md.
- Maximum six physical lines per entry, one headline plus concise delta-only bullets.

This is a supplied protocol, not a fresh read of LoopyLogic from Jim's environment.

## Recommended reliability model

1. Treat GitHub as durable source of truth; never rely on chat-window memory as the only queue.
2. Prefer append-only GitHub issue or PR comments for immutable per-message IDs and timestamps, but only if EACH actor's permissions are separately verified. Existing Markdown channels remain an acceptable compatibility transport.
3. Every message carries event_id, source, destination, UTC timestamp, related commit/issue, payload and an acknowledgment reference. Use a monotonic per-sender sequence; never reuse an ID for different content.
4. Delivery states are distinct: created, published, fetched, acknowledged, relayed_to_human. Do not mark delivered before the relevant actor reads it.
5. Deduplicate retries by event_id. For Markdown file append, fetch current blob SHA, perform conditional update, and on a conflict refetch, reconcile and retry. Do not issue concurrent updates to the same path.
6. Compress the mobile briefing to six lines maximum: one header and up to five delta-only bullets. Put long evidence in a linked issue, report or commit. Include an explicit NEEDS_NES field for a blocking decision.
7. A push to GitHub does not itself imply a background listener or that Gemma has seen a message. Polling/notification requires a separately confirmed automation, webhook, workflow or explicit agent invocation.

### Proposed six-line envelope

    [FRANK→GEMMA] id=frank-20261121T220000Z-0001
    - delta: 2 transform call sites mapped
    - evidence: commit <sha>
    - blocker: runtime target unknown
    - needs_NES: approve targeted tracing?
    - ack: pending

## Not yet validated

Real two-agent GitHub delivery; issue permission on both sides; update conflict recovery; retries and idempotency; notification latency; automated polling; voice-read delivery.

## Safe next protocol test

After explicit separate authorization, create one isolated test message in a dedicated issue or branch, have the other agent fetch it, post an acknowledgment referencing the same event_id, retry the event once to check deduplication, and record latency/error behavior. Do not touch Frank's production channels while testing this proposal.
