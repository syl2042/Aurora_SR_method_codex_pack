#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from validate_lot_contract import parse_simple_yaml, validate_lot
except Exception:
    parse_simple_yaml = None
    validate_lot = None


REQUIRED_PROFILE_MARKERS = [
    "require_sr_harness_for_multi_lot",
    "require_repo_map",
    "knowledge:",
    "sr_harness:",
    "context_budget:",
    "lot_naming:",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def source_or_installed(root: Path, installed: str, source: str) -> Path:
    p = root / installed
    if p.exists():
        return p
    return root / source


def check_markers(path: Path, markers: list[str], prefix: str) -> list[str]:
    text = read_text(path)
    if not text:
        return [f"{prefix}: missing {path}"]
    return [f"{prefix}: {path} missing marker {marker!r}" for marker in markers if marker not in text]


def lot_contract_errors(path: Path) -> list[str]:
    if not path.exists():
        return [f"lot_contract: missing {path}"]
    if parse_simple_yaml is None or validate_lot is None:
        return ["lot_contract: validator import unavailable"]
    data = parse_simple_yaml(path)
    lots = data.get("lots")
    if not isinstance(lots, list) or not lots:
        return ["lot_contract: no lots found"]
    errors = []
    seen = set()
    for index, lot in enumerate(lots):
        if not isinstance(lot, dict):
            errors.append(f"lot[{index}]: must be an object")
            continue
        lot_id = lot.get("lot_id")
        if lot_id in seen:
            errors.append(f"lot[{index}]: duplicate lot_id {lot_id!r}")
        seen.add(lot_id)
        errors.extend(validate_lot(lot, index))
    return errors


def collect_allowed_skills(profile: Path, skill_map: Path) -> set[str]:
    text = read_text(profile) + "\n" + read_text(skill_map)
    matches = re.findall(r"`([a-zA-Z0-9_.:-]+)`|-\s+([a-zA-Z0-9_.:-]+)\s*(?:#|$|:)", text.replace("\r", ""))
    allowed = set()
    for backtick, bullet in matches:
        value = backtick or bullet
        if value:
            allowed.add(value)
    return allowed


def task_plan_skill_warnings(root: Path, allowed: set[str]) -> list[str]:
    warnings = []
    task_roots = [root / "docs/codex/tasks", root / "tasks"]
    for task_root in task_roots:
        if not task_root.exists():
            continue
        for plan in task_root.glob("**/task_plan.md"):
            text = read_text(plan)
            match = re.search(r"## Skills[^\n]*\n(?P<body>.*?)(?:\n## |\Z)", text, re.S | re.I)
            if not match:
                continue
            for skill in re.findall(r"`([^`]+)`", match.group("body")):
                if skill and skill not in allowed and not skill.startswith("aurora-"):
                    warnings.append(f"skill_usage: {plan}: skill {skill!r} not declared in project allowlist")
    return warnings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    profile = source_or_installed(root, "docs/codex/PROJECT_PROFILE.yaml", "core/PROJECT_PROFILE.template.yaml")
    skill_map = source_or_installed(root, "docs/codex/SKILL_MAP.md", "core/SKILL_MAP.template.md")
    lots = source_or_installed(root, "docs/codex/SR_LOTS.yaml", "blueprints/sr_lots.template.yaml")
    agents = source_or_installed(root, "AGENTS.md", "core/AGENTS.template.md")
    repomap = source_or_installed(root, "docs/codex/CODEBASE_MAP.md", "core/CODEBASE_MAP.md")
    errors = []
    warnings = []
    errors.extend(check_markers(profile, REQUIRED_PROFILE_MARKERS, "project_profile"))
    errors.extend(check_markers(agents, ["SR Bootstrap obligatoire", "Context budget gate", "Self Evaluation Gate"], "agents"))
    errors.extend(check_markers(repomap, ["CODEBASE_MAP"], "repomap"))
    lot_errors = lot_contract_errors(lots)
    errors.extend(f"lot_contract: {err}" for err in lot_errors)
    allowed = collect_allowed_skills(profile, skill_map)
    warnings.extend(task_plan_skill_warnings(root, allowed))
    result = {
        "root": str(root),
        "profile": str(profile),
        "skill_map": str(skill_map),
        "lots": str(lots),
        "agents": str(agents),
        "repomap": str(repomap),
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"SR project audit: {root}")
        if errors:
            print("Errors:")
            for error in errors:
                print(f"- {error}")
        if warnings:
            print("Warnings:")
            for warning in warnings:
                print(f"- {warning}")
        if not errors:
            print("OK: SR project contract passed")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
