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
                "status": "done",
                "coverage": "schema, template et validateur crees",
                "files": ["scripts/codex/validate_sr_contract.py"],
                "verification": ["python3 scripts/codex/validate_sr_contract.py --file sr_contract.json"],
                "notes": [],
            }
        ],
        "scope": {"in": ["schema"], "out": [], "allowed_paths": [], "forbidden_paths": []},
        "product_truth": {"required": True, "items": ["les fichiers legacy restent historiques"]},
        "evidence": {"sources_read": ["docs/codex/SR_METHOD.md"], "code_files_read": [], "tests_or_logs": []},
        "skills": {"method": ["aurora-lot-runner"], "domain": []},
        "plan": ["Creer le schema."],
        "findings": [],
        "decisions": [],
        "implementation": {"app_code_changed": False, "changed_files": ["scripts/codex/validate_sr_contract.py"]},
        "verification": {"commands_run": ["unit"], "commands_failed": [], "not_run_reason": None},
        "gates": {"evidence": "pass", "verification": "pass", "context_budget": "pass"},
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


if __name__ == "__main__":
    unittest.main()
