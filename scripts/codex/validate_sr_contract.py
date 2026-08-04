#!/usr/bin/env python3
"""Validate a SR 3.0.0 living task contract."""
import argparse
import json
import re
import sys
from pathlib import Path


SCHEMA_VERSION = "3.0.0"
VALID_TASK_TYPES = {"feature", "bugfix", "upgrade", "realign", "documentation", "analysis", "maintenance", "method"}
VALID_STATUSES = {"planned", "doing", "user_testing", "repair", "done", "blocked", "cancelled"}
VALID_REQUEST_STATUSES = {"todo", "doing", "done", "requires_e2e", "blocked", "moved_to_new_lot", "cancelled"}
VALID_GATE_STATUSES = {"pending", "pass", "fail", "not_applicable"}
VALID_COMPLETION_STATUSES = {"fait", "partiel", "non fait", "bloque", "hors perimetre valide", "requires_e2e"}
BLOCKING_COMPLETION_STATUSES = {"partiel", "non fait", "bloque", "requires_e2e"}
VALID_CONTEXT_STATUSES = {"green", "yellow", "orange", "red", "unknown", "stale", "ambiguous", "not_checked"}
VALID_TRANSITIONS = {"continue_current", "recommend_new_conversation", "stop_for_new_conversation", "not_applicable"}
VALID_PROPAGATION_RISK_LEVELS = {"low", "medium", "high", "critical", "not_applicable"}
VALID_PROPAGATION_COMPATIBILITY = {
    "full_propagation",
    "compatibility_shim",
    "two_step_migration",
    "not_required",
}
VALID_PROPAGATION_DECISIONS = {"pass", "repair", "blocked", "not_applicable"}


def load_contract(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid json: {exc}")
    if not isinstance(data, dict):
        raise ValueError("contract root must be an object")
    return data


def require_object(data: dict, key: str, errors: list[str]) -> dict:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be an object")
        return {}
    return value


def require_list(data: dict, key: str, errors: list[str]) -> list:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"{key} must be a list")
        return []
    return value


def non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_backlog_mutation(data: dict, errors: list[str]) -> dict:
    mutation = data.get("backlog_mutation")
    if mutation is None:
        return {}
    if not isinstance(mutation, dict):
        errors.append("backlog_mutation must be an object")
        return {}
    status = mutation.get("status")
    if status not in VALID_GATE_STATUSES:
        errors.append(f"backlog_mutation.status must be one of {sorted(VALID_GATE_STATUSES)}")
    for key in ("structural_change_detected", "mutation_required", "sr_inbox_updated", "sr_lots_updated"):
        if not isinstance(mutation.get(key), bool):
            errors.append(f"backlog_mutation.{key} must be boolean")
    for key in ("affected_lots", "created_lots", "reopened_lots", "blocked_lots", "superseded_lots"):
        if not isinstance(mutation.get(key), list):
            errors.append(f"backlog_mutation.{key} must be a list")
    if not non_empty_string(mutation.get("decision")):
        errors.append("backlog_mutation.decision must be a non-empty string")
    if mutation.get("mutation_required") is True:
        updated = mutation.get("sr_inbox_updated") is True or mutation.get("sr_lots_updated") is True
        if not updated and not non_empty_string(mutation.get("not_updated_reason")):
            errors.append("backlog_mutation.not_updated_reason is required when mutation_required is true and no backlog file was updated")
    return mutation


def validate_global_impact(data: dict, errors: list[str]) -> dict:
    impact = data.get("global_impact")
    if impact is None:
        return {}
    if not isinstance(impact, dict):
        errors.append("global_impact must be an object")
        return {}
    required = impact.get("required")
    if not isinstance(required, bool):
        errors.append("global_impact.required must be boolean")
    status = impact.get("status")
    if status not in VALID_GATE_STATUSES:
        errors.append(f"global_impact.status must be one of {sorted(VALID_GATE_STATUSES)}")
    for key in (
        "surfaces_reviewed",
        "impacted_lots",
        "new_lots_to_create",
        "lots_to_reopen_or_block",
        "assumptions",
        "open_questions",
    ):
        if not isinstance(impact.get(key), list):
            errors.append(f"global_impact.{key} must be a list")
    if not non_empty_string(impact.get("sequencing_recommendation")):
        errors.append("global_impact.sequencing_recommendation must be a non-empty string")
    if required is True:
        if status == "not_applicable":
            errors.append("global_impact.status cannot be not_applicable when required is true")
        if not impact.get("surfaces_reviewed"):
            errors.append("global_impact.surfaces_reviewed must not be empty when required is true")
    return impact


def validate_requests(data: dict, errors: list[str]) -> list:
    requests = require_list(data, "validated_requests", errors)
    seen = set()
    for index, request in enumerate(requests):
        prefix = f"validated_requests[{index}]"
        if not isinstance(request, dict):
            errors.append(f"{prefix} must be an object")
            continue
        request_id = request.get("id")
        if not non_empty_string(request_id):
            errors.append(f"{prefix}.id must be a non-empty string")
        elif request_id in seen:
            errors.append(f"{prefix}.id is duplicated: {request_id}")
        else:
            seen.add(request_id)
        if request.get("status") not in VALID_REQUEST_STATUSES:
            errors.append(f"{prefix}.status must be one of {sorted(VALID_REQUEST_STATUSES)}")
        if "requirement_type" in request and not non_empty_string(request.get("requirement_type")):
            errors.append(f"{prefix}.requirement_type must be a non-empty string when present")
        for key in ("source", "coverage"):
            if not non_empty_string(request.get(key)):
                errors.append(f"{prefix}.{key} must be a non-empty string")
        for key in ("files", "verification"):
            value = request.get(key)
            if not isinstance(value, list):
                errors.append(f"{prefix}.{key} must be a list")
        if "notes" in request and not isinstance(request["notes"], list):
            errors.append(f"{prefix}.notes must be a list when present")
    return requests


def request_requires_ui_evidence(request: dict) -> bool:
    request_type = str(request.get("requirement_type", "")).lower()
    text = " ".join(str(request.get(key, "")) for key in ("id", "source", "coverage")).lower()
    return request_type in {"ui", "ui_ux", "design", "ux"} or bool(
        re.search(r"\b(ui|ux|design|ecran|écran|page|interface|visuel)\b", text)
    )


def validate_lot_completion_gate(data: dict, requests: list, errors: list[str]) -> dict:
    gate = data.get("lot_completion_gate")
    if gate is None:
        return {}
    if not isinstance(gate, dict):
        errors.append("lot_completion_gate must be an object")
        return {}
    status = gate.get("status")
    if status not in VALID_GATE_STATUSES:
        errors.append(f"lot_completion_gate.status must be one of {sorted(VALID_GATE_STATUSES)}")
    if "validated_scope_source" in gate and not non_empty_string(gate.get("validated_scope_source")):
        errors.append("lot_completion_gate.validated_scope_source must be a non-empty string when present")
    for key in ("scope_reduction_requested", "scope_reduction_validated_by_user", "ui_ux_required"):
        if key in gate and not isinstance(gate.get(key), bool):
            errors.append(f"lot_completion_gate.{key} must be boolean")
    if gate.get("scope_reduction_requested") is True and gate.get("scope_reduction_validated_by_user") is not True:
        errors.append("lot_completion_gate scope reduction requires explicit user validation")

    coverage_table = gate.get("coverage_table")
    if not isinstance(coverage_table, list):
        errors.append("lot_completion_gate.coverage_table must be a list")
        coverage_table = []

    request_ids = {
        request.get("id")
        for request in requests
        if isinstance(request, dict) and non_empty_string(request.get("id"))
    }
    covered_ids = set()
    for index, row in enumerate(coverage_table):
        prefix = f"lot_completion_gate.coverage_table[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{prefix} must be an object")
            continue
        requirement_id = row.get("requirement_id")
        if not non_empty_string(requirement_id):
            errors.append(f"{prefix}.requirement_id must be a non-empty string")
        else:
            covered_ids.add(requirement_id)
        if not non_empty_string(row.get("requirement")):
            errors.append(f"{prefix}.requirement must be a non-empty string")
        if row.get("status") not in VALID_COMPLETION_STATUSES:
            errors.append(f"{prefix}.status must be one of {sorted(VALID_COMPLETION_STATUSES)}")
        if not isinstance(row.get("proof"), list):
            errors.append(f"{prefix}.proof must be a list")
        if "comment" in row and not isinstance(row.get("comment"), str):
            errors.append(f"{prefix}.comment must be a string when present")

    missing_ids = sorted(request_ids - covered_ids)
    if data.get("status") in {"done", "user_testing", "repair"} and missing_ids:
        errors.append(f"lot_completion_gate.coverage_table must cover all validated_requests: missing {missing_ids}")

    visual_evidence = gate.get("visual_evidence")
    if not isinstance(visual_evidence, list):
        errors.append("lot_completion_gate.visual_evidence must be a list")
        visual_evidence = []
    decision = gate.get("decision")
    if decision not in VALID_STATUSES:
        errors.append(f"lot_completion_gate.decision must be one of {sorted(VALID_STATUSES)}")

    if data.get("status") == "done":
        if status != "pass":
            errors.append("status done requires lot_completion_gate.status pass")
        blocking_rows = [
            row.get("requirement_id", f"#{index}")
            for index, row in enumerate(coverage_table)
            if isinstance(row, dict) and row.get("status") in BLOCKING_COMPLETION_STATUSES
        ]
        if blocking_rows:
            errors.append(f"status done is incompatible with incomplete lot_completion_gate rows: {blocking_rows}")
        for request in requests:
            if not isinstance(request, dict) or request.get("status") != "done":
                continue
            has_proof = bool(request.get("files")) or bool(request.get("verification")) or bool(request.get("notes"))
            if not has_proof:
                errors.append(f"validated_requests {request.get('id')} marked done requires files, verification or notes proof")
        ui_required = gate.get("ui_ux_required") is True or any(
            isinstance(request, dict) and request_requires_ui_evidence(request) for request in requests
        )
        e2e = data.get("e2e") if isinstance(data.get("e2e"), dict) else {}
        if ui_required and not visual_evidence and not e2e.get("items"):
            errors.append("status done with UI/UX requirements requires lot_completion_gate.visual_evidence or e2e.items")
    return gate


def validate_propagation(data: dict, errors: list[str], warnings: list[str]) -> dict:
    propagation = data.get("propagation")
    gates = data.get("gates") if isinstance(data.get("gates"), dict) else {}
    if propagation is None:
        if "propagation" in gates and gates.get("propagation") != "not_applicable":
            errors.append("gates.propagation requires propagation object")
        else:
            warnings.append("propagation missing; accepted as legacy contract")
        return {}
    if not isinstance(propagation, dict):
        errors.append("propagation must be an object")
        return {}

    required = propagation.get("required")
    if not isinstance(required, bool):
        errors.append("propagation.required must be boolean")
        required = False
    status = propagation.get("status")
    if status not in VALID_GATE_STATUSES:
        errors.append(f"propagation.status must be one of {sorted(VALID_GATE_STATUSES)}")
    risk_level = propagation.get("risk_level")
    if risk_level not in VALID_PROPAGATION_RISK_LEVELS:
        errors.append(f"propagation.risk_level must be one of {sorted(VALID_PROPAGATION_RISK_LEVELS)}")
    compatibility = propagation.get("compatibility_strategy")
    if compatibility not in VALID_PROPAGATION_COMPATIBILITY:
        errors.append(f"propagation.compatibility_strategy must be one of {sorted(VALID_PROPAGATION_COMPATIBILITY)}")
    decision = propagation.get("decision")
    if decision not in VALID_PROPAGATION_DECISIONS:
        errors.append(f"propagation.decision must be one of {sorted(VALID_PROPAGATION_DECISIONS)}")

    preflight = propagation.get("preflight")
    if not isinstance(preflight, dict):
        errors.append("propagation.preflight must be an object")
        preflight = {}
    else:
        if not isinstance(preflight.get("done"), bool):
            errors.append("propagation.preflight.done must be boolean")
        if not non_empty_string(preflight.get("summary")):
            errors.append("propagation.preflight.summary must be a non-empty string")
        for key in ("human_validation_required", "human_validation_received"):
            if not isinstance(preflight.get(key), bool):
                errors.append(f"propagation.preflight.{key} must be boolean")

    for key in (
        "changed_symbols",
        "affected_surfaces",
        "consumers_checked",
        "reference_searches",
        "remaining_references",
        "ignored_references",
        "verification",
    ):
        if not isinstance(propagation.get(key), list):
            errors.append(f"propagation.{key} must be a list")

    if required is True and status == "not_applicable":
        errors.append("propagation.status cannot be not_applicable when required is true")
    if required is not True:
        return propagation

    is_done_or_pass = data.get("status") == "done" or status == "pass" or decision == "pass"
    if not is_done_or_pass:
        return propagation

    if status != "pass":
        errors.append("status done requires propagation.status pass when propagation is required")
    if decision != "pass":
        errors.append("status done requires propagation.decision pass when propagation is required")
    if preflight.get("done") is not True:
        errors.append("propagation.preflight.done must be true when propagation is required")
    if preflight.get("human_validation_required") is True and preflight.get("human_validation_received") is not True:
        errors.append("propagation human validation required but not received")
    if not propagation.get("changed_symbols"):
        errors.append("propagation.changed_symbols must not be empty when propagation is required")
    if not propagation.get("reference_searches"):
        errors.append("propagation.reference_searches must not be empty when propagation is required")
    if propagation.get("remaining_references") and not propagation.get("ignored_references"):
        errors.append("propagation.remaining_references require ignored_references justification")
    if risk_level in {"high", "critical"}:
        if not propagation.get("affected_surfaces"):
            errors.append("high/critical propagation requires propagation.affected_surfaces")
        if not propagation.get("consumers_checked"):
            errors.append("high/critical propagation requires propagation.consumers_checked")
        if not propagation.get("verification"):
            errors.append("high/critical propagation requires propagation.verification")
    return propagation


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    required = (
        "schema_version",
        "task_id",
        "lot_id",
        "task_type",
        "status",
        "objective",
        "validated_requests",
        "lot_completion_gate",
        "scope",
        "product_truth",
        "evidence",
        "skills",
        "plan",
        "findings",
        "decisions",
        "implementation",
        "verification",
        "gates",
        "e2e",
        "context",
        "transition",
    )
    for key in required:
        if key not in data:
            errors.append(f"missing required key: {key}")

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    if data.get("task_type") not in VALID_TASK_TYPES:
        errors.append(f"task_type must be one of {sorted(VALID_TASK_TYPES)}")
    status = data.get("status")
    if status not in VALID_STATUSES:
        errors.append(f"status must be one of {sorted(VALID_STATUSES)}")
    for key in ("task_id", "lot_id", "objective"):
        if not non_empty_string(data.get(key)):
            errors.append(f"{key} must be a non-empty string")

    requests = validate_requests(data, errors)
    validate_lot_completion_gate(data, requests, errors)
    propagation = validate_propagation(data, errors, warnings)
    if data.get("task_type") != "analysis" and not requests:
        errors.append("validated_requests must not be empty for non-analysis tasks")
    if status == "done":
        open_statuses = {"todo", "doing", "requires_e2e", "blocked"}
        for request in requests:
            if isinstance(request, dict) and request.get("status") in open_statuses:
                errors.append("status done requires all validated_requests to be done, moved_to_new_lot or cancelled")

    scope = require_object(data, "scope", errors)
    if scope:
        for key in ("in", "out", "allowed_paths", "forbidden_paths"):
            if key in scope and not isinstance(scope[key], list):
                errors.append(f"scope.{key} must be a list")

    product_truth = require_object(data, "product_truth", errors)
    if product_truth:
        required_truth = product_truth.get("required")
        items = product_truth.get("items")
        if not isinstance(required_truth, bool):
            errors.append("product_truth.required must be boolean")
        if not isinstance(items, list):
            errors.append("product_truth.items must be a list")
        if required_truth is True and not items:
            errors.append("product_truth.items must not be empty when product_truth.required is true")

    backlog_mutation = validate_backlog_mutation(data, errors)
    global_impact = validate_global_impact(data, errors)
    if backlog_mutation and global_impact:
        if backlog_mutation.get("structural_change_detected") is True and global_impact.get("required") is not True:
            errors.append("structural backlog changes require global_impact.required true")
    for request in requests:
        if isinstance(request, dict) and request.get("status") == "moved_to_new_lot":
            notes = request.get("notes") if isinstance(request.get("notes"), list) else []
            notes_text = " ".join(str(item) for item in notes)
            coverage = request.get("coverage") if isinstance(request.get("coverage"), str) else ""
            created_lots = backlog_mutation.get("created_lots") if isinstance(backlog_mutation, dict) else []
            has_target = (
                bool(created_lots)
                or "SR_INBOX" in notes_text
                or "SR_LOTS" in notes_text
                or "SR-" in coverage
                or "lot cible" in coverage.lower()
            )
            if not has_target:
                errors.append("moved_to_new_lot requests require a target lot, SR_INBOX/SR_LOTS note, or backlog_mutation.created_lots")

    evidence = require_object(data, "evidence", errors)
    if evidence:
        for key in ("sources_read", "code_files_read", "tests_or_logs"):
            if key in evidence and not isinstance(evidence[key], list):
                errors.append(f"evidence.{key} must be a list")
        if status == "done" and not evidence.get("sources_read"):
            errors.append("evidence.sources_read must not be empty when status is done")

    skills = require_object(data, "skills", errors)
    if skills:
        for key in ("method", "domain"):
            if key in skills and not isinstance(skills[key], list):
                errors.append(f"skills.{key} must be a list")

    for key in ("plan", "findings", "decisions"):
        value = data.get(key)
        if not isinstance(value, list):
            errors.append(f"{key} must be a list")

    implementation = require_object(data, "implementation", errors)
    if implementation:
        app_code_changed = implementation.get("app_code_changed")
        changed_files = implementation.get("changed_files")
        if not isinstance(app_code_changed, bool):
            errors.append("implementation.app_code_changed must be boolean")
        if not isinstance(changed_files, list):
            errors.append("implementation.changed_files must be a list")
        if app_code_changed is True and not changed_files:
            errors.append("implementation.changed_files must not be empty when app_code_changed is true")

    verification = require_object(data, "verification", errors)
    if verification:
        commands_run = verification.get("commands_run")
        commands_failed = verification.get("commands_failed")
        not_run_reason = verification.get("not_run_reason")
        if not isinstance(commands_run, list):
            errors.append("verification.commands_run must be a list")
            commands_run = []
        if not isinstance(commands_failed, list):
            errors.append("verification.commands_failed must be a list")
            commands_failed = []
        if status == "done" and not commands_run and not non_empty_string(not_run_reason):
            errors.append("status done requires verification.commands_run or verification.not_run_reason")
        if status == "done" and commands_failed and not non_empty_string(not_run_reason):
            errors.append("status done requires failed commands to be justified")

    gates = require_object(data, "gates", errors)
    if gates:
        for key, value in gates.items():
            if value not in VALID_GATE_STATUSES:
                errors.append(f"gates.{key} must be one of {sorted(VALID_GATE_STATUSES)}")
        if status == "done":
            for key, value in gates.items():
                if value == "fail":
                    errors.append(f"status done is incompatible with gates.{key}=fail")
            if gates.get("lot_completion") != "pass":
                errors.append("status done requires gates.lot_completion pass")
            if isinstance(propagation, dict) and propagation.get("required") is True and gates.get("propagation") != "pass":
                errors.append("status done requires gates.propagation pass when propagation is required")

    e2e = require_object(data, "e2e", errors)
    if e2e:
        required_e2e = e2e.get("required")
        items = e2e.get("items")
        if not isinstance(required_e2e, bool):
            errors.append("e2e.required must be boolean")
        if not isinstance(items, list):
            errors.append("e2e.items must be a list")
        if required_e2e is True and not items:
            errors.append("e2e.items must not be empty when e2e.required is true")

    context = require_object(data, "context", errors)
    context_status = None
    if context:
        context_status = context.get("status")
        if context_status not in VALID_CONTEXT_STATUSES:
            errors.append(f"context.status must be one of {sorted(VALID_CONTEXT_STATUSES)}")
        if "report_path" in context and context["report_path"] is not None and not non_empty_string(context["report_path"]):
            errors.append("context.report_path must be null or a non-empty string")

    transition = require_object(data, "transition", errors)
    if transition:
        decision = transition.get("decision")
        if decision not in VALID_TRANSITIONS:
            errors.append(f"transition.decision must be one of {sorted(VALID_TRANSITIONS)}")
        if not non_empty_string(transition.get("reason")):
            errors.append("transition.reason must be a non-empty string")
        next_required = transition.get("next_session_prompt_required")
        if not isinstance(next_required, bool):
            errors.append("transition.next_session_prompt_required must be boolean")
        next_path = transition.get("next_session_prompt_path")
        next_user_prompt = transition.get("next_user_prompt")
        if next_required is True:
            if not non_empty_string(next_path):
                errors.append("transition.next_session_prompt_path is required when next_session_prompt_required is true")
            if not non_empty_string(next_user_prompt):
                errors.append("transition.next_user_prompt is required when next_session_prompt_required is true")
        if context_status in {"red", "stale", "ambiguous"} and decision != "stop_for_new_conversation":
            errors.append("red/stale/ambiguous context requires transition.decision stop_for_new_conversation")
        if context_status == "orange" and decision not in {"recommend_new_conversation", "stop_for_new_conversation"}:
            errors.append("orange context requires transition.decision recommend_new_conversation or stop_for_new_conversation")
        if decision in {"recommend_new_conversation", "stop_for_new_conversation"} and next_required is not True:
            errors.append("new conversation transition requires next_session_prompt_required true")
        if context_status == "yellow" and decision == "continue_current":
            warnings.append("yellow context should usually recommend a new conversation before a long next lot")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a SR 3.0.0 sr_contract.json file.")
    parser.add_argument("--file", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.file)
    try:
        data = load_contract(path)
        errors, warnings = validate(data)
    except ValueError as exc:
        errors, warnings = [str(exc)], []

    result = {"ok": not errors, "errors": errors, "warnings": warnings, "file": str(path)}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if errors:
            print("SR contract errors:")
            for error in errors:
                print(f"- {error}")
        if warnings:
            print("SR contract warnings:")
            for warning in warnings:
                print(f"- {warning}")
        if not errors:
            print(f"OK: SR contract valid ({path})")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
