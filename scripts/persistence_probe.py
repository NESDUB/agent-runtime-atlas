#!/usr/bin/env python3
"""Agent Runtime Atlas offline persistence probe (non-secret markers only).

A seed writes a marker using exclusive creation. A check reads a pre-existing
marker and compares the exact byte hash; it never creates missing files.
This does NOT attest that a call was made in a separate session.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "agent-runtime-atlas/persistence-marker/v1"
PAYLOAD = "nonsecret Jim-Gemma persistence check; no credentials"


def marker_data(marker_id: str) -> dict:
    return {
        "schema": SCHEMA,
        "marker_id": marker_id,
        "payload": PAYLOAD,
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def serialize(marker: dict) -> bytes:
    return (json.dumps(marker, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def seed(path: Path, marker_id: str) -> dict:
    content = serialize(marker_data(marker_id))
    try:
        with path.open("xb") as out:
            out.write(content)
    except (OSError, ValueError) as exc:
        return {"status": "blocked", "error_category": type(exc).__name__, "operation": "seed"}
    return {"status": "seeded", "path": str(path), "marker_id": marker_id,
            "sha256": digest(content), "byte_count": len(content)}


def check(path: Path, marker_id: str, expected_sha256: str) -> dict:
    try:
        content = path.read_bytes()
    except OSError as exc:
        return {"status": "blocked", "error_category": type(exc).__name__, "operation": "check"}
    try:
        marker = json.loads(content)
    except (ValueError, UnicodeDecodeError) as exc:
        return {"status": "blocked", "error_category": type(exc).__name__, "operation": "parse"}
    valid_schema = isinstance(marker, dict) and marker.get("schema") == SCHEMA
    valid_id = isinstance(marker, dict) and marker.get("marker_id") == marker_id
    valid_hash = digest(content) == expected_sha256
    return {"status": "verified_read" if valid_schema and valid_id and valid_hash else "mismatch",
            "path": str(path), "marker_id_matches": bool(valid_id), "schema_matches": bool(valid_schema),
            "sha256_matches": bool(valid_hash), "observed_sha256": digest(content)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    s = commands.add_parser("seed", help="Explicitly create harmless marker once; refuses overwrite")
    s.add_argument("--path", type=Path, required=True)
    s.add_argument("--marker-id", required=True)
    c = commands.add_parser("check", help="Read-only verify; NEVER create missing marker")
    c.add_argument("--path", type=Path, required=True)
    c.add_argument("--marker-id", required=True)
    c.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()
    result = (seed(args.path, args.marker_id) if args.command == "seed" else
              check(args.path, args.marker_id, args.expected_sha256))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"seeded", "verified_read"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
