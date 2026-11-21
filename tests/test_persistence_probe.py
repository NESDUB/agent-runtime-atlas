"""Offline, isolated local behavioral tests for the marker probe."""
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import persistence_probe as p

class PersistenceTests(unittest.TestCase):
    def test_seed_exclusive_and_check(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'marker.json'
            seeded = p.seed(path, 'safe-marker')
            self.assertEqual(seeded['status'], 'seeded')
            self.assertEqual(p.check(path, 'safe-marker', seeded['sha256'])['status'], 'verified_read')
            self.assertEqual(p.seed(path, 'safe-marker')['status'], 'blocked')
            self.assertEqual(p.check(path, 'different', seeded['sha256'])['status'], 'mismatch')
            self.assertEqual(p.check(path, 'safe-marker', '0'*64)['status'], 'mismatch')
    def test_missing_file_is_never_created_by_check(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'missing.json'
            self.assertEqual(p.check(path, 'safe-marker', '0'*64)['status'], 'blocked')
            self.assertFalse(path.exists())
if __name__ == '__main__':
    unittest.main()
