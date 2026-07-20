#!/usr/bin/env python3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import audit_sr_project
import validate_pass_contract


def valid_pass() -> dict:
    return {
        "pass_id": "NR-PASS-001",
        "title": "Core foundation",
        "status": "validated",
        "priority": "high",
        "lots": ["NR-03", "NR-09", "NR-04"],
        "sequencing": {
            "strategy": "topological_with_foundation_first",
            "rationale": ["NR-03 creates the DB foundation."],
            "dependency_overrides": [],
            "open_questions": [],
        },
        "preflight": {
            "required_before_start": ["NR-02 E2E confirmed."],
            "secrets_required": [],
            "external_actions_required": [],
            "human_validation_required": ["migration"],
            "migrations_required": ["initial additive migration"],
            "open_questions": [],
        },
        "shared_sources": ["docs/CURRENT_STATE.md"],
        "e2e_strategy": {
            "mode": "grouped_at_pass_end",
            "items": ["Login, migration, shell and API smoke pass."],
        },
        "stop_on": ["gate_failure"],
        "notes": [],
    }


def lots() -> dict[str, dict]:
    return {
        "NR-02": {"lot_id": "NR-02", "status": "done", "depends_on": []},
        "NR-03": {"lot_id": "NR-03", "status": "validated", "depends_on": ["NR-02"]},
        "NR-09": {"lot_id": "NR-09", "status": "validated", "depends_on": ["NR-03"]},
        "NR-04": {"lot_id": "NR-04", "status": "validated", "depends_on": ["NR-03"]},
    }


def valid_pass_item(pass_id: str, status: str, lot_ids: list[str]) -> dict:
    item = valid_pass()
    item["pass_id"] = pass_id
    item["status"] = status
    item["lots"] = lot_ids
    return item


def inter_pass_lots(status_a: str = "proposed", status_b: str = "proposed") -> dict[str, dict]:
    return {
        "LOT-A": {"lot_id": "LOT-A", "status": status_a, "depends_on": []},
        "LOT-B": {"lot_id": "LOT-B", "status": status_b, "depends_on": ["LOT-A"]},
    }


class ValidatePassContractTest(unittest.TestCase):
    def test_valid_pass_with_finished_external_dependency_passes(self) -> None:
        errors = validate_pass_contract.validate_pass(valid_pass(), 0, lots())
        self.assertEqual([], errors)

    def test_unknown_lot_is_rejected(self) -> None:
        item = valid_pass()
        item["lots"] = ["NR-999"]
        errors = validate_pass_contract.validate_pass(item, 0, lots())
        self.assertTrue(any("unknown lot_id" in error for error in errors), errors)

    def test_unfinished_external_dependency_is_rejected(self) -> None:
        project_lots = lots()
        project_lots["NR-02"]["status"] = "validated"
        errors = validate_pass_contract.validate_pass(valid_pass(), 0, project_lots)
        self.assertTrue(any("unfinished lot 'NR-02' outside pass" in error for error in errors), errors)

    def test_dependency_order_is_rejected_without_override(self) -> None:
        item = valid_pass()
        item["lots"] = ["NR-04", "NR-03"]
        errors = validate_pass_contract.validate_pass(item, 0, lots())
        self.assertTrue(any("appears before dependency" in error for error in errors), errors)

    def test_dependency_override_must_name_lot_and_dependency(self) -> None:
        item = valid_pass()
        item["lots"] = ["NR-04", "NR-03"]
        item["sequencing"]["dependency_overrides"] = ["generic exception"]
        errors = validate_pass_contract.validate_pass(item, 0, lots())
        self.assertTrue(any("appears before dependency" in error for error in errors), errors)

    def test_precise_dependency_override_allows_named_internal_order_exception(self) -> None:
        item = valid_pass()
        item["lots"] = ["NR-04", "NR-03"]
        item["sequencing"]["dependency_overrides"] = ["NR-04 may run before NR-03 because schema is pre-existing"]
        errors = validate_pass_contract.validate_pass(item, 0, lots())
        self.assertFalse(any("appears before dependency" in error for error in errors), errors)

    def test_grouped_e2e_requires_items(self) -> None:
        item = valid_pass()
        item["e2e_strategy"]["items"] = []
        errors = validate_pass_contract.validate_pass(item, 0, lots())
        self.assertTrue(any("e2e_strategy.items" in error for error in errors), errors)

    def test_pass_subset_parser_without_pyyaml(self) -> None:
        data = validate_pass_contract.parse_pass_subset(
            """
passes:
  - pass_id: NR-PASS-001
    title: Core foundation
    status: validated
    lots:
      - NR-03
    preflight:
      required_before_start:
        - Auth confirmed
      secrets_required: []
    e2e_strategy:
      mode: grouped_at_pass_end
      items:
        - Login smoke
    stop_on:
      - gate_failure
"""
        )
        self.assertEqual("NR-PASS-001", data["passes"][0]["pass_id"])
        self.assertEqual(["NR-03"], data["passes"][0]["lots"])
        self.assertEqual("grouped_at_pass_end", data["passes"][0]["e2e_strategy"]["mode"])

    def test_proposed_inter_pass_dependency_to_earlier_proposed_pass_is_accepted(self) -> None:
        passes = [
            valid_pass_item("MIA-PASS-001", "proposed", ["LOT-A"]),
            valid_pass_item("MIA-PASS-002", "proposed", ["LOT-B"]),
        ]
        self.assertEqual([], validate_pass_contract.validate_passes(passes, inter_pass_lots()))

    def test_planned_inter_pass_dependency_to_earlier_planned_pass_is_accepted(self) -> None:
        passes = [
            valid_pass_item("MIA-PASS-001", "planned", ["LOT-A"]),
            valid_pass_item("MIA-PASS-002", "planned", ["LOT-B"]),
        ]
        self.assertEqual([], validate_pass_contract.validate_passes(passes, inter_pass_lots("planned", "planned")))

    def test_validated_pass_requires_earlier_inter_pass_dependency_to_be_finished(self) -> None:
        passes = [
            valid_pass_item("MIA-PASS-001", "planned", ["LOT-A"]),
            valid_pass_item("MIA-PASS-002", "validated", ["LOT-B"]),
        ]
        errors = validate_pass_contract.validate_passes(passes, inter_pass_lots("planned", "validated"))
        self.assertTrue(any("unfinished lot 'LOT-A' in earlier pass" in error for error in errors), errors)

    def test_in_progress_pass_requires_earlier_inter_pass_dependency_to_be_finished(self) -> None:
        passes = [
            valid_pass_item("MIA-PASS-001", "planned", ["LOT-A"]),
            valid_pass_item("MIA-PASS-002", "in_progress", ["LOT-B"]),
        ]
        errors = validate_pass_contract.validate_passes(passes, inter_pass_lots("planned", "in_progress"))
        self.assertTrue(any("unfinished lot 'LOT-A' in earlier pass" in error for error in errors), errors)

    def test_dependency_to_later_pass_is_rejected(self) -> None:
        passes = [
            valid_pass_item("MIA-PASS-001", "planned", ["LOT-B"]),
            valid_pass_item("MIA-PASS-002", "planned", ["LOT-A"]),
        ]
        errors = validate_pass_contract.validate_passes(passes, inter_pass_lots("planned", "planned"))
        self.assertTrue(any("depends on lot 'LOT-A' in later pass" in error for error in errors), errors)

    def test_dependency_outside_all_passes_must_be_finished(self) -> None:
        project_lots = {
            "LOT-A": {"lot_id": "LOT-A", "status": "planned", "depends_on": []},
            "LOT-B": {"lot_id": "LOT-B", "status": "planned", "depends_on": ["LOT-A"]},
        }
        passes = [valid_pass_item("MIA-PASS-001", "planned", ["LOT-B"])]
        errors = validate_pass_contract.validate_passes(passes, project_lots)
        self.assertTrue(any("unfinished lot 'LOT-A' outside pass" in error for error in errors), errors)

    def test_duplicate_lot_across_passes_is_rejected_explicitly(self) -> None:
        passes = [
            valid_pass_item("MIA-PASS-001", "planned", ["LOT-A"]),
            valid_pass_item("MIA-PASS-002", "planned", ["LOT-A"]),
        ]
        errors = validate_pass_contract.validate_passes(passes, inter_pass_lots("planned", "planned"))
        self.assertTrue(any("appears in multiple passes" in error for error in errors), errors)

    def test_audit_pass_contract_accepts_ordered_proposed_inter_pass_dependencies(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            lots_path = root / "SR_LOTS.yaml"
            passes_path = root / "SR_PASSES.yaml"
            lots_path.write_text(
                """
lots:
  - lot_id: LOT-A
    title: Foundation
    status: proposed
    depends_on: []
  - lot_id: LOT-B
    title: Feature
    status: proposed
    depends_on:
      - LOT-A
""",
                encoding="utf-8",
            )
            passes_path.write_text(
                """
passes:
  - pass_id: MIA-PASS-001
    title: Foundation
    status: proposed
    priority: high
    lots:
      - LOT-A
    preflight:
      required_before_start: []
      secrets_required: []
      external_actions_required: []
      human_validation_required: []
      migrations_required: []
      open_questions: []
    e2e_strategy:
      mode: not_required
      items: []
    stop_on:
      - dependency_unresolved
  - pass_id: MIA-PASS-002
    title: Feature
    status: proposed
    priority: high
    lots:
      - LOT-B
    preflight:
      required_before_start: []
      secrets_required: []
      external_actions_required: []
      human_validation_required: []
      migrations_required: []
      open_questions: []
    e2e_strategy:
      mode: not_required
      items: []
    stop_on:
      - dependency_unresolved
""",
                encoding="utf-8",
            )
            self.assertEqual([], audit_sr_project.pass_contract_errors(passes_path, lots_path))


if __name__ == "__main__":
    unittest.main()
