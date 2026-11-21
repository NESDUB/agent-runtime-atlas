"""Passive-only safety tests for the Agent Runtime Atlas probe."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import probe_runtime


class PassiveSafetyTests(unittest.TestCase):
    def test_default_marks_stateful_probes_unexecuted(self):
        report = probe_runtime.collect()
        self.assertEqual(report["schema"], "agent-runtime-atlas/probe/v1")
        self.assertTrue(all(row["status"] == "not_tested" for row in report["temporary_files"].values()))
        self.assertTrue(all(row["status"] == "not_tested" for row in report["subprocesses"].values()))
        self.assertFalse(report["safety"]["connects_to_network"])
        self.assertFalse(report["safety"]["reads_credentials"])

    def test_fixed_commands_are_benign(self):
        self.assertEqual(set(probe_runtime.COMMANDS), {"shell", "python", "node", "git"})
        self.assertEqual(probe_runtime.COMMANDS["git"], ["git", "--version"])


if __name__ == "__main__":
    unittest.main()
