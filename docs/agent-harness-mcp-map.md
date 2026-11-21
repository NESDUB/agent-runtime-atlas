# Agent Harness & MCP Map — Jim, 2026-11-21

## Scope and provenance

This report implements the revised NES/Gemma instructions in PR #2 comments 7070347293 and 7070358739. The current repository AGENTS.md on main was read and verified at blob SHA a06f8d98e4523bc6f1487774876bd8e5439a82ee. Priority is **all authorized discoverable agent resources**, especially skills; the full software ZIP and cross-session persistence test are deferred.

Methods: skill registry listing and individual skill reads; exposed JavaScript tool metadata enumeration; authorized GitHub tree/read actions; read-only bounded local directory scans, CLI version checks, interpreter imports, Python package metadata and global Node package listing. No external shell network requests, installations, privileged inspection, protected prompts, credential reads or private connected-account queries.

Statuses: **discovered** = name/path observed; **readable** = authorized content/metadata accessed; **configured** = wiring evidenced; **invocable** = command/action callable; **tested functional** = expected behavior observed. A filename or exposed tool name never implies successful operation.

## Inventory overview

| Surface | Discovered | Tested | Limitation |
|---|---:|---|---|
| Virtual plugin skill roots | 37 | 37 root reads succeeded | Workflows not necessarily executed |
| Advertised bundled skill resource URIs | 87 | A sample skill.md and reference.xlsx read | Most assets not fetched separately |
| Local SKILL.md files | 4 | All four readable; hashes recorded | Helper scripts not individually exercised |
| JavaScript tool registry actions | 202 | Selected skills and GitHub actions invoked | 202 is discovery count, not working-permission count |
| MCP-prefixed managed connector actions | 187 | Selected GitHub actions | Native MCP transport/server configuration not exposed |
| Scoped candidate MCP/config paths | 12 | Existence checks completed | None found at checked paths; not systemwide proof |
| Repository agent instruction files | AGENTS.md and README.md | GitHub read and tree listing | No CLAUDE.md/Copilot/MCP config in scoped repo tree |

### Machine-readable inventories

- [All 202 tool names, families, descriptions, status](../data/agent-discovery/tool-actions-2026-11-21.json)
- [Skills 00–11](../data/agent-discovery/plugin-skills-00-11.json), [skills 12–23](../data/agent-discovery/plugin-skills-12-23.json), [skills 24–36](../data/agent-discovery/plugin-skills-24-36.json)
- [Local paths, package versions, CLI entry points and config candidates](../data/agent-discovery/local-surfaces-2026-11-21.json)

## 1. SKILLS are two different discovery surfaces

**Virtual registered skills:** The tools.skills__list({}) API returned 37 entries. Every root was independently opened via tools.skills__read({uri}). Instruction roots advertised 87 bundled file URIs in total, stored per skill in the JSON catalog. The categories are:

| Family | Count | Role | Outcome |
|---|---:|---|---|
| Spotify app | 6 | Search/browse, playlists, playback, library, now-playing | All roots readable; no matching Spotify actions exposed in the 202-action tool catalog |
| OpenAI artifact templates | 20 | Templates for documents, spreadsheets and slides | Roots readable; one project-tracker reference.xlsx and skill.md readable |
| Template Creator | 1 | Create reusable template skills | Instructions readable, workflow not tested |
| Pages | 4 | Write, maintain, organize and schedule Space pages | Instructions readable; 37 ChatGPT_Space actions discoverable |
| Artifact routers | 4 | Explicitly selected PDF/document/presentation/spreadsheet workflows | Instructions readable; no route invoked for a user artifact |
| Plugin Management | 1 | Plugin discovery, dependencies, connections | Instructions readable; 6 related actions discoverable |
| Health | 1 | Personal health connector instructions | Instructions readable; personal data not queried |

A plugin skill is a **virtual skill resource** (skills://plugins/...); its presence does not prove that a corresponding service is connected, authenticated, or exposed for invocation. The Spotify skill/action mismatch makes this distinction concrete. Skill activation preconditions vary: selection-driven router skills require explicit artifact selection, while other skill roots describe task-specific triggers. Downstream actions were not exercised merely by reading a root.

**Bundled file check:** The Project Tracker skill's advertised skill.md file and assets/reference.xlsx were independently readable through skills__read. The XLSX read returned extracted textual content (~112,717 characters), not an editable workbook. Its instructions mention artifact-template.json although that filename was not present in its advertised available-file URI list; access to that manifest is **unverified**, not assumed.

**Local skill directories:** The shell separately exposes:

    /home/oai/skills/
      docx/SKILL.md          13,799 bytes; 69 non-cache files in folder
      pdfs/SKILL.md           5,389 bytes; 47 non-cache files in folder
      slides/SKILL.md           812 bytes; 64 non-cache files in folder
      spreadsheets/SKILL.md  7,406 bytes; 4 non-cache files in folder

All four SKILL.md files were opened for size, headings and SHA-256; exact hashes are preserved in the local inventory. Support directories include docx examples/ooxml/scripts/tasks/troubleshooting; PDF js/scripts/examples/tasks/troubleshooting; slides artifact_tool/container_tools/pptxgenjs_helpers/slide_templates; spreadsheets templates. The 184 supporting files include document-processing utilities, rendering/inspection scripts and example workflows, but those scripts are not each independently invoked.

**Instruction precedence:** The repository AGENTS.md is public project-scoped guidance; skill instructions describe task-specific workflows. No inference is made about the precedence or contents of protected platform instructions. No protected prompts were inspected or reproduced.

## 2. Repository and bounded local instruction search

Authorized GitHub tree read on PR #2 (then-head 70acbfc983db79fb5422d3653585e06696240a56, truncated=false) returned 17 files at that moment, including AGENTS.md and README.md. No repository CLAUDE.md, .github/copilot-instructions.md, SKILL.md or mcp.json appeared. Subsequent commits have added atlas documents and inventories.

A bounded local name search under /home/oai/skills and /mnt/data found exactly the four local SKILL.md files for AGENTS.md/CLAUDE.md/SKILL.md/MCP candidate filename patterns. Twelve fixed candidate locations for conventional user MCP/agent config files were checked for **existence only**; none existed at those locations. This does not claim the complete host has no other instructions or configs. Private or protected storage and authorization settings were not inspected.

## 3. Harness / launchers / installed agent frameworks

| Surface or path | Evidence | Classification |
|---|---|---|
| functions.exec / ALL_TOOLS metadata | JavaScript orchestrator exposed 202 actions; selected GitHub read/write calls successful | Exposed registry and selected actions tested functional |
| tools.skills__list and tools.skills__read | Registry enumerated; 37 root reads and two bundled-file reads succeeded | Tested functional for discovery/read |
| /opt/pyvenv/bin/python | Python 3.13.5, harmless subprocess and file tests succeeded previously | Executable, functional |
| /opt/nvm/versions/node/v22.16.0/bin/node | Node 22.16.0, harmless arithmetic execution succeeded previously | Executable, functional |
| npm / npx | Version 10.9.2; paths present | Version verified; network-assisted package run not attempted |
| /opt/pyvenv/bin/uv and uvx | Version 0.10.0 | Version verified; no remote process launch |
| /usr/bin/git | Version 2.47.3; local invocation succeeded | Executable, functional locally; authenticated shell push untested |
| Python openai, fastapi, artifact_tool modules | Importable in active Python | Installed/importable, **not** proven agent runtime services |
| Python mcp, fastmcp, anthropic, langchain, langgraph, crewai, autogen | Imports failed | Not available through that active interpreter; other environments unknown |
| codex, claude, gemini, gh, mcp, mcp-server CLI names | No executable found on the checked PATH | Not on PATH; no systemwide conclusion |

Other discovered package metadata: Pydantic 2.13.5, FastAPI 0.128.2, Uvicorn 0.48.0, JupyterLab 4.5.3, artifact_tool_v2 2.8.66, Go 1.23.2, jq 1.7, TypeScript 5.8.3, ts-node 10.9.2, Sharp 0.34.1, pptxgenjs 4.0.0 and http-server 14.1.1. Global Node package names and versions and relevant Python framework distributions are in the local JSON. Presence is not proof of configured/reachable services.

No evidence shows that shell launchers start or govern this ChatGPT orchestration runtime; local execution, code-mode actions and virtual skill services are distinct surfaces. Platform-managed internals are not exposed through these authorized metadata probes and were not inspected.

## 4. MCP: connector API vs direct server vs advertised skill

| Exposed action family | Count | Actual behavioral test here |
|---|---:|---|
| GitHub | 89 | Selected authenticated repository reads/writes passed |
| ChatGPT_Space | 37 | Exposed only |
| Gmail | 21 | Exposed only; no mail data accessed |
| Finances | 14 | Exposed only; no financial data accessed |
| Health | 13 | Exposed only; no private health data accessed |
| Automations | 7 | Exposed only; no schedule created |
| Plugin_Management | 6 | Exposed only; no account changes |
| **MCP-prefixed connector/API actions** | **187** | Subset exercised |
| Files, Skills, User Settings | 11 + 2 + 2 | Skills discovery/read exercised |

MCP-prefixed names reveal **managed tool/connector action functions** in the orchestration registry, not an independently observed native MCP server, stdio process, Streamable HTTP/SSE transport, host/port or authentication configuration. No direct MCP endpoint, transport negotiation or server manifest was verified. The GitHub connector works, but the infrastructure behind its action interface remains undisclosed. Do not describe all 187 functions as direct MCP server tools without a supported server-level mapping.

In the active shell, Python mcp and fastmcp are not importable, no mcp CLI exists on checked PATH, no MCP-looking global Node package was returned, and common config candidate files were not found at 12 checked locations. These scoped negatives cannot rule out platform-managed MCP connections outside the shell.

## 5. Evidence quality and next actions

- **Verified:** virtual skill registry and 37 root reads; two listed asset reads; four local SKILL.md reads/hash checks; safe CLI version and package metadata; 202 action-name enumeration; selected GitHub connector reads/writes.
- **Discovered/untested:** most skill asset URIs, 202 tool family permissions outside selected GitHub/skills calls, agent launcher implementations, local skill helper executions, native MCP server topology, connector authentication configuration, skill-to-action workflow end-to-end.
- **No unauthorized access:** no credentials, private data, protected platform instructions, direct unapproved network transmissions, package installs or privileged operations.
- **Highest-value next:** reconcile each of the 37 skill workflows with its listed downstream action family and availability; safely verify listed text bundle references; address the previously reported probe-output validation bug; seek an explicitly permitted platform metadata interface for direct MCP server registrations if one exists. Preserve separate tests for readable, invocable and functional.

**Assessment:** exhaustive with respect to the **37 currently registered skill roots and 202 exposed tool actions** and the explicitly checked local/repository surfaces. Not a complete atlas of protected infrastructure, unconstrained filesystem roots or unexposed runtime services. PR #2 remains **open, unmerged**.
