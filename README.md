# Agent Runtime Atlas

Evidence-backed discovery of what an AI agent can actually do in its current environment. Jim owns this atlas; Frank runs separately in the LoopyLogic environment; Gemma relays mobile voice decisions. Never assume one agent shares another's tools, permissions or filesystem.

## Initial artifacts

- [Jim's findings, November 21, 2026](docs/reports/2026-11-21-jim-initial.md)
- [Machine-readable capability matrix](data/capabilities/jim-2026-11-21.json)
- [Safe probes and independent comparison protocol](docs/probe-methodology.md)
- [Proposed Frank–Gemma handoff](docs/communication-handoff.md)
- [Offline Python probe](scripts/probe_runtime.py) and [tests](tests/test_probe_runtime.py)

## Reproduce

Requires Python 3.9 or newer (initially tested on Python 3.13.5). The default mode performs passive system inspection and outputs JSON:

    python3 scripts/probe_runtime.py

Explicitly opt in to benign subprocess calls and ephemeral scratch-file roundtrips:

    python3 scripts/probe_runtime.py --allow-exec --allow-temp-write
    python3 -m unittest discover -s tests -v

To save JSON, pass --output followed by an unused file path. The script refuses to overwrite existing files. Review any result before publication.

## Rules

Statuses: verified, observed_unvalidated, inferred, not_tested, blocked. Every claim identifies the specific agent/session, invocation surface, test and result. An advertised tool, API metadata flag or another worker's result is not proof.

This probe makes no network requests, installs no packages, reads no secrets or environment variables, changes no privileges, and does not probe connected personal accounts. Cross-session persistence and host privileges must be tested independently. UID 0 in an isolated runtime is not proof of host privileges.

## Separation of concerns

Jim can propose communication improvements but cannot modify Frank's LoopyLogic project without separate authorization. Work is published to a review branch and proposed through a pull request; no automatic merge to main.
