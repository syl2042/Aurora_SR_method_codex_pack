#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

import validate_sr_contract


def valid_contract() -> dict:
    return {
        "schema_version": "3.0.0",
        "task_id": "2026-05-26_example",
        "lot_id": "SR-CORE-300-CONTRACT-SCHEMA",
        "task_type": "method",
        "status": "done",
        "objective": "Installer un contrat SR vivant.",
        "validated_requests": [
            {
                "id": "REQ-001",
                "source": "validation utilisateur",
                "requirement_type": "method",
                "status": "done",
                "coverage": "schema, template et validateur crees",
                "files": ["scripts/codex/validate_sr_contract.py"],
                "verification": ["python3 scripts/codex/validate_sr_contract.py --file sr_contract.json"],
                "notes": [],
            }
        ],
        "lot_completion_gate": {
            "status": "pass",
            "validated_scope_source": "validation utilisateur",
            "scope_reduction_requested": False,
            "scope_reduction_validated_by_user": False,
            "coverage_table": [
                {
                    "requirement_id": "REQ-001",
                    "requirement": "Installer le contrat SR vivant.",
                    "status": "fait",
                    "proof": ["scripts/codex/validate_sr_contract.py", "unit"],
                    "comment": "",
                }
            ],
            "ui_ux_required": False,
            "visual_evidence": [],
            "decision": "done",
        },
        "scope": {"in": ["schema"], "out": [], "allowed_paths": [], "forbidden_paths": []},
        "product_truth": {"required": True, "items": ["les fichiers legacy restent historiques"]},
        "backlog_mutation": {
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
        "global_impact": {
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
        "propagation": {
            "required": False,
            "status": "not_applicable",
            "trigger": "not_applicable",
            "risk_level": "not_applicable",
            "preflight": {
                "done": False,
                "summary": "Aucun changement de symbole ou contrat partage.",
                "human_validation_required": False,
                "human_validation_received": False,
            },
            "changed_symbols": [],
            "affected_surfaces": [],
            "consumers_checked": [],
            "reference_searches": [],
            "remaining_references": [],
            "ignored_references": [],
            "compatibility_strategy": "not_required",
            "verification": [],
            "decision": "not_applicable",
        },
        "evidence": {"sources_read": ["docs/codex/SR_METHOD.md"], "code_files_read": [], "tests_or_logs": []},
        "ui_validation": {
            "required": False,
            "routes": [],
            "test_readiness": {
                "status": "not_applicable",
                "auth_required": False,
                "auth_mode": "none",
                "state_available": None,
                "state_valid": None,
                "login_redirect_detected": False,
                "blocked_reason": None,
            },
            "visual_evidence": {
                "status": "not_applicable",
                "routes": [],
                "viewports": [],
                "screenshots": [],
                "report_file": None,
                "console_errors": 0,
                "page_errors": 0,
                "request_failed": 0,
                "horizontal_overflow_detected": False,
                "unexpected_login_redirect": False,
            },
        },
        "skills": {"method": ["aurora-lot-runner"], "domain": []},
        "plan": ["Creer le schema."],
        "findings": [],
        "decisions": [],
        "implementation": {"app_code_changed": False, "changed_files": ["scripts/codex/validate_sr_contract.py"]},
        "verification": {"commands_run": ["unit"], "commands_failed": [], "not_run_reason": None},
        "gates": {
            "evidence": "pass",
            "lot_completion": "pass",
            "propagation": "not_applicable",
            "ui_test_readiness": "not_applicable",
            "ui_visual_evidence": "not_applicable",
            "verification": "pass",
            "context_budget": "pass",
        },
        "e2e": {"required": True, "items": ["Relire le contrat et verifier les requetes couvertes."]},
        "context": {"status": "green", "report_path": None},
        "transition": {
            "decision": "continue_current",
            "reason": "Contexte vert.",
            "next_session_prompt_required": False,
            "next_session_prompt_path": None,
            "next_user_prompt": None,
        },
    }


class ValidateSrContractTest(unittest.TestCase):
    def assert_errors(self, data: dict, expected: str) -> None:
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_valid_contract_passes(self) -> None:
        errors, warnings = validate_sr_contract.validate(valid_contract())
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_done_rejects_open_request(self) -> None:
        data = valid_contract()
        data["validated_requests"][0]["status"] = "todo"
        self.assert_errors(data, "status done requires all validated_requests")

    def test_rejects_duplicate_request_ids(self) -> None:
        data = valid_contract()
        data["validated_requests"].append(dict(data["validated_requests"][0]))
        self.assert_errors(data, "duplicated")

    def test_product_truth_required_needs_items(self) -> None:
        data = valid_contract()
        data["product_truth"]["items"] = []
        self.assert_errors(data, "product_truth.items must not be empty")

    def test_e2e_required_needs_items(self) -> None:
        data = valid_contract()
        data["e2e"]["items"] = []
        self.assert_errors(data, "e2e.items must not be empty")

    def test_orange_context_requires_transition(self) -> None:
        data = valid_contract()
        data["context"]["status"] = "orange"
        self.assert_errors(data, "orange context requires transition.decision")

    def test_next_prompt_required_needs_path_and_prompt(self) -> None:
        data = valid_contract()
        data["transition"]["decision"] = "recommend_new_conversation"
        data["transition"]["next_session_prompt_required"] = True
        self.assert_errors(data, "transition.next_session_prompt_path is required")

    def test_cli_validates_temp_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sr_contract.json"
            path.write_text(json.dumps(valid_contract()), encoding="utf-8")
            data = validate_sr_contract.load_contract(path)
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)

    def test_structural_change_requires_global_impact(self) -> None:
        data = valid_contract()
        data["backlog_mutation"]["structural_change_detected"] = True
        data["backlog_mutation"]["mutation_required"] = True
        data["backlog_mutation"]["sr_lots_updated"] = True
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("global_impact.required true" in error for error in errors), errors)

    def test_moved_to_new_lot_requires_target(self) -> None:
        data = valid_contract()
        data["validated_requests"][0]["status"] = "moved_to_new_lot"
        data["validated_requests"][0]["coverage"] = "Sortie du lot courant sans cible explicite."
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("moved_to_new_lot requests require" in error for error in errors), errors)

    def test_done_rejects_partial_completion_row(self) -> None:
        data = valid_contract()
        data["lot_completion_gate"]["coverage_table"][0]["status"] = "partiel"
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("incomplete lot_completion_gate rows" in error for error in errors), errors)

    def test_done_ui_requires_visual_or_e2e_evidence(self) -> None:
        data = valid_contract()
        data["validated_requests"][0]["requirement_type"] = "ui_ux"
        data["e2e"]["items"] = []
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("UI/UX requirements requires" in error for error in errors), errors)

    def test_done_requires_propagation_pass_when_required(self) -> None:
        data = valid_contract()
        data["propagation"]["required"] = True
        data["propagation"]["status"] = "pending"
        data["propagation"]["risk_level"] = "medium"
        data["propagation"]["decision"] = "repair"
        data["gates"]["propagation"] = "pending"
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("propagation.status pass" in error for error in errors), errors)

    def test_high_risk_propagation_requires_consumers_and_verification(self) -> None:
        data = valid_contract()
        data["propagation"].update(
            {
                "required": True,
                "status": "pass",
                "risk_level": "high",
                "decision": "pass",
                "changed_symbols": ["old_name -> new_name"],
                "reference_searches": ["rg old_name", "rg new_name"],
            }
        )
        data["propagation"]["preflight"]["done"] = True
        data["propagation"]["preflight"]["human_validation_required"] = True
        data["propagation"]["preflight"]["human_validation_received"] = True
        data["gates"]["propagation"] = "pass"
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("consumers_checked" in error for error in errors), errors)
        self.assertTrue(any("propagation.verification" in error for error in errors), errors)

    def test_missing_propagation_is_legacy_warning(self) -> None:
        data = valid_contract()
        del data["propagation"]
        data["gates"]["propagation"] = "not_applicable"
        errors, warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)
        self.assertTrue(any("legacy contract" in warning for warning in warnings), warnings)

    def test_done_ui_validation_required_with_pass_evidence_is_valid(self) -> None:
        data = valid_contract()
        data["validated_requests"][0]["requirement_type"] = "ui_ux"
        data["lot_completion_gate"]["ui_ux_required"] = True
        data["lot_completion_gate"]["visual_evidence"] = ["output/playwright/dashboard/desktop.png"]
        data["ui_validation"] = {
            "required": True,
            "routes": ["/dashboard"],
            "test_readiness": {
                "status": "pass",
                "auth_required": False,
                "auth_mode": "none",
                "state_available": None,
                "state_valid": None,
                "login_redirect_detected": False,
                "blocked_reason": None,
            },
            "visual_evidence": {
                "status": "pass",
                "routes": ["/dashboard"],
                "viewports": ["desktop"],
                "screenshots": ["output/playwright/dashboard/desktop.png"],
                "report_file": "output/playwright/ui-verification-report.json",
                "console_errors": 0,
                "page_errors": 0,
                "request_failed": 0,
                "horizontal_overflow_detected": False,
                "unexpected_login_redirect": False,
            },
        }
        data["gates"]["ui_test_readiness"] = "pass"
        data["gates"]["ui_visual_evidence"] = "pass"
        errors, warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_done_ui_validation_required_rejects_missing_visual_evidence(self) -> None:
        data = valid_contract()
        data["ui_validation"]["required"] = True
        data["ui_validation"]["test_readiness"]["status"] = "pass"
        data["ui_validation"]["visual_evidence"]["status"] = "not_applicable"
        data["gates"]["ui_test_readiness"] = "pass"
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("visual_evidence.status pass" in error for error in errors), errors)
        self.assertTrue(any("visual_evidence.report_file" in error for error in errors), errors)

    def test_done_ui_validation_required_rejects_readiness_fail(self) -> None:
        data = valid_contract()
        data["ui_validation"]["required"] = True
        data["ui_validation"]["test_readiness"]["status"] = "fail"
        data["ui_validation"]["visual_evidence"].update(
            {
                "status": "pass",
                "screenshots": ["output/playwright/dashboard/desktop.png"],
                "report_file": "output/playwright/ui-verification-report.json",
            }
        )
        data["gates"]["ui_visual_evidence"] = "pass"
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("test_readiness.status pass" in error for error in errors), errors)

    def test_done_ui_validation_rejects_login_redirect(self) -> None:
        data = valid_contract()
        data["ui_validation"]["required"] = True
        data["ui_validation"]["test_readiness"].update({"status": "pass", "login_redirect_detected": True})
        data["ui_validation"]["visual_evidence"].update(
            {
                "status": "pass",
                "screenshots": ["output/playwright/login/desktop.png"],
                "report_file": "output/playwright/ui-verification-report.json",
                "unexpected_login_redirect": True,
            }
        )
        data["gates"]["ui_test_readiness"] = "pass"
        data["gates"]["ui_visual_evidence"] = "pass"
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("login redirect" in error for error in errors), errors)

    def test_user_testing_with_blocked_ui_requires_e2e_items(self) -> None:
        data = valid_contract()
        data["status"] = "user_testing"
        data["lot_completion_gate"]["decision"] = "user_testing"
        data["ui_validation"]["required"] = True
        data["ui_validation"]["test_readiness"]["status"] = "blocked"
        data["e2e"]["items"] = []
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("requires e2e.items" in error for error in errors), errors)

    def test_legacy_user_testing_rejects_partial_implementation_row(self) -> None:
        data = valid_contract()
        data["status"] = "user_testing"
        data["lot_completion_gate"]["status"] = "fail"
        data["lot_completion_gate"]["decision"] = "user_testing"
        data["validated_requests"][0]["status"] = "doing"
        data["lot_completion_gate"]["coverage_table"][0]["status"] = "partiel"
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("user_testing" in error and "partial" in error for error in errors), errors)

    def test_legacy_request_done_rejects_requires_e2e_coverage(self) -> None:
        data = valid_contract()
        data["status"] = "user_testing"
        data["lot_completion_gate"]["status"] = "pending"
        data["lot_completion_gate"]["decision"] = "user_testing"
        data["lot_completion_gate"]["coverage_table"][0]["status"] = "requires_e2e"
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("status done contradicts" in error for error in errors), errors)

    def test_legacy_multi_lot_single_request_emits_normalization_warning(self) -> None:
        data = valid_contract()
        data["validated_requests"][0]["coverage"] = "Couvrir tous les lots valides."
        errors, warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)
        self.assertTrue(any("multi-lot" in warning and "generic" in warning for warning in warnings), warnings)

    def test_missing_ui_validation_is_legacy_warning(self) -> None:
        data = valid_contract()
        del data["ui_validation"]
        errors, warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)
        self.assertTrue(any("ui_validation missing" in warning for warning in warnings), warnings)


if __name__ == "__main__":
    unittest.main()
