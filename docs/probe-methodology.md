# Reproducible runtime probe methodology

## Provenance contract

Every evidence record must specify UTC date, agent/environment ID, invocation surface, platform/runtime versions if known, exact safe test procedure, observed result, status and limits. Do not collect credentials, environment dumps, secret-bearing headers, private content or exact sensitive locations. Use neutral environment IDs, not account identifiers.

A tool-orchestrator JavaScript isolate, shell container, Python tool and remote GitHub connector are distinct surfaces. A successful network-capable connector does not establish direct shell internet access.

## Status semantics

| Status | Meaning |
|---|---|
| verified | Executed a bounded test in the stated environment; expected result observed. |
| observed_unvalidated | Exposed capability or API metadata seen, but operational outcome not tested. |
| inferred | Plausible from indirect evidence, not directly verified. |
| not_tested | No test attempted or deferred for safety or authorization. |
| blocked | Attempted test failed or could not proceed; state preconditions and safe error type. |

## Execution

1. Default passive probe: python3 scripts/probe_runtime.py. Records sanitized OS, kernel, architecture, Python, reported CPU count, effective UID indicator and whether a fixed set of tools is on PATH.
2. Local scratch (explicit opt-in): python3 scripts/probe_runtime.py --allow-temp-write. Creates temporary directories and benign text files inside /mnt/data and /tmp if these directories exist, reads them back, and automatically cleans up.
3. Fixed subprocesses (explicit opt-in): python3 scripts/probe_runtime.py --allow-exec. Runs only sh, Python, Node and Git with known harmless commands, no input from the network and a four-second timeout.
4. Combined: python3 scripts/probe_runtime.py --allow-exec --allow-temp-write. Run unit checks via python3 -m unittest discover -s tests -v.
5. Save results: optional --output path.json creates a NEW local file and refuses an overwrite. Inspect before sharing. Report errors by type, not raw secret-bearing output.

The probe itself does not verify authentication, GitHub writes, network egress, system-wide package availability, background execution or persistence in another chat. These require separately authorized tests.

## How Frank can compare

Frank must examine his own applicable agent instructions, obtain the same script through his authorized repository workflow, record an independent agent/session ID, and run only probes permitted in his environment. Jim must not run commands in Frank's environment.

Each agent should commit separate files under data/capabilities/ and dated reports under docs/reports/. Compare rows keyed by capability, invocation surface and environment ID, not merely matching executable names.

Recommended independent comparisons: OS/arch/version; shell/subprocess; temporary file read/write/cleanup; within-session readback; fresh-session persistence; GitHub connector read and isolated branch write; package list; approved DNS and outbound HTTPS (with explicit consent); and one second-agent delivery/ack scenario (with explicit consent). Mark missing evidence as not_tested instead of assuming parity.

Cross-session marker persistence: write a benign marker in one session, then initiate a distinct session and attempt readback. Within-session tool calls never qualify as a cross-session durability test.

## Safe boundaries

Do not attempt credential discovery, broad network scans, privilege escalation, host escape, untrusted code execution, package installation, excessive resource use, calls to unapproved network targets, or destructive Git operations. Ask before externally transmitting test data or making persistent account changes beyond already authorized repository commits.
