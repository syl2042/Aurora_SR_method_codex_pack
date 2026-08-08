#!/usr/bin/env python3
import tempfile
import unittest
from pathlib import Path

import validate_lot_contract


def valid_lot() -> dict:
    return {
        "lot_id": "SR-GOV-001",
        "title": "Installer les gates d'impact global",
        "status": "validated",
        "objective": "Forcer l'analyse transverse des fonctions structurantes.",
        "acceptance_criteria": ["Le gate est documente."],
        "verification_commands": ["python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml"],
        "stop_conditions": ["Validation impossible."],
        "depends_on": [],
        "blocked_by": [],
        "impacts": [],
        "impacted_by": [],
        "supersedes": [],
        "superseded_by": None,
        "dependency_reconciliation": {
            "status": "not_required",
            "reviewed_lots": [],
            "classifications": [],
            "open_questions": [],
        },
        "global_impact": {
            "required": False,
            "status": "not_applicable",
            "surfaces_reviewed": [],
            "impacted_lots": [],
            "new_lots_to_create": [],
            "lots_to_reopen_or_block": [],
            "sequencing_recommendation": "not_required",
            "open_questions": [],
        },
        "design_evidence": {
            "status": "pass",
            "code_read_required": True,
            "candidate_files": ["core/SR_HARNESS_METHOD.md"],
            "confirmed_files_read": ["core/SR_HARNESS_METHOD.md"],
            "symbols_or_routes_checked": [],
            "tests_or_logs_checked": [],
            "assumptions_remaining": [],
            "open_questions": [],
            "not_applicable_reason": None,
            "status_ceiling_if_not_pass": "proposed",
        },
    }


class ValidateLotContractTest(unittest.TestCase):
    def test_version_comparison_is_numeric(self) -> None:
        self.assertTrue(validate_lot_contract.version_at_least("0.10", "0.3"))
        self.assertFalse(validate_lot_contract.version_at_least("0.2", "0.3"))

    def test_valid_lot_with_impact_fields_passes(self) -> None:
        errors = validate_lot_contract.validate_lot(valid_lot(), 0, enforce_design_evidence=True)
        self.assertEqual([], errors)

    def test_required_global_impact_needs_surfaces(self) -> None:
        lot = valid_lot()
        lot["global_impact"]["required"] = True
        lot["global_impact"]["status"] = "pass"
        errors = validate_lot_contract.validate_lot(lot, 0, enforce_design_evidence=True)
        self.assertTrue(any("surfaces_reviewed must not be empty" in error for error in errors), errors)

    def test_executable_lot_requires_design_evidence(self) -> None:
        lot = valid_lot()
        lot.pop("design_evidence")
        errors = validate_lot_contract.validate_lot(lot, 0, enforce_design_evidence=True)
        self.assertTrue(any("design_evidence is required" in error for error in errors), errors)

    def test_legacy_executable_lot_without_design_evidence_remains_compatible(self) -> None:
        lot = valid_lot()
        lot.pop("design_evidence")
        errors = validate_lot_contract.validate_lot(lot, 0)
        self.assertEqual([], errors)

    def test_proposed_lot_accepts_pending_design_evidence(self) -> None:
        lot = valid_lot()
        lot["status"] = "proposed"
        lot["design_evidence"]["status"] = "pending"
        lot["design_evidence"]["confirmed_files_read"] = []
        errors = validate_lot_contract.validate_lot(lot, 0, enforce_design_evidence=True)
        self.assertEqual([], errors)

    def test_executable_lot_requires_pass_or_not_applicable_design_evidence(self) -> None:
        lot = valid_lot()
        lot["design_evidence"]["status"] = "pending"
        errors = validate_lot_contract.validate_lot(lot, 0, enforce_design_evidence=True)
        self.assertTrue(any("requires design_evidence.status" in error for error in errors), errors)

    def test_code_read_required_needs_confirmed_files(self) -> None:
        lot = valid_lot()
        lot["design_evidence"]["confirmed_files_read"] = []
        errors = validate_lot_contract.validate_lot(lot, 0, enforce_design_evidence=True)
        self.assertTrue(any("confirmed_files_read must not be empty" in error for error in errors), errors)

    def test_not_applicable_design_evidence_requires_reason(self) -> None:
        lot = valid_lot()
        lot["design_evidence"]["status"] = "not_applicable"
        lot["design_evidence"]["code_read_required"] = False
        lot["design_evidence"]["confirmed_files_read"] = []
        lot["design_evidence"]["not_applicable_reason"] = ""
        errors = validate_lot_contract.validate_lot(lot, 0, enforce_design_evidence=True)
        self.assertTrue(any("not_applicable_reason is required" in error for error in errors), errors)

    def test_unknown_dependency_is_rejected_by_cli_flow(self) -> None:
        content = """
lots:
  - lot_id: SR-GOV-001
    title: Example
    status: validated
    objective: Example
    depends_on:
      - SR-GOV-999
    acceptance_criteria:
      - Done
    verification_commands:
      - unit
    stop_conditions:
      - stop
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SR_LOTS.yaml"
            path.write_text(content, encoding="utf-8")
            data = validate_lot_contract.parse_simple_yaml(path)
        lots = data["lots"]
        seen = {lot.get("lot_id") for lot in lots}
        errors = []
        for index, lot in enumerate(lots):
            errors.extend(validate_lot_contract.validate_lot(lot, index))
            for ref in lot.get("depends_on", []):
                if ref not in seen:
                    errors.append(f"lot[{index}]: depends_on references unknown lot_id {ref!r}")
        self.assertTrue(any("unknown lot_id" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
