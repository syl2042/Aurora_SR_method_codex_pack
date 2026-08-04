#!/usr/bin/env python3
import unittest

import validate_loop_contract


def valid_contract() -> dict:
    return {
        "schema_version": "1.0",
        "task_id": "2026-05-29_example",
        "task_type": "maintenance",
        "status_decision": "done",
        "evidence_gate": {"done": True, "sources_read": ["AGENTS.md"]},
        "backlog_mutation_gate": {
            "status": "not_applicable",
            "structural_change_detected": False,
            "mutation_required": False,
            "sr_inbox_updated": False,
            "sr_lots_updated": False,
            "affected_lots": [],
            "created_lots": [],
            "reopened_lots": [],
            "blocked_lots": [],
            "superseded_lots": [],
            "not_updated_reason": "No backlog mutation required.",
            "decision": "no_backlog_mutation_required",
        },
        "global_impact_gate": {
            "required": False,
            "status": "not_applicable",
            "surfaces_reviewed": [],
            "impacted_lots": [],
            "new_lots_to_create": [],
            "lots_to_reopen_or_block": [],
            "assumptions": [],
            "open_questions": [],
            "sequencing_recommendation": "not_required",
        },
        "lot_completion_gate": {
            "status": "pass",
            "validated_scope_source": "validation utilisateur",
            "scope_reduction_requested": False,
            "scope_reduction_validated_by_user": False,
            "coverage_table": [
                {
                    "requirement_id": "REQ-001",
                    "requirement": "Verifier la maintenance.",
                    "status": "fait",
                    "proof": ["unit"],
                    "comment": "",
                }
            ],
            "ui_ux_required": False,
            "visual_evidence": [],
            "decision": "done",
        },
        "propagation_gate": {
            "required": False,
            "status": "not_applicable",
            "trigger": "not_applicable",
            "risk_level": "not_applicable",
            "preflight_done": False,
            "human_validation_required": False,
            "human_validation_received": False,
            "changed_symbols": [],
            "affected_surfaces": [],
            "consumers_identified": [],
            "reference_searches": [],
            "remaining_references": [],
            "ignored_references": [],
            "compatibility_strategy": "not_required",
            "verification": [],
            "decision": "not_applicable",
        },
        "implementation": {"app_code_changed": False, "changed_files": []},
        "verification": {"commands_run": ["unit"], "commands_failed": [], "not_run_reason": None},
        "e2e_user_tests": {"required": False, "items": []},
        "memory_updates": {
            "sr_lots_updated": False,
            "current_state_updated": False,
            "task_memory_updated": True,
            "gate_report_updated": True,
        },
        "context_budget": {"checked": True, "status": "green", "next_session_prompt": "not_required"},
        "conversation_transition": {
            "decision": "continue_current",
            "reason": "Contexte vert.",
            "next_session_prompt_path": None,
            "user_message_required": False,
        },
        "resume_protocol": {
            "required": False,
            "mode": "not_required",
            "next_user_prompt": None,
            "default_on_plain_resume": "strict_resume",
            "must_not_code_before_user_validation": False,
        },
    }


class ValidateLoopContractTest(unittest.TestCase):
    def test_maintenance_can_skip_current_state(self) -> None:
        errors, _warnings = validate_loop_contract.validate(valid_contract())
        self.assertEqual([], errors)

    def test_method_task_type_is_valid(self) -> None:
        data = valid_contract()
        data["task_type"] = "method"
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertEqual([], errors)

    def test_upgrade_done_requires_current_state_update(self) -> None:
        data = valid_contract()
        data["task_type"] = "upgrade"
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertTrue(any("current_state_updated true" in error for error in errors), errors)

    def test_upgrade_done_passes_with_current_state_update(self) -> None:
        data = valid_contract()
        data["task_type"] = "upgrade"
        data["memory_updates"]["current_state_updated"] = True
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertEqual([], errors)

    def test_realign_user_testing_requires_current_state_update(self) -> None:
        data = valid_contract()
        data["task_type"] = "realign"
        data["status_decision"] = "user_testing"
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertTrue(any("current_state_updated true" in error for error in errors), errors)

    def test_upgrade_repair_can_skip_current_state_temporarily(self) -> None:
        data = valid_contract()
        data["task_type"] = "upgrade"
        data["status_decision"] = "repair"
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertEqual([], errors)

    def test_structural_change_requires_global_impact(self) -> None:
        data = valid_contract()
        data["backlog_mutation_gate"]["structural_change_detected"] = True
        data["backlog_mutation_gate"]["mutation_required"] = True
        data["backlog_mutation_gate"]["sr_lots_updated"] = True
        data["memory_updates"]["sr_lots_updated"] = True
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertTrue(any("global_impact_gate.required true" in error for error in errors), errors)

    def test_required_global_impact_needs_surfaces(self) -> None:
        data = valid_contract()
        data["global_impact_gate"]["required"] = True
        data["global_impact_gate"]["status"] = "pass"
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertTrue(any("surfaces_reviewed must not be empty" in error for error in errors), errors)

    def test_done_rejects_partial_completion_row(self) -> None:
        data = valid_contract()
        data["lot_completion_gate"]["coverage_table"][0]["status"] = "partiel"
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertTrue(any("incomplete lot_completion_gate rows" in error for error in errors), errors)

    def test_done_ui_requires_visual_or_e2e_evidence(self) -> None:
        data = valid_contract()
        data["lot_completion_gate"]["ui_ux_required"] = True
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertTrue(any("UI/UX requirements requires" in error for error in errors), errors)

    def test_done_requires_propagation_pass_when_required(self) -> None:
        data = valid_contract()
        data["propagation_gate"]["required"] = True
        data["propagation_gate"]["status"] = "pending"
        data["propagation_gate"]["risk_level"] = "medium"
        data["propagation_gate"]["decision"] = "repair"
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertTrue(any("propagation_gate.status pass" in error for error in errors), errors)

    def test_high_risk_propagation_requires_consumers_and_verification(self) -> None:
        data = valid_contract()
        data["propagation_gate"].update(
            {
                "required": True,
                "status": "pass",
                "risk_level": "high",
                "preflight_done": True,
                "human_validation_required": True,
                "human_validation_received": True,
                "changed_symbols": ["old_name -> new_name"],
                "reference_searches": ["rg old_name", "rg new_name"],
                "decision": "pass",
            }
        )
        errors, _warnings = validate_loop_contract.validate(data)
        self.assertTrue(any("consumers_identified" in error for error in errors), errors)
        self.assertTrue(any("propagation_gate.verification" in error for error in errors), errors)

    def test_missing_propagation_gate_is_legacy_warning(self) -> None:
        data = valid_contract()
        del data["propagation_gate"]
        errors, warnings = validate_loop_contract.validate(data)
        self.assertEqual([], errors)
        self.assertTrue(any("legacy contract" in warning for warning in warnings), warnings)


if __name__ == "__main__":
    unittest.main()
