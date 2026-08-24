#!/usr/bin/env python3
import json
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
            self.assertTrue(any("generic" in warning and "normalize" in warning for warning in warnings), warnings)

    def test_existing_contract_is_not_overwritten_by_default(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            task = root / "docs/codex/tasks/2026-05-27_legacy"
            contract = task / "sr_contract.json"
            contract.write_text('{"schema_version": "custom"}\n', encoding="utf-8")
            result = audit_sr_task_contracts.audit(root, write=True)
            self.assertEqual(0, result["created"])
            self.assertEqual('{"schema_version": "custom"}\n', contract.read_text(encoding="utf-8"))

    def test_pre_cutoff_contract_missing_lot_completion_gate_is_legacy_warning(self) -> None:
        with self.make_root() as directory:
            root = Path(directory)
            task = root / "docs/codex/tasks/2026-05-27_legacy"
            contract_data = validate_sr_contract_test_contract()
            del contract_data["lot_completion_gate"]
            del contract_data["gates"]["lot_completion"]
            (task / "sr_contract.json").write_text(
                json.dumps(contract_data, indent=2),
                encoding="utf-8",
            )

            result = audit_sr_task_contracts.audit(root)
            item = result["items"][0]
            self.assertTrue(result["ok"], result)
            self.assertEqual(0, result["invalid_sr_contract"])
            self.assertTrue(item["legacy_compat"])
            self.assertTrue(item["valid"])
            self.assertEqual([], item["errors"])
            self.assertTrue(any("Lot Completion Gate cutoff" in warning for warning in item["warnings"]))

    def test_cutoff_or_newer_contract_missing_lot_completion_gate_stays_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task = root / "docs/codex/tasks/2026-08-08_new"
            task.mkdir(parents=True)
            (task / "task_plan.md").write_text("# New task\n", encoding="utf-8")
            contract_data = validate_sr_contract_test_contract()
            del contract_data["lot_completion_gate"]
            del contract_data["gates"]["lot_completion"]
            (task / "sr_contract.json").write_text(
                json.dumps(contract_data, indent=2),
                encoding="utf-8",
            )

            result = audit_sr_task_contracts.audit(root)
            item = result["items"][0]
            self.assertFalse(result["ok"], result)
            self.assertEqual(1, result["invalid_sr_contract"])
            self.assertFalse(item["legacy_compat"])
            self.assertFalse(item["valid"])
            self.assertTrue(any("lot_completion_gate" in error for error in item["errors"]))


def validate_sr_contract_test_contract() -> dict:
    return {
        "schema_version": "3.0.0",
        "task_id": "2026-05-27_legacy",
        "lot_id": "SR-LEGACY",
        "task_type": "method",
        "status": "done",
        "objective": "Legacy contract.",
        "validated_requests": [
            {
                "id": "REQ-001",
                "source": "legacy",
                "requirement_type": "method",
                "status": "done",
                "coverage": "legacy",
                "files": ["task_plan.md"],
                "verification": [],
                "notes": ["legacy proof"],
            }
        ],
        "lot_completion_gate": {
            "status": "pass",
            "coverage_table": [
                {
                    "requirement_id": "REQ-001",
                    "requirement": "Legacy requirement.",
                    "status": "fait",
                    "proof": ["task_plan.md"],
                }
            ],
            "visual_evidence": [],
            "decision": "done",
        },
        "scope": {"in": ["legacy"], "out": [], "allowed_paths": [], "forbidden_paths": []},
        "product_truth": {"required": True, "items": ["legacy"]},
        "evidence": {"sources_read": ["task_plan.md"], "code_files_read": [], "tests_or_logs": []},
        "skills": {"method": [], "domain": []},
        "plan": [],
        "findings": [],
        "decisions": [],
        "implementation": {"app_code_changed": False, "changed_files": []},
        "verification": {"commands_run": [], "commands_failed": [], "not_run_reason": "legacy"},
        "gates": {"lot_completion": "pass", "propagation": "not_applicable", "verification": "pass"},
        "e2e": {"required": False, "items": []},
        "context": {"status": "green", "report_path": None},
        "transition": {
            "decision": "continue_current",
            "reason": "legacy",
            "next_session_prompt_required": False,
            "next_session_prompt_path": None,
            "next_user_prompt": None,
        },
    }


if __name__ == "__main__":
    unittest.main()
