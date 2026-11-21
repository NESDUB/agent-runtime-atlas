# Cross-session persistence: controlled marker-and-readback protocol

**Status:** prepared and seeded in Jim's present session, **not** yet tested in a genuinely new session. Scope is Jim ↔ Gemma in this repository. Follow current AGENTS.md. No external shell network, user account data or elevated operations.

## What different tests actually establish

| Surface | Independent control | Now | A real new-session pass requires |
|---|---|---|---|
| Local sandbox filesystem | Harmless marker at fixed path in /mnt/data; compare bytes and SHA-256 | Seeded and same-session checked | On a **genuinely new agent/chat session**, before downloading/materializing any GitHub or conversation file, read the **pre-existing** marker at exactly the recorded path, compare ID and SHA-256, and report platform/session separately. |
| Conversation-provided file | User uploads/attaches a distinct benign file, retaining attachment reference | Not tested | Start a distinct session and inspect whether it is actually automatically available **without new upload or materialization**. If user reattaches it, classify as an explicit transfer, not persistence. |
| GitHub remote state | Committed manifest in this repository's PR branch; read using connected GitHub API | GitHub write/read previously verified; manifest committed here | Fetch the **specific recorded commit/path** in a genuine new session. A successful remote fetch proves the GitHub source is durable and readable, **not local sandbox persistence**. |

## Baseline (Jim, current session only)

- Marker ID: `jim-2026-11-21-persistence-seed-01`
- Original seed timestamp (UTC): `2026-11-21T22:25:24+00:00`
- Exact local path: `/mnt/data/atlas-session-marker-2026-11-21.json`
- Exact byte SHA-256: `b66bd011b2ac115662fec44b4586e90e0b646585b1cb9270a58828cfceaad897`
- Local test: readback in the same invocation passed; two isolated offline unit tests passed. These are not cross-session results.
- Repository record: `data/persistence/jim-2026-11-21-seed.json` on review branch `jim/initial-atlas-2026-11-21`.
- Marker file deliberately **not uploaded or published** to GitHub as an attachment: that would risk confounding a local-persistence test with explicit file restoration.

## Reproduce in a genuinely new session

First identify that the new session is really different (record new chat/session distinction without publishing identifiers). **Do not seed again** and **do not download or materialize the marker into /mnt/data** before this check. Use the already recorded baseline from GitHub or this document. Then:

```sh
python3 scripts/persistence_probe.py check \
  --path /mnt/data/atlas-session-marker-2026-11-21.json \
  --marker-id jim-2026-11-21-persistence-seed-01 \
  --expected-sha256 b66bd011b2ac115662fec44b4586e90e0b646585b1cb9270a58828cfceaad897
```

If absent, record `FileNotFoundError`/`blocked` **for that new session**; it is not proof the file was deleted. If matching, record `verified_read` and note that isolation/mount semantics still need identification. Never silently recreate a missing marker.

For future baselines, explicit one-time creation is:

```sh
python3 scripts/persistence_probe.py seed --path /mnt/data/UNIQUE-NEW-MARKER.json --marker-id nonsecret-unique-id
```

The seed refuses overwrite; the check is read-only; no network requests, credentials, package installation or elevated operations. To test remote GitHub durability use the connected GitHub read action in the *new session* on the immutable commit; do not infer shell DNS/HTTPS from it.

## Observation checklist

Record status per surface (`verified`, `observed_unvalidated`, `not_tested`, `blocked`), UTC time, agent/session distinction, invocation mechanism, tested path or commit ref, expected/observed hash, failure category, and whether any artifact was explicitly reattached or materialized. Do not claim cross-session persistence from two tool calls within the same chat.

## Remaining unknowns

True cross-session sandbox and attachment visibility, GitHub durability independently rechecked in a new session, per-session mounted file semantics, app context persistence, and background execution are unknown. Avoid conflating remote GitHub storage, model memory, chat attachments and filesystem state.
