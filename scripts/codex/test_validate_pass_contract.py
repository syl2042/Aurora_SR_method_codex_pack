#!/usr/bin/env python3
import unittest

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


if __name__ == "__main__":
    unittest.main()
