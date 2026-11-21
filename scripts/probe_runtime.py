#!/usr/bin/env python3
"""Agent Runtime Atlas: low-risk, offline, stdlib-only environment probe.

Default execution is passive. Optional execution and temporary writes require
explicit flags. No network calls, credential access, or privilege changes.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROBE_SCHEMA = "agent-runtime-atlas/probe/v1"
COMMANDS = {
    "shell": ["sh", "-c", "printf atlas-ok"],
    "python": [sys.executable, "-c", "print(2 + 2)"],
    "node": ["node", "-e", "process.stdout.write(String(2 + 2))"],
    "git": ["git", "--version"],
}
TOOL_NAMES = ["python", "node", "npm", "git", "gcc", "clang", "go", "java", "ffmpeg", "cargo", "rustc", "jq", "rg", "curl"]


def temp_roundtrip(directory: str) -> dict:
    if not Path(directory).is_dir():
        return {"status": "blocked", "reason": "directory_absent"}
    try:
        with tempfile.TemporaryDirectory(prefix="atlas-probe-", dir=directory) as sandbox:
            target = Path(sandbox) / "roundtrip.txt"
            target.write_text("atlas-local-write-test\n", encoding="utf-8")
            passed = target.read_text(encoding="utf-8") == "atlas-local-write-test\n"
        return {"status": "verified" if passed else "blocked", "roundtrip": passed, "cleanup": "automatic"}
    except (OSError, PermissionError) as exc:
        return {"status": "blocked", "error_type": type(exc).__name__}


def command_probe(name: str, argv: list[str]) -> dict:
    if shutil.which(argv[0]) is None:
        return {"status": "blocked", "reason": "executable_not_on_PATH"}
    try:
        outcome = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                 timeout=4, check=False)
        return {"status": "verified" if outcome.returncode == 0 else "blocked",
                "exit_code": outcome.returncode,
                "stdout": outcome.stdout.strip()[:120],
                "stderr_present": bool(outcome.stderr)}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "blocked", "error_type": type(exc).__name__}


def collect(allow_temp_write: bool = False, allow_exec: bool = False) -> dict:
    os_info = {"system": platform.system(), "release": platform.release(),
               "machine": platform.machine(), "python": platform.python_version()}
    try:
        distro = platform.freedesktop_os_release()
        os_info["distribution"] = distro.get("PRETTY_NAME", "unknown")
    except (OSError, AttributeError):
        os_info["distribution"] = "unknown"
    result = {
        "schema": PROBE_SCHEMA,
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "current isolated invocation only; not another agent or future session",
        "platform": os_info,
        "effective_uid_zero": (os.geteuid() == 0) if hasattr(os, "geteuid") else None,
        "cpu_count_reported": os.cpu_count(),
        "tools_on_path": {name: shutil.which(name) is not None for name in TOOL_NAMES},
        "temporary_files": {},
        "subprocesses": {},
        "not_tested": ["outbound_network", "dns", "host_privileges", "cross_session_persistence",
                       "package_installation", "connector_permissions", "github_write"],
        "safety": {"reads_credentials": False, "connects_to_network": False,
                   "changes_privileges": False, "runs_untrusted_code": False},
    }
    for directory in ("/mnt/data", "/tmp"):
        result["temporary_files"][directory] = (temp_roundtrip(directory) if allow_temp_write
            else {"status": "not_tested", "reason": "requires_--allow-temp-write"})
    for name, command in COMMANDS.items():
        result["subprocesses"][name] = (command_probe(name, command) if allow_exec
            else {"status": "not_tested", "reason": "requires_--allow-exec"})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-temp-write", action="store_true", help="Write and delete isolated temporary test files")
    parser.add_argument("--allow-exec", action="store_true", help="Run four fixed, benign subprocess commands")
    parser.add_argument("--output", type=Path, help="Create a new JSON file (refuses to overwrite)")
    args = parser.parse_args()
    output = json.dumps(collect(args.allow_temp_write, args.allow_exec), indent=2, sort_keys=True) + "\n"
    if args.output:
        try:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(output)
        except OSError as exc:
            print(f"Output not written: {type(exc).__name__}", file=sys.stderr)
            return 1
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
