# Jim ↔ Gemma GitHub handoff — proposal, not deployed

## Current project boundary

Jim investigates his own runtime; Gemma coordinates with NES through ChatGPT Mobile. Both should use NESDUB/agent-runtime-atlas as the source of project records. Do not read, modify, or send tasks to unrelated research agents or repositories. This is a design proposal; there has not been a verified second-agent delivery.

## Proposed transport

1. Maintain a durable, versioned source of truth in this repository. Use append-only GitHub issue/PR comments for discrete messages if each actor independently verifies appropriate permissions; use versioned Markdown as a fallback.
2. Each event includes event_id, source, destination, UTC timestamp, minimal delta, related commit/report URL and optional NEEDS_NES decision field. Use a per-sender monotonic sequence and do not reuse an event ID for different content.
3. Separate states: authored, published, fetched, acknowledged, relayed_to_NES. A successful GitHub write is not proof that Gemma read or spoke the briefing.
4. Acknowledgments reference exact event IDs. On retries, read before writing and deduplicate by ID. If updating Markdown, use fetched blob SHA to make a conditional update; after conflict refetch and reconcile rather than overwriting.
5. Keep voice briefings short and delta-only: one headline plus no more than five bullet lines. Link deep technical findings to a committed report.
6. No background polling or notification capability is assumed. Only a separately verified automation/trigger or explicit invocation can progress messages without another user turn.

### Example message (six lines)

    [JIM→GEMMA] id=jim-20261121T220000Z-0001
    - delta: offline runtime probe tested
    - evidence: report + commit link
    - blocked: outbound shell networking untested
    - needs_NES: approve scoped HTTPS probe?
    - ack: pending

## Untested hypotheses and next validation

Unverified: Gemma's independent read/ack ability, issue-comment write permissions on both sides, failure recovery, voice delivery, notification delay, simultaneous updates and idempotent retries. Do not claim operational inter-agent communication based on a document in GitHub.

After NES/Gemma authorizes a sandbox transport trial, create a single isolated test event in this repository, independently fetch it in Gemma's environment, post a matching acknowledgment, and verify a duplicate ID does not create a duplicate action. Keep tests in this repository; do not expand scope without new instructions.
