#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path

import sr_completion_rules
import validate_pass_contract
import validate_sr_contract


FIXTURES = Path(__file__).parent / "fixtures/requirement_traceability"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def evidence(kind: str, status: str = "pass", reference: str = "test") -> dict:
    return {"kind": kind, "status": status, "reference": reference}


def request(
    request_id: str,
    lot_id: str,
    implementation_status: str,
    expected: list[str] | None = None,
    obtained: list[dict] | None = None,
    requirement: str | None = None,
) -> dict:
    expected = expected or []
    obtained = obtained or []
    item = {
        "id": request_id,
        "source": {"kind": "user_validation", "reference": "message utilisateur"},
        "requirement_type": "product",
        "requirement": requirement or f"Couvrir {request_id}",
        "origin": {"pass_id": "PASS-1", "lot_id": lot_id},
        "implementation_status": implementation_status,
        "evidence_status": "missing",
        "affected_files": [],
        "affected_components": [],
        "expected_evidence": [
            {"kind": kind, "required": True, "description": f"Preuve {kind}"} for kind in expected
        ],
        "obtained_evidence": obtained,
        "remaining_work": [],
        "remaining_tests": [],
        "history": [],
        "blocked_reason": None,
        "disposition": None,
        "decision": "repair",
    }
    item["evidence_status"] = sr_completion_rules.derive_evidence_status(item)
    item["decision"] = sr_completion_rules.derive_request_decision(item)
    if item["decision"] == "user_testing":
        item["remaining_tests"] = ["Executer la preuve restante."]
    if implementation_status in {"not_started", "partial", "defective"}:
        item["remaining_work"] = ["Terminer ou reparer l'implementation."]
    return item


def contract(requests: list[dict], lots: list[str] | None = None, status: str | None = None) -> dict:
    lots = lots or sorted({item["origin"]["lot_id"] for item in requests})
    decision = sr_completion_rules.derive_contract_decision(requests)
    status = status or decision
    rows = [sr_completion_rules.coverage_row(item) for item in requests]
    open_ids = sr_completion_rules.open_requirement_ids(requests)
    return {
        "schema_version": "3.1.0",
        "task_id": "2026-08-24_traceability",
        "lot_id": lots[0],
        "task_type": "method",
        "status": status,
        "objective": "Conserver toutes les demandes validees.",
        "origin": {"pass_id": "PASS-1", "lot_ids": lots, "validation_source": "je valide"},
        "intake": {
            "classification": "new_requirement",
            "matched_requirement_ids": [],
            "creates_new_lot": False,
            "feedback": None,
        },
        "lineage": {
            "parent_contract": None,
            "inherited_open_requirement_ids": [],
            "reopened_lot_ids": [],
            "next_coherent_scope": "Traiter toutes les demandes ouvertes.",
        },
        "new_lot_justification": None,
        "validated_requests": requests,
        "lot_completion_gate": {
            "status": sr_completion_rules.derive_gate_status(decision),
            "derived_from_validated_requests": True,
            "validated_scope_source": "je valide",
            "scope_reduction_requested": False,
            "scope_reduction_validated_by_user": False,
            "coverage_table": rows,
            "ui_ux_required": False,
            "visual_evidence": [],
            "decision": decision,
        },
        "closure": {
            "overall_claim": sr_completion_rules.derive_closure_claim(decision),
            "summary": "Des demandes restent ouvertes." if decision != "done" else "Toutes les demandes sont terminees et prouvees.",
            "open_requirement_ids": open_ids,
        },
        "scope": {"in": [], "out": [], "allowed_paths": [], "forbidden_paths": []},
        "product_truth": {"required": False, "items": []},
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
            "not_updated_reason": "Aucune mutation.",
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
                "summary": "Aucune propagation.",
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
        "evidence": {"sources_read": ["message utilisateur"], "code_files_read": [], "tests_or_logs": []},
        "ui_validation": {
            "required": False,
            "routes": [],
            "test_readiness": {"status": "not_applicable", "auth_mode": "none"},
            "visual_evidence": {
                "status": "not_applicable",
                "routes": [],
                "viewports": [],
                "screenshots": [],
                "report_file": None,
            },
        },
        "skills": {"method": ["aurora-lot-runner"], "domain": []},
        "plan": [],
        "findings": [],
        "decisions": [],
        "implementation": {"app_code_changed": False, "changed_files": []},
        "verification": {"commands_run": ["unit"], "commands_failed": [], "not_run_reason": None},
        "gates": {"lot_completion": sr_completion_rules.derive_gate_status(decision)},
        "e2e": {"required": decision == "user_testing", "items": ["Executer les tests restants."] if decision == "user_testing" else []},
        "context": {"status": "green", "report_path": None},
        "transition": {
            "decision": "continue_current",
            "reason": "Contexte vert.",
            "next_session_prompt_required": False,
            "next_session_prompt_path": None,
            "next_user_prompt": None,
        },
    }


class RequirementTraceabilityTest(unittest.TestCase):
    def assert_error(self, data: dict, fragment: str, path: Path | None = None) -> list[str]:
        errors, _warnings = validate_sr_contract.validate(data, contract_path=path)
        self.assertTrue(any(fragment in error for error in errors), errors)
        return errors

    def test_scenario_a_partial_ui_forces_repair_and_forbids_complete_closure(self) -> None:
        fixture = load_fixture("scenario_a_five_lots_one_partial.json")
        requests = []
        for item in fixture["requests"]:
            expected = ["unit", "build"] if item["evidence_status"] == "sufficient" else ["visual"]
            obtained = [evidence(kind) for kind in expected] if item["evidence_status"] == "sufficient" else []
            requests.append(request(item["id"], item["lot_id"], item["implementation_status"], expected, obtained))
        data = contract(requests, fixture["lots"], status=fixture["declared_status"])
        data["lot_completion_gate"]["decision"] = "user_testing"
        data["lot_completion_gate"]["status"] = "fail"
        data["closure"]["overall_claim"] = "technically_complete_awaiting_evidence"
        data["closure"]["summary"] = fixture["forbidden_closure"]
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertTrue(any("status user_testing" in error for error in errors), errors)
        self.assertTrue(any("closure.summary" in error for error in errors), errors)
        self.assertEqual("repair", sr_completion_rules.derive_contract_decision(requests))
        self.assertIn("REQ-SOURCES-ACCORDION", sr_completion_rules.open_requirement_ids(requests))

    def test_scenario_b_complete_code_with_missing_e2e_allows_user_testing(self) -> None:
        fixture = load_fixture("scenario_b_complete_e2e_pending.json")
        item = request(fixture["request_id"], "LOT-SOURCES", "complete", fixture["expected_evidence"], [])
        self.assertEqual(fixture["expected_evidence_status"], item["evidence_status"])
        self.assertEqual(fixture["expected_decision"], item["decision"])
        data = contract([item])
        errors, warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_complete_code_with_missing_technical_verification_stays_repair(self) -> None:
        item = request("REQ-BUILD", "LOT-BUILD", "complete", ["build"], [])
        item["remaining_tests"] = []
        item["remaining_work"] = ["Executer et corriger le build technique."]
        item["decision"] = sr_completion_rules.derive_request_decision(item)
        self.assertEqual("repair", item["decision"])
        data = contract([item])
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)

    def test_scenario_c_feedback_reopens_original_lot_without_new_lot(self) -> None:
        fixture = load_fixture("scenario_c_existing_requirement_feedback.json")
        requests = [
            request("REQ-SOURCES-ACCORDION", "LOT-SOURCES", "partial", ["visual"], []),
            request("REQ-SOURCES-SEPARATION", "LOT-SOURCES", "complete", ["e2e"], [evidence("e2e")]),
            request("REQ-SOURCES-DOCUMENT-OPEN", "LOT-SOURCES", "complete", ["e2e"], []),
        ]
        data = contract(requests)
        data["intake"].update(
            {
                "classification": fixture["classification"],
                "matched_requirement_ids": [fixture["matched_requirement_id"]],
                "feedback": "L'accordeon prevu n'existe pas.",
            }
        )
        data["lineage"]["reopened_lot_ids"] = [fixture["origin_lot_id"]]
        data["validated_requests"][0]["history"].append(
            {"type": "user_feedback", "summary": "L'accordeon prevu n'existe pas."}
        )
        data["backlog_mutation"].update(
            {
                "status": "pass",
                "mutation_required": True,
                "sr_lots_updated": True,
                "affected_lots": [fixture["origin_lot_id"]],
                "reopened_lots": [fixture["origin_lot_id"]],
                "not_updated_reason": None,
                "decision": "reopen_or_amend_existing_lot",
            }
        )
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)
        self.assertEqual(fixture["expected_status"], data["status"])
        self.assertEqual(set(fixture["source_checklist"]), {item["id"] for item in data["validated_requests"]})
        self.assertEqual([], data["backlog_mutation"]["created_lots"])

    def test_existing_requirement_repair_can_close_after_fix_and_evidence(self) -> None:
        fixed = request(
            "REQ-SOURCES-ACCORDION",
            "LOT-SOURCES",
            "complete",
            ["visual"],
            [evidence("visual")],
        )
        fixed["history"].append(
            {"type": "user_feedback", "summary": "L'accordeon prevu n'existait pas."}
        )
        data = contract([fixed])
        data["intake"].update(
            {
                "classification": "existing_requirement_repair",
                "matched_requirement_ids": [fixed["id"]],
                "feedback": "L'accordeon prevu n'existait pas.",
            }
        )
        data["lineage"]["reopened_lot_ids"] = ["LOT-SOURCES"]
        errors, warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)
        self.assertEqual("done", data["status"])

    def test_scenario_d_new_requirement_requires_justification_and_preserves_existing_open_request(self) -> None:
        fixture = load_fixture("scenario_d_new_document_library.json")
        requests = [
            request(fixture["existing_open_requirement_id"], "LOT-SOURCES", "complete", ["e2e"], []),
            request(fixture["new_requirement_id"], fixture["new_lot_id"], "not_started", [], []),
        ]
        data = contract(requests, ["LOT-SOURCES", fixture["new_lot_id"]])
        data["intake"]["creates_new_lot"] = True
        data["new_lot_justification"] = {
            "outside_existing_validated_scope": True,
            "checked_lots": fixture["checked_lots"],
            "reason": fixture["reason"],
            "user_decision_required": True,
        }
        errors, _warnings = validate_sr_contract.validate(data)
        self.assertEqual([], errors)
        self.assertIn(fixture["existing_open_requirement_id"], sr_completion_rules.open_requirement_ids(requests))
        data["new_lot_justification"] = None
        self.assert_error(data, "new_lot_justification")

    def test_scenario_e_rejects_declared_gate_contradiction(self) -> None:
        fixture = load_fixture("scenario_e_contract_contradiction.json")
        item = request("REQ-E", "LOT-E", "complete", ["e2e"], [])
        data = contract([item])
        data["lot_completion_gate"]["status"] = fixture["completion_gate_status"]
        errors, _warnings = validate_sr_contract.validate(data)
        for fragment in fixture["expected_error_fragments"]:
            self.assertTrue(any(fragment in error for error in errors), errors)

    def test_scenario_f_parent_open_requirements_must_all_be_inherited(self) -> None:
        fixture = load_fixture("scenario_f_handoff_inheritance.json")
        parent_requests = [request(item, "LOT-F", "complete", ["e2e"], []) for item in fixture["parent_open_requirement_ids"]]
        parent = contract(parent_requests)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent_path = root / "parent.json"
            child_path = root / "child.json"
            parent_path.write_text(json.dumps(parent), encoding="utf-8")

            child_requests = [request(item, "LOT-F", "complete", ["e2e"], []) for item in fixture["incomplete_child_requirement_ids"]]
            child = contract(child_requests)
            child["lineage"].update(
                {
                    "parent_contract": "parent.json",
                    "inherited_open_requirement_ids": fixture["incomplete_child_requirement_ids"],
                    "reopened_lot_ids": ["LOT-F"],
                    "next_coherent_scope": fixture["expected_next_scope"],
                }
            )
            self.assert_error(child, "missing inherited open requirements", child_path)

            child_requests = [request(item, "LOT-F", "complete", ["e2e"], []) for item in fixture["complete_child_requirement_ids"]]
            child = contract(child_requests)
            child["lineage"].update(
                {
                    "parent_contract": "parent.json",
                    "inherited_open_requirement_ids": fixture["complete_child_requirement_ids"],
                    "reopened_lot_ids": ["LOT-F"],
                    "next_coherent_scope": fixture["expected_next_scope"],
                }
            )
            errors, _warnings = validate_sr_contract.validate(child, contract_path=child_path)
            self.assertEqual([], errors)
            resume = sr_completion_rules.render_resume_requirements(child_requests)
            for request_id in fixture["parent_open_requirement_ids"]:
                self.assertIn(request_id, resume)
        next_session_template = (Path(__file__).parents[2] / "tasks/_TEMPLATE/NEXT_SESSION_PROMPT.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "exigences partielles ou defectueuses",
            "preuves et tests manquants",
            "retours utilisateur rattaches",
            "prochain ensemble coherent",
        ):
            self.assertIn(marker, next_session_template)

    def test_pass_statuses_repair_and_reopened_are_supported_and_derived(self) -> None:
        lots = {
            "LOT-1": {"lot_id": "LOT-1", "status": "done", "depends_on": []},
            "LOT-2": {"lot_id": "LOT-2", "status": "repair", "depends_on": []},
        }
        item = {
            "pass_id": "PASS-1",
            "title": "Passe consolidee",
            "status": "repair",
            "lots": ["LOT-1", "LOT-2"],
            "preflight": {},
            "e2e_strategy": {"mode": "not_required", "items": []},
            "stop_on": ["gate_failure"],
        }
        self.assertEqual([], validate_pass_contract.validate_pass(item, 0, lots))
        item["status"] = "user_testing"
        errors = validate_pass_contract.validate_pass(item, 0, lots)
        self.assertTrue(any("user_testing" in error and "repair" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
