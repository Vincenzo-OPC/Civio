import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("bank_inventory", Path(__file__).with_name("inventory.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InventoryTest(unittest.TestCase):
    def item(self, **changes):
        return dict(id="TEST-1", stem="Synthetic fixture", options=["A", "B", "C", "D"], correct_option=0, **changes)

    def test_declared_approval_is_preserved_but_does_not_change_content_digest(self):
        draft = module.inspect_item(self.item(status="draft"), "a.json")
        claimed = module.inspect_item(self.item(status="approved", review_status="passed"), "a.json")
        self.assertEqual(draft["content_sha256"], claimed["content_sha256"])
        self.assertNotEqual(draft["item_sha256"], claimed["item_sha256"])
        self.assertEqual("approved", claimed["declared_status"])

    def test_fix_targets_original_identity(self):
        result = module.inspect_item(self.item(fix_of="ORIGINAL-1"), "fix.json")
        self.assertEqual("ORIGINAL-1", result["identity"])
        self.assertEqual("TEST-1", result["declared_id"])

    def test_legacy_ids_never_merge_across_snapshot_files(self):
        item = self.item()
        item["id"] = 462
        a = module.inspect_item(item, "snapshot-a.json")
        b = module.inspect_item(item, "snapshot-b.json")
        self.assertNotEqual(a["identity"], b["identity"])
        self.assertIn("identity-mapping-required", a["flags"])

    def test_duplicate_options_and_boolean_answer_index_are_flagged(self):
        item = self.item()
        item.update(options=[" A ", "a", "B", "C"], correct_option=True)
        result = module.inspect_item(item, "a.json")
        self.assertIn("duplicate-options", result["flags"])
        self.assertIn("invalid-answer-index", result["flags"])

    def test_conflicting_sources_are_reported_without_choosing_a_winner(self):
        a, b = self.item(), self.item()
        b["stem"] = "Changed fixture"
        lock = {"sources": [{"name": "main", "commit": "a", "scope": "all-bank-artifacts"},
                            {"name": "proposal", "commit": "b", "base": "a", "scope": "changed-bank-artifacts"}]}
        def fake_git(root, *args):
            if args[0] in {"ls-tree", "diff"}:
                return b"docs/research/fixture.json\n"
            return json.dumps({"items": [a if args[1].startswith("a:") else b]}).encode()
        with patch.object(module, "git", side_effect=fake_git):
            result = module.inventory(Path("."), lock)
        self.assertEqual(1, result["summary"]["conflicting_identity_groups"])
        self.assertEqual(2, len(result["occurrences"]))
        self.assertEqual("NOT VERIFIED", result["summary"]["runtime_count"])


if __name__ == "__main__":
    unittest.main()
