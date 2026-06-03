#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

import audit_sr_task_contracts


class AuditSrTaskContractsTest(unittest.TestCase):
    def make_root(self) -> tempfile.TemporaryDirectory:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        task = root / "docs/codex/tasks/2026-05-27_legacy"
        task.mkdir(parents=True)
        (task / "task_plan.md").write_text("# Legacy task\n\n## Objectif\nFaire un test.\n", encoding="utf-8")
        (task / "progress.md").write_text("- done ancien\n", encoding="utf-8")
        return tmp

    def test_read_only_reports_missing_contract(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            result = audit_sr_task_contracts.audit(root)
            contract = root / "docs/codex/tasks/2026-05-27_legacy/sr_contract.json"
            self.assertEqual(1, result["legacy_tasks"])
            self.assertEqual(1, result["missing_sr_contract"])
            self.assertFalse(contract.exists())

    def test_write_creates_valid_contract_without_deleting_legacy(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            result = audit_sr_task_contracts.audit(root, write=True)
            task = root / "docs/codex/tasks/2026-05-27_legacy"
            contract = task / "sr_contract.json"
            self.assertEqual(1, result["created"])
            self.assertTrue(contract.exists())
            self.assertTrue((task / "task_plan.md").exists())
            valid, errors, warnings = audit_sr_task_contracts.validate_contract(contract)
            self.assertTrue(valid, errors)
            self.assertEqual([], warnings)

    def test_existing_contract_is_not_overwritten_by_default(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            task = root / "docs/codex/tasks/2026-05-27_legacy"
            contract = task / "sr_contract.json"
            contract.write_text('{"schema_version": "custom"}\n', encoding="utf-8")
            result = audit_sr_task_contracts.audit(root, write=True)
            self.assertEqual(0, result["created"])
            self.assertEqual('{"schema_version": "custom"}\n', contract.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
