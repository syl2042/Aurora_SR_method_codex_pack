#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


VALID_TASK_TYPES = {"feature", "bugfix", "upgrade", "realign", "documentation", "analysis", "maintenance"}
VALID_STATUS_DECISIONS = {"done", "user_testing", "repair", "blocked", "not_applicable"}
VALID_CONTEXT_STATUS = {"green", "yellow", "orange", "red", "unknown", "stale", "ambiguous", "not_checked"}
VALID_NEXT_PROMPT = {"created", "updated", "not_required", "missing"}
VALID_TRANSITION_DECISIONS = {
    "continue_current",
    "recommend_new_conversation",
    "stop_for_new_conversation",
    "not_applicable",
}
VALID_RESUME_MODES = {
    "not_required",
    "strict_resume",
    "resume_and_continue",
}
VALID_PLAIN_RESUME_DEFAULTS = {
    "strict_resume",
    "resume_and_continue",
    "not_applicable",
}


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


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for key in (
        "schema_version",
        "task_id",
        "task_type",
        "status_decision",
        "evidence_gate",
        "implementation",
        "verification",
        "e2e_user_tests",
        "memory_updates",
        "context_budget",
        "conversation_transition",
        "resume_protocol",
    ):
        if key not in data:
            errors.append(f"missing required key: {key}")

    task_type = data.get("task_type")
    if task_type not in VALID_TASK_TYPES:
        errors.append(f"task_type must be one of {sorted(VALID_TASK_TYPES)}")

    status_decision = data.get("status_decision")
    if status_decision not in VALID_STATUS_DECISIONS:
        errors.append(f"status_decision must be one of {sorted(VALID_STATUS_DECISIONS)}")

    evidence = require_object(data, "evidence_gate", errors)
    sources_read = require_list(evidence, "sources_read", errors) if evidence else []
    if evidence and evidence.get("done") is not True:
        errors.append("evidence_gate.done must be true for non-trivial tasks")
    if evidence and not sources_read and task_type not in {"upgrade", "documentation"}:
        errors.append("evidence_gate.sources_read must not be empty")

    implementation = require_object(data, "implementation", errors)
    changed_files = require_list(implementation, "changed_files", errors) if implementation else []
    app_code_changed = implementation.get("app_code_changed") if implementation else None
    if app_code_changed is not None and not isinstance(app_code_changed, bool):
        errors.append("implementation.app_code_changed must be boolean")
    if app_code_changed and not changed_files:
        errors.append("implementation.changed_files must not be empty when app_code_changed is true")
    if task_type == "upgrade" and app_code_changed:
        errors.append("task_type upgrade must not change app code")

    verification = require_object(data, "verification", errors)
    commands_run = require_list(verification, "commands_run", errors) if verification else []
    commands_failed = require_list(verification, "commands_failed", errors) if verification else []
    not_run_reason = verification.get("not_run_reason") if verification else None
    if app_code_changed and not commands_run and not not_run_reason:
        errors.append("verification.commands_run or verification.not_run_reason is required when app code changed")
    if status_decision == "done" and commands_failed and not not_run_reason:
        errors.append("status_decision done requires failed commands to be justified")

    e2e = require_object(data, "e2e_user_tests", errors)
    e2e_items = require_list(e2e, "items", errors) if e2e else []
    e2e_required = e2e.get("required") if e2e else None
    if e2e_required is not None and not isinstance(e2e_required, bool):
        errors.append("e2e_user_tests.required must be boolean")
    if (status_decision == "user_testing" or e2e_required is True) and not e2e_items:
        errors.append("e2e_user_tests.items must not be empty when user testing is required")

    memory = require_object(data, "memory_updates", errors)
    if memory:
        for key in ("sr_lots_updated", "current_state_updated", "task_memory_updated", "gate_report_updated"):
            if key in memory and not isinstance(memory[key], bool):
                errors.append(f"memory_updates.{key} must be boolean")
        if memory.get("task_memory_updated") is not True:
            errors.append("memory_updates.task_memory_updated must be true for non-trivial tasks")
        if (
            task_type in {"upgrade", "realign"}
            and status_decision in {"done", "user_testing"}
            and memory.get("current_state_updated") is not True
        ):
            errors.append("task_type upgrade/realign requires memory_updates.current_state_updated true")
        if memory.get("gate_report_updated") is not True and task_type not in {"analysis"}:
            warnings.append("memory_updates.gate_report_updated is false")

    context = require_object(data, "context_budget", errors)
    context_status = None
    next_prompt = None
    if context:
        if context.get("checked") is not True:
            errors.append("context_budget.checked must be true")
        context_status = context.get("status")
        if context_status not in VALID_CONTEXT_STATUS:
            errors.append(f"context_budget.status must be one of {sorted(VALID_CONTEXT_STATUS)}")
        next_prompt = context.get("next_session_prompt")
        if next_prompt not in VALID_NEXT_PROMPT:
            errors.append(f"context_budget.next_session_prompt must be one of {sorted(VALID_NEXT_PROMPT)}")
        if context_status in {"orange", "red", "stale", "ambiguous"} and next_prompt not in {"created", "updated"}:
            errors.append("orange/red/stale/ambiguous context requires next_session_prompt created or updated")

    transition = require_object(data, "conversation_transition", errors)
    if transition:
        decision = transition.get("decision")
        if decision not in VALID_TRANSITION_DECISIONS:
            errors.append(f"conversation_transition.decision must be one of {sorted(VALID_TRANSITION_DECISIONS)}")
        reason = transition.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append("conversation_transition.reason must be a non-empty string")
        path = transition.get("next_session_prompt_path")
        if path is not None and (not isinstance(path, str) or not path.strip()):
            errors.append("conversation_transition.next_session_prompt_path must be null or a non-empty string")
        user_message_required = transition.get("user_message_required")
        if user_message_required is not None and not isinstance(user_message_required, bool):
            errors.append("conversation_transition.user_message_required must be boolean")

        if context_status in {"orange", "red", "stale", "ambiguous"} and decision != "stop_for_new_conversation":
            errors.append("orange/red/stale/ambiguous context requires conversation_transition.decision stop_for_new_conversation")
        if context_status == "yellow" and decision == "continue_current":
            warnings.append("yellow context should usually recommend a new conversation before a long next task")
        if next_prompt in {"created", "updated"} and not path:
            errors.append("conversation_transition.next_session_prompt_path is required when next_session_prompt is created or updated")
        if decision in {"recommend_new_conversation", "stop_for_new_conversation"} and next_prompt not in {"created", "updated"}:
            errors.append("new conversation decisions require next_session_prompt created or updated")
        if decision == "stop_for_new_conversation" and user_message_required is not True:
            errors.append("stop_for_new_conversation requires conversation_transition.user_message_required true")

    resume = require_object(data, "resume_protocol", errors)
    if resume:
        required = resume.get("required")
        if not isinstance(required, bool):
            errors.append("resume_protocol.required must be boolean")
        mode = resume.get("mode")
        if mode not in VALID_RESUME_MODES:
            errors.append(f"resume_protocol.mode must be one of {sorted(VALID_RESUME_MODES)}")
        next_user_prompt = resume.get("next_user_prompt")
        if next_user_prompt is not None and (not isinstance(next_user_prompt, str) or not next_user_prompt.strip()):
            errors.append("resume_protocol.next_user_prompt must be null or a non-empty string")
        plain_resume_default = resume.get("default_on_plain_resume")
        if plain_resume_default not in VALID_PLAIN_RESUME_DEFAULTS:
            errors.append(f"resume_protocol.default_on_plain_resume must be one of {sorted(VALID_PLAIN_RESUME_DEFAULTS)}")
        must_not_code = resume.get("must_not_code_before_user_validation")
        if must_not_code is not None and not isinstance(must_not_code, bool):
            errors.append("resume_protocol.must_not_code_before_user_validation must be boolean")

        if decision in {"recommend_new_conversation", "stop_for_new_conversation"}:
            if required is not True:
                errors.append("new conversation decisions require resume_protocol.required true")
            if mode not in {"strict_resume", "resume_and_continue"}:
                errors.append("new conversation decisions require resume_protocol.mode strict_resume or resume_and_continue")
            if not next_user_prompt:
                errors.append("new conversation decisions require resume_protocol.next_user_prompt")
            if plain_resume_default != "strict_resume":
                errors.append("new conversation decisions require default_on_plain_resume strict_resume")
        if decision == "stop_for_new_conversation":
            if mode != "strict_resume":
                errors.append("stop_for_new_conversation requires resume_protocol.mode strict_resume")
            if must_not_code is not True:
                errors.append("stop_for_new_conversation requires must_not_code_before_user_validation true")
        if mode == "strict_resume" and next_user_prompt:
            lowered = next_user_prompt.lower()
            if "ne code pas" not in lowered and "attends" not in lowered:
                warnings.append("strict resume prompt should explicitly say not to code or to wait for validation")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a SR loop contract JSON file.")
    parser.add_argument("--file", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.file)
    try:
        data = load_contract(path)
        errors, warnings = validate(data)
    except ValueError as exc:
        errors, warnings = [str(exc)], []

    result = {"file": str(path), "ok": not errors, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"SR loop contract: {path}")
        if errors:
            print("Errors:")
            for item in errors:
                print(f"- {item}")
        if warnings:
            print("Warnings:")
            for item in warnings:
                print(f"- {item}")
        if not errors:
            print("OK: SR loop contract passed")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
