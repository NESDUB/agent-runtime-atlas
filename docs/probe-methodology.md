# Safe reproducible runtime probe methodology

## Provenance

For every result record UTC timestamp, current agent/environment ID, invocation surface, platform and versions (if known), command or connector action, success criterion, actual result, status and limitation. Never commit credentials, auth headers, environment-variable dumps, private data or sensitive host details.

A JavaScript tool-orchestrator isolate, shell container, Python tool and connected GitHub API are distinct surfaces. A successful connector operation does not demonstrate shell outbound internet access.

## Status definitions

| Status | Meaning |
|---|---|
| verified | Bounded test executed in the specified current environment and expected result observed. |
| observed_unvalidated | Tool/schema or API metadata visible, but functional behavior untested. |
| inferred | Indirect evidence without direct confirmation. |
| not_tested | Test not attempted, or deliberately deferred. |
| blocked | Attempted test failed or could not proceed; record safe error class and prerequisites. |

## Reproduction

1. Passive only: python3 scripts/probe_runtime.py. Records OS/kernel/architecture/Python, CPU count, effective UID indicator and fixed executable availability on PATH.
2. Explicit scratch opt-in: python3 scripts/probe_runtime.py --allow-temp-write. In /tmp and /mnt/data if present, create a temporary directory and text file, roundtrip read and clean automatically.
3. Explicit process opt-in: python3 scripts/probe_runtime.py --allow-exec. Run fixed harmless sh, Python, Node and Git commands with four-second timeouts. No arbitrary commands.
4. Combined: python3 scripts/probe_runtime.py --allow-exec --allow-temp-write. Test passive defaults via python3 -m unittest discover -s tests -v.
5. Optional local output: --output path.json creates a NEW file and refuses overwrite. Inspect before sharing.

The script does not establish network egress, connected-service permissions, GitHub authenticated writes, package-install privileges, notification delivery, or cross-session persistence. Those need separate, authorized, scoped tests.

## Protocol for a future environment comparison (not yet authorized or executed)

This methodology is reusable, but the current investigation concerns Jim only. No other research agent should be contacted or tested for this initial scope. If NES explicitly authorizes a comparison in the future, a separate agent must run the same benign probes independently and record separate environment IDs, timestamps and source evidence. Compare by capability, invocation surface and environment. Missing evidence remains not_tested, never inferred as equivalent.

A persistence test needs a benign marker written in one ChatGPT session and a new session trying to read it; reading it through multiple tools in the same session does not establish persistence.

## Boundaries

No external networking probe without authorization; no privileged or destructive operations; no credential discovery, network scans, package installation, resource exhaustion, host escape, untrusted code execution, third-party account queries or changes to unrelated repositories. Ask before persistent account changes beyond the GitHub commits NES explicitly requested.
