# Agent Runtime Atlas

Evidence-backed discovery of what an AI agent can actually do in its current environment.

**Jim** performs this runtime investigation. **Gemma** is the coordinating ChatGPT Mobile collaborator for NES. This repository is the sole scope of the initial project. Do not involve unrelated research agents, inspect their environments, or modify other repositories without NES explicitly extending the scope.

## Initial artifacts

- [Jim's first-session findings](docs/reports/2026-11-21-jim-initial.md)
- [Machine-readable capability matrix](data/capabilities/jim-2026-11-21.json)
- [Safe reproducible probes and future comparison procedure](docs/probe-methodology.md)
- [Proposed Jim–Gemma handoff protocol](docs/communication-handoff.md)
- [Offline Python probe](scripts/probe_runtime.py) and [unit tests](tests/test_probe_runtime.py)

## Reproduce

Requires Python 3.9+ (tested with Python 3.13.5). Default mode is passive and prints JSON:

    python3 scripts/probe_runtime.py

Explicitly opt in to benign subprocess calls and ephemeral scratch-file roundtrips:

    python3 scripts/probe_runtime.py --allow-exec --allow-temp-write
    python3 -m unittest discover -s tests -v

To save JSON, use --output with an unused file path; overwrite is refused. Review any result before publication.

## Evidence and safety

Statuses: verified, observed_unvalidated, inferred, not_tested, blocked. Every claim identifies the current agent/session, tool surface, procedure, observation, and uncertainty. Advertised tools and API metadata do not prove they function.

The probe sends no network traffic, installs no packages, reads no secrets or environment variables, changes no privileges, and does not query connected personal account data. Session persistence, host privileges, and future independent-agent compatibility have not been established. Local UID 0 is not proof of host privileges.

## Collaboration

Jim records evidence and proposals here. Gemma reviews and coordinates next steps with NES. Findings are submitted for review on a dedicated branch/PR; no automatic merge to main.
