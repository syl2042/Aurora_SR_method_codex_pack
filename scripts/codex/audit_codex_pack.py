#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

TARGET_VERSION = "3.0.3"

REQUIRED = {
    "AGENTS.md": [
        "SR Bootstrap obligatoire",
        "Memoire SR",
        "aurora-lot-runner",
        "Evidence gate obligatoire",
        "Tests E2E utilisateur",
        "Context budget gate",
        "Self Evaluation Gate",
        "SR Core = RepoMap",
        "find_next_session_prompt.py",
        "SKILL_DIGEST.md",
        "validate_lot_contract.py",
        "Validation humaine stricte",
    ],
    "docs/codex/SR_BOOTSTRAP.md": ["Memoire de tache", "Auto-reprise obligatoire", "Validation humaine stricte"],
    "docs/codex/SR_METHOD.md": ["Specification Runtime", "SR Development Method", "SR Agent Method", "sr_contract.json", "Validation humaine stricte"],
    "docs/codex/SR_DEVELOPMENT_METHOD.md": ["loop_contract.json", "validate_loop_contract.py"],
    "docs/codex/SR_AGENT_METHOD.md": ["AI_AGENT_RUNTIME_METHOD.md", "output JSON schema", "Pydantic Output Contract"],
    "docs/codex/prompts/01_start_sr_session.md": ["find_next_session_prompt.py", "NEXT_SESSION_PROMPT.md", "Reprise SR stricte", "SR Contract 3.0.0", "validate_sr_contract.py"],
    "docs/codex/prompts/05_upgrade_codex_environment.md": ["https://github.com/syl2042/Aurora_SR_method_codex_pack", "commit source", "SR_PACK_SOURCE", "validate_sr_contract.py", "audit_sr_task_contracts.py"],
    "docs/codex/SR_HARNESS_METHOD.md": ["SR Development Method", "SR_INBOX.yaml", "SR_LOTS.yaml", "Fact gate", "Execution multi-lots par defaut", "Visibilite utilisateur obligatoire", "Modes de connaissance codebase", "Self evaluation gate", "Loop Contract", "SR Contract 3.0.0", "validate_lot_contract.py"],
    "docs/codex/LOT_EXECUTION_METHOD.md": ["Boucle lot", "Evidence gate", "Self evaluation gate", "tests E2E utilisateur", "loop_contract.json", "sr_contract.json", "validate_lot_contract.py"],
    "docs/codex/SR_LOTS.yaml": ["lots:"],
    "docs/codex/SR_INBOX.yaml": ["items:"],
    "docs/codex/WORKFLOW_CODEX.md": ["SR-Harness", "Agents IA runtime", "validation humaine stricte"],
    "docs/codex/SKILL_MAP.md": ["aurora-lot-runner", "SKILL_DIGEST.md"],
    "docs/codex/SKILL_DIGEST.md": ["Skills methode globales", "Skills metier Codex locales", "Skills runtime applicatives"],
    "docs/codex/V3_UPGRADE_TEST_PLAN.md": ["SR 3.0.0", "Prompt initial pour projet pilote", "validate_sr_contract.py", "audit_sr_task_contracts.py"],
    "docs/codex/AI_AGENT_RUNTIME_METHOD.md": ["SR Agent Method", "output JSON schema", "Pydantic Output Contract", "invalid_output_policy"],
    "docs/codex/prompts/15_define_runtime_agents.md": ["Pydantic obligatoire", "politique d'echec", "tests de sortie typee"],
    "docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md": ["DOMAIN_PROFILE"],
    "docs/codex/PROJECT_SKILLS_POLICY.md": ["docs/codex/project-skills"],
    "docs/codex/tasks/_TEMPLATE/gate_report.md": ["Gate Report", "Tests E2E utilisateur a faire", "Context Budget Gate", "Self Evaluation Gate", "Fact Gate", "Knowledge Gate", "Loop Contract"],
    "docs/codex/tasks/_TEMPLATE/loop_contract.json": ["schema_version", "status_decision", "e2e_user_tests", "conversation_transition", "resume_protocol"],
    "docs/codex/tasks/_TEMPLATE/sr_contract.json": ["schema_version", "validated_requests", "transition"],
    "docs/codex/tasks/_TEMPLATE/context_pack.md": ["SR Context Pack"],
    "docs/codex/tasks/_TEMPLATE/NEXT_SESSION_PROMPT.md": ["NEXT_SESSION_PROMPT", "Reprise SR stricte"],
    "scripts/codex/validate_lot_contract.py": ["REQUIRED_LOT_FIELDS"],
    "scripts/codex/validate_scope.py": ["Scope gate failed"],
    "scripts/codex/context_budget_report.py": ["Context budget"],
    "scripts/codex/audit_sr_project.py": ["SR project audit"],
    "scripts/codex/audit_sr_task_contracts.py": ["SR 3.0.0", "legacy task memories"],
    "scripts/codex/sr_post_install_check.py": ["SR post-install check"],
    "scripts/codex/validate_loop_contract.py": ["SR loop contract"],
    "scripts/codex/validate_sr_contract.py": ["SR 3.0.0", "validated_requests"],
    "scripts/codex/find_next_session_prompt.py": ["NEXT_SESSION_PROMPT.md"],
    "docs/codex/prompts/06_verify_sr_installation.md": ["sr_post_install_check.py", "SR Contract 3.0.0", "audit_sr_task_contracts.py"],
    "docs/codex/prompts/07_realign_sr_state_after_upgrade.md": ["audit SR de reprise", "audit_sr_task_contracts.py", "sr_contract.json"],
    "docs/codex/prompts/60_review_diff_before_close.md": ["SR Contract 3.0.0", "validate_sr_contract.py", "validated_requests", "validate_lot_contract.py"],
}

SOURCE_REQUIRED = {
    "README.md": ["Public source package", "Install Into A Project"],
    "INSTALLATION.md": ["Install In A Target Project", "--profile default"],
    "MANIFEST.json": ["public_source", "profiles/default/PROJECT_PROFILE.yaml"],
    "core/SR_BOOTSTRAP.md": ["Memoire de tache", "Auto-reprise obligatoire", "Validation humaine stricte"],
    "core/SR_METHOD.md": ["Specification Runtime", "SR Development Method", "SR Agent Method"],
    "core/SR_HARNESS_METHOD.md": ["SR Development Method", "SR_INBOX.yaml", "SR_LOTS.yaml"],
    "core/LOT_EXECUTION_METHOD.md": ["Boucle lot", "loop_contract.json", "sr_contract.json"],
    "core/SR_PACK_VERSION.json": ["3.0.3"],
    "core/V3_UPGRADE_TEST_PLAN.md": ["SR 3.0.0", "Prompt initial pour projet pilote"],
    "prompts/05_upgrade_codex_environment.md": ["SR_PACK_SOURCE", "commit source"],
    "prompts/06_verify_sr_installation.md": ["sr_post_install_check.py"],
    "prompts/07_realign_sr_state_after_upgrade.md": ["audit SR de reprise"],
    "scripts/install_codex_pack.py": ["default", "docs/codex/SR_BOOTSTRAP.md"],
    "scripts/codex/verify_codex_pack.py": ["source_mode"],
    "scripts/codex/sr_post_install_check.py": ["SR post-install check"],
    "scripts/codex/validate_loop_contract.py": ["SR loop contract"],
    "scripts/codex/validate_sr_contract.py": ["SR 3.0.0", "validated_requests"],
    "profiles/default/PROJECT_PROFILE.yaml": ["default-project", "knowledge:", "context_budget:"],
}


def read_version(root: Path) -> str:
    path = root / "docs/codex/SR_PACK_VERSION.json"
    if not path.exists():
        path = root / "core/SR_PACK_VERSION.json"
    if not path.exists():
        return "unknown"
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("version", "unknown")
    except Exception:
        return "unreadable"


def audit(root: Path) -> tuple[list[str], list[str]]:
    missing = []
    stale = []
    required = SOURCE_REQUIRED if (root / "core/SR_BOOTSTRAP.md").exists() and not (root / "docs/codex/SR_BOOTSTRAP.md").exists() else REQUIRED
    for rel, markers in required.items():
        path = root / rel
        if not path.exists():
            missing.append(rel)
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in markers:
            if marker not in text:
                stale.append(f"{rel}: missing marker {marker!r}")
    installed = read_version(root)
    if installed != TARGET_VERSION:
        stale.append(f"docs/codex/SR_PACK_VERSION.json: installed_version {installed!r} != target {TARGET_VERSION!r}")
    return missing, stale


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Project root to audit")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    missing, stale = audit(root)
    result = {
        "root": str(root),
        "installed_version": read_version(root),
        "target_version": TARGET_VERSION,
        "missing": missing,
        "stale": stale,
        "ok": not missing and not stale,
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"SR pack audit: {root}")
        print(f"installed_version: {result['installed_version']}")
        print(f"target_version: {result['target_version']}")
        if missing:
            print("Missing:")
            for item in missing:
                print(f"- {item}")
        if stale:
            print("Stale or incomplete:")
            for item in stale:
                print(f"- {item}")
        if result["ok"]:
            print(f"OK: project aligned with SR pack {TARGET_VERSION} markers")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
