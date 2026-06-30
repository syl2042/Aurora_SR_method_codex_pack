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
    }


class ValidateLotContractTest(unittest.TestCase):
    def test_valid_lot_with_impact_fields_passes(self) -> None:
        errors = validate_lot_contract.validate_lot(valid_lot(), 0)
        self.assertEqual([], errors)

    def test_required_global_impact_needs_surfaces(self) -> None:
        lot = valid_lot()
        lot["global_impact"]["required"] = True
        lot["global_impact"]["status"] = "pass"
        errors = validate_lot_contract.validate_lot(lot, 0)
        self.assertTrue(any("surfaces_reviewed must not be empty" in error for error in errors), errors)

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
