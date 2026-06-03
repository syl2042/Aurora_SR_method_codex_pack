#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


EXPECTED_VERSION = "3.0.3"
VALID_KNOWLEDGE_MODES = {"core", "nexus_kg"}

SKILL_AGENT_TEMPLATE = """\
interface:
  display_name: "{display_name}"
  short_description: "{short_description}"
"""

REPORT_TEMPLATE = """\
# SR Post Install Check

- created_at: {created_at}
- root: `{root}`
- fix_safe: {fix_safe}
- status: {status}

## Summary

- errors: {errors_count}
- warnings: {warnings_count}
- fixed: {fixed_count}

## Fixed

{fixed}

## Errors

{errors}

## Warnings

{warnings}
"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore
    except Exception:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def dump_yaml(path: Path, data: dict) -> None:
    import yaml  # type: ignore

    write_text(path, yaml.safe_dump(data, sort_keys=False, allow_unicode=False))


def run_command(root: Path, args: list[str]) -> dict:
    try:
        proc = subprocess.run(args, cwd=root, text=True, capture_output=True, timeout=120)
    except FileNotFoundError:
        return {"command": args, "returncode": 127, "stdout": "", "stderr": "command not found"}
    except subprocess.TimeoutExpired as exc:
        return {"command": args, "returncode": 124, "stdout": exc.stdout or "", "stderr": exc.stderr or "timeout"}
    return {"command": args, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def parse_json_output(result: dict) -> dict:
    try:
        return json.loads(result.get("stdout") or "{}")
    except Exception:
        return {}


def version(root: Path) -> str:
    path = root / "docs/codex/SR_PACK_VERSION.json"
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("version", "unknown")
    except Exception:
        return "unknown"


def check_required(root: Path) -> tuple[list[str], list[str]]:
    required = [
        "AGENTS.md",
        "docs/codex/PROJECT_PROFILE.yaml",
        "docs/codex/SKILL_MAP.md",
        "docs/codex/SKILL_DIGEST.md",
        "docs/codex/V3_UPGRADE_TEST_PLAN.md",
        "docs/codex/SR_PACK_VERSION.json",
        "docs/codex/SR_BOOTSTRAP.md",
        "docs/codex/SR_METHOD.md",
        "docs/codex/SR_DEVELOPMENT_METHOD.md",
        "docs/codex/SR_AGENT_METHOD.md",
        "docs/codex/SR_HARNESS_METHOD.md",
        "docs/codex/LOT_EXECUTION_METHOD.md",
        "docs/codex/SR_LOTS.yaml",
        "docs/codex/SR_INBOX.yaml",
        "docs/codex/prompts/06_verify_sr_installation.md",
        "docs/codex/prompts/07_realign_sr_state_after_upgrade.md",
        "docs/codex/prompts/05_upgrade_codex_environment.md",
        "scripts/codex/sr_post_install_check.py",
        "scripts/codex/find_next_session_prompt.py",
        "scripts/codex/validate_loop_contract.py",
        "scripts/codex/validate_sr_contract.py",
        "scripts/codex/audit_sr_task_contracts.py",
    ]
    errors = []
    warnings = []
    for rel in required:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")
    if version(root) != EXPECTED_VERSION:
        errors.append(f"SR version mismatch: installed={version(root)!r}, expected={EXPECTED_VERSION!r}")
    return errors, warnings


def check_markers(root: Path) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []
    marker_checks = {
        "AGENTS.md": ["Context budget gate", "Self Evaluation Gate", "Fact Gate", "SR Core = RepoMap", "find_next_session_prompt.py", "Loop Contract", "SKILL_DIGEST.md", "Validation humaine stricte"],
        "docs/codex/SR_METHOD.md": ["Specification Runtime", "SR Development Method", "SR Agent Method", "sr_contract.json", "Validation humaine stricte"],
        "docs/codex/SR_DEVELOPMENT_METHOD.md": ["loop_contract.json", "validate_loop_contract.py"],
        "docs/codex/SR_AGENT_METHOD.md": ["AI_AGENT_RUNTIME_METHOD.md", "output JSON schema"],
        "docs/codex/SKILL_MAP.md": ["Knowledge mode", "SKILL_DIGEST.md"],
        "docs/codex/SKILL_DIGEST.md": ["Skills methode globales", "Skills metier Codex locales", "Skills runtime applicatives"],
        "docs/codex/V3_UPGRADE_TEST_PLAN.md": ["SR 3.0.0", "Prompt initial pour projet pilote", "validate_sr_contract.py", "audit_sr_task_contracts.py"],
        "docs/codex/tasks/_TEMPLATE/gate_report.md": ["Knowledge Gate", "Fact Gate", "Self Evaluation Gate", "Context Budget Gate", "Loop Contract"],
        "docs/codex/tasks/_TEMPLATE/loop_contract.json": ["schema_version", "status_decision", "e2e_user_tests", "resume_protocol"],
        "docs/codex/tasks/_TEMPLATE/sr_contract.json": ["schema_version", "validated_requests", "transition"],
        "docs/codex/prompts/06_verify_sr_installation.md": ["sr_post_install_check.py", "--fix-safe", "SR Contract 3.0.0", "audit_sr_task_contracts.py"],
        "docs/codex/prompts/07_realign_sr_state_after_upgrade.md": ["audit SR de reprise", "audit_sr_task_contracts.py", "sr_contract.json"],
        "docs/codex/prompts/05_upgrade_codex_environment.md": ["https://github.com/syl2042/Aurora_SR_method_codex_pack", "commit source", "SR_PACK_SOURCE", "validate_sr_contract.py", "audit_sr_task_contracts.py"],
        "docs/codex/prompts/01_start_sr_session.md": ["find_next_session_prompt.py", "NEXT_SESSION_PROMPT.md", "Reprise SR stricte", "SR Contract 3.0.0", "validate_sr_contract.py"],
        "docs/codex/prompts/60_review_diff_before_close.md": ["SR Contract 3.0.0", "validate_sr_contract.py", "validated_requests"],
        "docs/codex/SR_BOOTSTRAP.md": ["find_next_session_prompt.py", "Auto-reprise obligatoire", "Reprise SR stricte", "Validation humaine stricte"],
        "scripts/codex/find_next_session_prompt.py": ["NEXT_SESSION_PROMPT.md"],
        "scripts/codex/validate_loop_contract.py": ["SR loop contract"],
        "scripts/codex/validate_sr_contract.py": ["SR 3.0.0", "validated_requests"],
        "scripts/codex/audit_sr_task_contracts.py": ["SR 3.0.0", "legacy task memories"],
    }
    for rel, markers in marker_checks.items():
        text = read_text(root / rel)
        if not text:
            errors.append(f"missing marker target: {rel}")
            continue
        for marker in markers:
            if marker not in text:
                errors.append(f"{rel}: missing marker {marker!r}")
    return errors, warnings


def check_knowledge(root: Path) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []
    profile = load_yaml(root / "docs/codex/PROJECT_PROFILE.yaml")
    knowledge = profile.get("knowledge") if isinstance(profile.get("knowledge"), dict) else {}
    mode = knowledge.get("mode")
    if mode not in VALID_KNOWLEDGE_MODES:
        errors.append("PROJECT_PROFILE.yaml: knowledge.mode must be 'core' or 'nexus_kg'")
        return errors, warnings
    if mode == "core":
        if not (root / "docs/codex/CODEBASE_MAP.md").exists():
            errors.append("knowledge.mode core requires docs/codex/CODEBASE_MAP.md")
    if mode == "nexus_kg":
        kg = knowledge.get("nexus_kg") if isinstance(knowledge.get("nexus_kg"), dict) else {}
        if not kg:
            errors.append("knowledge.mode nexus_kg requires knowledge.nexus_kg configuration")
        else:
            if "enabled" not in kg:
                warnings.append("knowledge.nexus_kg.enabled is missing")
            if not kg.get("context_pack"):
                warnings.append("knowledge.nexus_kg.context_pack is missing")
    return errors, warnings


def merge_profile_defaults(root: Path) -> list[str]:
    defaults_path = root / "docs/codex/PROJECT_PROFILE.yaml"
    if not defaults_path.exists():
        return []
    try:
        import yaml  # type: ignore
    except Exception:
        return []
    data = yaml.safe_load(defaults_path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return []
    changed = []
    if "knowledge" not in data:
        data["knowledge"] = {"mode": "core", "core_sources": ["docs/codex/CODEBASE_MAP.md"], "nexus_kg": {"enabled": False, "context_pack": "docs/codex/NEXUS_CONTEXT_PACK.md"}}
        changed.append("knowledge")
    if "knowledge" in data and isinstance(data["knowledge"], dict) and "mode" not in data["knowledge"]:
        data["knowledge"]["mode"] = "core"
        changed.append("knowledge.mode")
    if "sr_harness" not in data:
        data["sr_harness"] = {}
        changed.append("sr_harness")
    if isinstance(data["sr_harness"], dict) and "require_sr_contract" not in data["sr_harness"]:
        data["sr_harness"]["require_sr_contract"] = True
        changed.append("sr_harness.require_sr_contract")
    if isinstance(data["sr_harness"], dict) and "sr_contract_file" not in data["sr_harness"]:
        data["sr_harness"]["sr_contract_file"] = "docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json"
        changed.append("sr_harness.sr_contract_file")
    if isinstance(data["sr_harness"], dict) and "require_loop_contract" not in data["sr_harness"]:
        data["sr_harness"]["require_loop_contract"] = True
        changed.append("sr_harness.require_loop_contract")
    if isinstance(data["sr_harness"], dict) and "loop_contract_file" not in data["sr_harness"]:
        data["sr_harness"]["loop_contract_file"] = "docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json"
        changed.append("sr_harness.loop_contract_file")
    if isinstance(data["sr_harness"], dict) and "require_conversation_transition_decision" not in data["sr_harness"]:
        data["sr_harness"]["require_conversation_transition_decision"] = True
        changed.append("sr_harness.require_conversation_transition_decision")
    if isinstance(data["sr_harness"], dict) and "require_self_evaluation_gate" not in data["sr_harness"]:
        data["sr_harness"]["require_self_evaluation_gate"] = True
        changed.append("sr_harness.require_self_evaluation_gate")
    if "context_budget" not in data:
        data["context_budget"] = {"context_window_tokens": 258400}
        changed.append("context_budget")
    if isinstance(data.get("context_budget"), dict) and "require_transition_decision" not in data["context_budget"]:
        data["context_budget"]["require_transition_decision"] = True
        changed.append("context_budget.require_transition_decision")
    if "lot_naming" not in data:
        data["lot_naming"] = {"convention": "<PROJECT_KEY>-<AREA>-<SEQ>"}
        changed.append("lot_naming")
    if changed:
        dump_yaml(defaults_path, data)
    return changed


def skill_description(skill_file: Path) -> str:
    text = read_text(skill_file)
    name = skill_file.parent.name
    match = None
    for line in text.splitlines():
        if line.lower().startswith("description:"):
            match = line.split(":", 1)[1].strip()
            break
    description = match or f"Skill projet locale {name}."
    return description[:1000]


def short_description(skill_file: Path) -> str:
    desc = skill_description(skill_file)
    words = " ".join(desc.split())
    if len(words) < 25:
        words = f"Skill projet locale {skill_file.parent.name}"
    return words[:64].rstrip(" .,:;-")


def fix_local_skill_agents(root: Path) -> list[str]:
    fixed = []
    skills_root = root / "docs/codex/project-skills"
    if not skills_root.exists():
        return fixed
    for skill_file in skills_root.glob("*/SKILL.md"):
        agent = skill_file.parent / "agents/openai.yaml"
        if agent.exists():
            continue
        name = skill_file.parent.name
        display_name = name.replace("-", " ").title()
        text = SKILL_AGENT_TEMPLATE.format(display_name=display_name, short_description=short_description(skill_file))
        write_text(agent, text)
        fixed.append(f"created {agent.relative_to(root)}")
    return fixed


def lot_legacy_warnings(root: Path) -> list[str]:
    warnings = []
    data = load_yaml(root / "docs/codex/SR_LOTS.yaml")
    version_value = data.get("version")
    if version_value and str(version_value) != "0.2":
        warnings.append(f"SR_LOTS.yaml uses legacy version {version_value!r}; keep existing lot IDs, use 2.3 naming for new lots")
    if "project_key" not in data:
        warnings.append("SR_LOTS.yaml has no project_key; not blocking for legacy lots")
    if "lot_naming" not in data:
        warnings.append("SR_LOTS.yaml has no lot_naming block; not blocking for legacy lots")
    return warnings


def make_report(root: Path, result: dict, fix_safe: bool) -> Path:
    now = datetime.now(timezone.utc)
    report_dir = root / "docs/codex/tasks" / f"{now:%Y-%m-%d}_sr-post-install-check"
    fixed = "\n".join(f"- {item}" for item in result["fixed"]) or "- none"
    errors = "\n".join(f"- {item}" for item in result["errors"]) or "- none"
    warnings = "\n".join(f"- {item}" for item in result["warnings"]) or "- none"
    report = REPORT_TEMPLATE.format(
        created_at=now.isoformat(),
        root=root,
        fix_safe=fix_safe,
        status="OK" if result["ok"] else "ERROR",
        errors_count=len(result["errors"]),
        warnings_count=len(result["warnings"]),
        fixed_count=len(result["fixed"]),
        fixed=fixed,
        errors=errors,
        warnings=warnings,
    )
    path = report_dir / "verification.md"
    write_text(path, report)
    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fix-safe", action="store_true")
    ap.add_argument("--no-report", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    errors = []
    warnings = []
    fixed = []
    commands = []

    if args.fix_safe:
        fixed.extend(merge_profile_defaults(root))
        fixed.extend(fix_local_skill_agents(root))

    for checker in (check_required, check_markers, check_knowledge):
        e, w = checker(root)
        errors.extend(e)
        warnings.extend(w)
    warnings.extend(lot_legacy_warnings(root))

    command_specs = [
        [sys.executable, "scripts/codex/verify_codex_pack.py"],
        [sys.executable, "scripts/codex/audit_codex_pack.py", "--json"],
        [sys.executable, "scripts/codex/audit_sr_project.py", "--root", ".", "--json"],
        [sys.executable, "scripts/codex/audit_sr_task_contracts.py", "--root", ".", "--json"],
        [sys.executable, "scripts/codex/find_next_session_prompt.py", "--root", ".", "--json"],
        [sys.executable, "scripts/codex/validate_lot_contract.py", "--file", "docs/codex/SR_LOTS.yaml"],
        [sys.executable, "scripts/codex/validate_loop_contract.py", "--file", "docs/codex/tasks/_TEMPLATE/loop_contract.json"],
        [sys.executable, "scripts/codex/validate_sr_contract.py", "--file", "docs/codex/tasks/_TEMPLATE/sr_contract.json"],
    ]
    if (root / "docs/codex/project-skills").exists():
        command_specs.append([sys.executable, "scripts/codex/validate_skills.py", "--path", "docs/codex/project-skills"])

    for spec in command_specs:
        res = run_command(root, spec)
        commands.append(res)
        if res["returncode"] != 0:
            errors.append(f"command failed ({res['returncode']}): {' '.join(spec)}")
            if res.get("stderr"):
                warnings.append(res["stderr"].strip())
            elif res.get("stdout"):
                warnings.append(res["stdout"].strip())

    context_script = root / "scripts/codex/context_budget_report.py"
    if context_script.exists():
        res = run_command(root, [sys.executable, "scripts/codex/context_budget_report.py", "--root", ".", "--json"])
        commands.append(res)
        if res["returncode"] not in (0, 2):
            warnings.append(f"context budget command failed: {' '.join(res['command'])}")
        else:
            context = parse_json_output(res)
            if context.get("status") in {"orange", "red"}:
                warnings.append(f"context budget is {context.get('status')}: {context.get('recommended_action')}")

    result = {
        "root": str(root),
        "expected_version": EXPECTED_VERSION,
        "installed_version": version(root),
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "fixed": fixed,
        "commands": [
            {
                "command": item["command"],
                "returncode": item["returncode"],
                "stdout_preview": (item.get("stdout") or "")[:1000],
                "stderr_preview": (item.get("stderr") or "")[:1000],
            }
            for item in commands
        ],
    }
    if not args.no_report:
        result["report_path"] = str(make_report(root, result, args.fix_safe))

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"SR post-install check: {root}")
        print(f"installed_version: {result['installed_version']}")
        print(f"expected_version: {EXPECTED_VERSION}")
        if fixed:
            print("Fixed:")
            for item in fixed:
                print(f"- {item}")
        if errors:
            print("Errors:")
            for item in errors:
                print(f"- {item}")
        if warnings:
            print("Warnings:")
            for item in warnings:
                print(f"- {item}")
        if result.get("report_path"):
            print(f"report: {result['report_path']}")
        if result["ok"]:
            print("OK: SR post-install contract passed")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
