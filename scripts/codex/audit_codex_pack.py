#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from validate_release_docs import audit as audit_release_docs

TARGET_VERSION = "3.7.0"

REQUIRED = {
    "AGENTS.md": [
        "SR Bootstrap obligatoire",
        "Memoire SR",
        "aurora-lot-runner",
        "Evidence gate obligatoire",
        "Backlog Mutation Gate",
        "Global Impact Gate",
        "Tests E2E utilisateur",
        "Context budget gate",
        "Self Evaluation Gate",
        "SR Core = RepoMap",
        "find_next_session_prompt.py",
        "SKILL_DIGEST.md",
        "validate_lot_contract.py",
        "Validation humaine stricte",
        "Propagation Gate",
    ],
    "docs/codex/SR_BOOTSTRAP.md": ["Memoire de tache", "Auto-reprise obligatoire", "Validation humaine stricte", "Lot Completion Gate", "Propagation Gate"],
    "docs/codex/SR_METHOD.md": ["Specification Runtime", "SR Development Method", "SR Agent Method", "sr_contract.json", "Validation humaine stricte", "Regle de completude", "Regle de propagation", "implementation_status", "existing_requirement_repair"],
    "docs/codex/SR_DEVELOPMENT_METHOD.md": ["loop_contract.json", "validate_loop_contract.py", "UI Verification Harness"],
    "docs/codex/SR_AGENT_METHOD.md": ["AI_AGENT_RUNTIME_METHOD.md", "output JSON schema", "Pydantic Output Contract"],
    "docs/codex/CHANGELOG.md": ["[Unreleased]", "[3.6.0]"],
    "docs/codex/prompts/01_start_sr_session.md": ["find_next_session_prompt.py", "NEXT_SESSION_PROMPT.md", "Reprise SR stricte", "SR Contract 3.1.0", "validate_sr_contract.py", "Propagation Gate"],
    "docs/codex/prompts/00_install_codex_environment.md": ["fresh_install", "3.7.0", "passes: []", "implementation_status", "evidence_status", "05_upgrade_codex_environment.md", "--write"],
    "docs/codex/prompts/05_upgrade_codex_environment.md": ["https://github.com/syl2042/Aurora_SR_method_codex_pack", "commit source", "SR_PACK_SOURCE", "upgrade_legacy_unknown", "2.2.0", "passes: []", "sr_post_install_check.py", "Lot Design Evidence Gate", "effet secondaire implicite", "sous-phase separee", "validate_sr_contract.py", "audit_sr_task_contracts.py", "Propagation Gate", "repository | marqueurs lus", "implementation_status", "evidence_status", "validated_requests"],
    "docs/codex/SR_HARNESS_METHOD.md": ["SR Development Method", "SR_INBOX.yaml", "SR_LOTS.yaml", "SR_PASSES.yaml", "Fact gate", "Backlog Mutation Gate", "Lot Design Evidence Gate", "Global Impact Gate", "Lot Dependency Reconciliation", "Pass Planning Gate", "Pass Runtime Goal", "Goal Length Gate", "Lot Completion Gate", "Propagation Gate", "UI Test Readiness Gate", "UI Visual Evidence Gate", "Execution multi-lots par defaut", "Visibilite utilisateur obligatoire", "Modes de connaissance codebase", "Self evaluation gate", "Loop Contract", "SR Contract 3.1.0", "validate_lot_contract.py", "validate_pass_contract.py", "build_pass_runtime_goal.py"],
    "docs/codex/LOT_EXECUTION_METHOD.md": ["Boucle lot", "Evidence gate", "Lot Design Evidence Gate", "Pass Planning Gate", "Pass Runtime Goal", "Goal Length Gate", "Backlog Mutation Gate", "Global Impact Gate", "Lot Completion Gate", "Propagation Gate", "ui_validation", "Self evaluation gate", "tests E2E utilisateur", "loop_contract.json", "sr_contract.json", "validate_lot_contract.py", "validate_pass_contract.py", "build_pass_runtime_goal.py"],
    "docs/codex/SR_LOTS.yaml": ["lots:"],
    "docs/codex/SR_PASSES.yaml": ["passes:"],
    "docs/codex/SR_INBOX.yaml": ["items:"],
    "docs/codex/WORKFLOW_CODEX.md": ["SR-Harness", "Agents IA runtime", "validation humaine stricte"],
    "docs/codex/SKILL_MAP.md": ["aurora-lot-runner", "SKILL_DIGEST.md"],
    "docs/codex/SKILL_DIGEST.md": ["Skills methode principales", "Skills metier Codex locales", "Skills runtime applicatives", "aurora-ui-visual-qa"],
    "docs/codex/V3_UPGRADE_TEST_PLAN.md": ["SR 3.0.0", "Prompt initial pour projet pilote", "validate_sr_contract.py", "audit_sr_task_contracts.py"],
    "docs/codex/AI_AGENT_RUNTIME_METHOD.md": ["SR Agent Method", "output JSON schema", "Pydantic Output Contract", "invalid_output_policy"],
    "docs/codex/prompts/15_define_runtime_agents.md": ["Pydantic obligatoire", "politique d'echec", "tests de sortie typee"],
    "docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md": ["DOMAIN_PROFILE"],
    "docs/codex/PROJECT_SKILLS_POLICY.md": ["docs/codex/project-skills"],
    "docs/codex/tasks/_TEMPLATE/gate_report.md": ["Gate Report", "Tests E2E utilisateur a faire", "Backlog Mutation Gate", "Lot Design Evidence Gate", "Global Impact Gate", "Lot Dependency Reconciliation", "Propagation Gate", "UI Test Readiness Gate", "UI Visual Evidence Gate", "Pass Runtime Goal", "Goal Length Gate", "Lot Completion Gate", "Context Budget Gate", "Self Evaluation Gate", "Fact Gate", "Knowledge Gate", "Loop Contract"],
    "docs/codex/tasks/_TEMPLATE/pass_runtime_goal.md": ["Pass Runtime Goal", "max_goal_command_chars: 1000", "hard_limit: 4000", "Pass Completion Gate"],
    "docs/codex/tasks/_TEMPLATE/loop_contract.json": ["schema_version", "status_decision", "requirement_registry", "lot_design_evidence_gate", "backlog_mutation_gate", "global_impact_gate", "propagation_gate", "lot_completion_gate", "e2e_user_tests", "conversation_transition", "resume_protocol"],
    "docs/codex/tasks/_TEMPLATE/sr_contract.json": ["schema_version", "validated_requests", "implementation_status", "evidence_status", "lineage", "closure", "lot_completion_gate", "design_evidence", "ui_validation", "backlog_mutation", "global_impact", "propagation", "transition"],
    "docs/codex/tasks/_TEMPLATE/context_pack.md": ["SR Context Pack"],
    "docs/codex/tasks/_TEMPLATE/NEXT_SESSION_PROMPT.md": ["NEXT_SESSION_PROMPT", "Reprise SR stricte"],
    "scripts/codex/validate_lot_contract.py": ["REQUIRED_LOT_FIELDS"],
    "scripts/codex/validate_pass_contract.py": ["SR_PASSES.yaml"],
    "scripts/codex/build_pass_runtime_goal.py": ["Pass Runtime Goal", "DEFAULT_MAX_GOAL_COMMAND_CHARS", "DEFAULT_HARD_LIMIT"],
    "scripts/codex/validate_scope.py": ["Scope gate failed"],
    "scripts/codex/context_budget_report.py": ["Context budget"],
    "scripts/codex/audit_sr_project.py": ["SR project audit"],
    "scripts/codex/audit_sr_task_contracts.py": ["SR 3.0.0", "legacy task memories"],
    "scripts/codex/sr_post_install_check.py": ["SR post-install check"],
    "scripts/codex/validate_loop_contract.py": ["SR loop contract", "lot_completion_gate", "propagation_gate"],
    "scripts/codex/validate_sr_contract.py": ["SR 3.0.0", "validated_requests", "lot_completion_gate", "propagation", "ui_validation"],
    "scripts/codex/validate_release_docs.py": ["PUBLIC_PROMPTS", "RELEASE_HISTORY", "release_status"],
    "scripts/codex/sr_completion_rules.py": ["implementation_status", "evidence_status", "derive_contract_decision"],
    "scripts/codex/test_install_upgrade_workflows.py": ["fresh_install", "existing SR installation detected", "heterogeneous_targets", "implementation_status", "evidence_status"],
    "scripts/codex/sr_ui_verify.mjs": ["ui_test_readiness_gate", "ui_visual_evidence_gate", "storageState"],
    "docs/codex/skills-method/aurora-ui-visual-qa/SKILL.md": ["UI Test Readiness Gate", "UI Visual Evidence Gate"],
    "scripts/codex/find_next_session_prompt.py": ["NEXT_SESSION_PROMPT.md"],
    "docs/codex/prompts/06_verify_sr_installation.md": ["sr_post_install_check.py", "SR Contract 3.1.0", "audit_sr_task_contracts.py", "Propagation Gate"],
    "docs/codex/prompts/07_realign_sr_state_after_upgrade.md": ["audit SR de reprise", "audit_sr_task_contracts.py", "sr_contract.json"],
    "docs/codex/prompts/08_define_sr_passes_from_lots.md": ["SR_PASSES.yaml", "Lot Design Evidence Gate", "validate_pass_contract.py"],
    "docs/codex/prompts/09_define_sr_lots_from_scope.md": ["SR_LOTS.yaml", "Lot Design Evidence Gate", "validate_lot_contract.py"],
    "docs/codex/prompts/60_review_diff_before_close.md": ["SR Contract 3.1.0", "validate_sr_contract.py", "validated_requests", "validate_lot_contract.py", "Lot Completion Gate", "Propagation Gate"],
}

SOURCE_REQUIRED = {
    "CHANGELOG.md": ["[Unreleased]", "[3.6.0]", "[3.0.4]"],
    "README.md": ["Public source package", "Install Into A Project"],
    "INSTALLATION.md": ["Install In A Target Project", "--profile default", "Choose The Correct Path First", "per-repository version matrix", "2.2.0", "passes: []", "implementation_status", "evidence_status"],
    "MANIFEST.json": ["public_source", "profiles/default/PROJECT_PROFILE.yaml", "blueprints/sr_passes.template.yaml"],
    "blueprints/runtime_agent_contract.template/agent_contract.yaml": ["product_action_scope", "internal_representation_contract", "user_message_builder", "tools_and_actions", "routing_policy"],
    "blueprints/runtime_agent_contract.template/README.md": ["framework-agnostic", "bounded product action", "runtime contract"],
    "core/SR_BOOTSTRAP.md": ["Memoire de tache", "Auto-reprise obligatoire", "Validation humaine stricte", "Lot Completion Gate", "Propagation Gate"],
    "core/SR_METHOD.md": ["Specification Runtime", "SR Development Method", "SR Agent Method", "Regle de completude", "Regle de propagation"],
    "core/SR_HARNESS_METHOD.md": ["SR Development Method", "SR_INBOX.yaml", "SR_LOTS.yaml", "SR_PASSES.yaml", "Backlog Mutation Gate", "Lot Design Evidence Gate", "Global Impact Gate", "Lot Dependency Reconciliation", "Pass Planning Gate", "Pass Runtime Goal", "Goal Length Gate", "Lot Completion Gate", "Propagation Gate", "UI Test Readiness Gate", "UI Visual Evidence Gate", "build_pass_runtime_goal.py"],
    "core/LOT_EXECUTION_METHOD.md": ["Boucle lot", "Lot Design Evidence Gate", "Pass Planning Gate", "Pass Runtime Goal", "Goal Length Gate", "Backlog Mutation Gate", "Global Impact Gate", "Lot Completion Gate", "Propagation Gate", "ui_validation", "loop_contract.json", "sr_contract.json", "build_pass_runtime_goal.py"],
    "core/SR_PACK_VERSION.json": ["3.7.0"],
    "core/V3_UPGRADE_TEST_PLAN.md": ["SR 3.0.0", "3.7.0", "Cibles heterogenes", "Prompt initial pour projet pilote"],
    "prompts/00_install_codex_environment.md": ["fresh_install", "3.7.0", "passes: []", "implementation_status", "evidence_status", "05_upgrade_codex_environment.md", "--write"],
    "prompts/05_upgrade_codex_environment.md": ["SR_PACK_SOURCE", "commit source", "upgrade_legacy_unknown", "2.2.0", "passes: []", "sr_post_install_check.py", "Lot Design Evidence Gate", "effet secondaire implicite", "sous-phase separee", "Propagation Gate", "repository | marqueurs lus", "implementation_status", "evidence_status", "validated_requests"],
    "scripts/codex/audit_sr_task_contracts.py": ["LEGACY_LOT_COMPLETION_GATE_CUTOFF", "legacy_compat"],
    "prompts/06_verify_sr_installation.md": ["sr_post_install_check.py", "Propagation Gate"],
    "prompts/07_realign_sr_state_after_upgrade.md": ["audit SR de reprise"],
    "prompts/08_define_sr_passes_from_lots.md": ["SR_PASSES.yaml", "Lot Design Evidence Gate", "validate_pass_contract.py"],
    "prompts/09_define_sr_lots_from_scope.md": ["SR_LOTS.yaml", "Lot Design Evidence Gate", "validate_lot_contract.py"],
    "prompts/en/08_define_sr_passes_from_lots.md": ["SR_PASSES.yaml", "Lot Design Evidence Gate", "validate_pass_contract.py"],
    "prompts/en/09_define_sr_lots_from_scope.md": ["SR_LOTS.yaml", "Lot Design Evidence Gate", "validate_lot_contract.py"],
    "prompts/fr/08_define_sr_passes_from_lots.md": ["SR_PASSES.yaml", "Lot Design Evidence Gate", "validate_pass_contract.py"],
    "prompts/fr/09_define_sr_lots_from_scope.md": ["SR_LOTS.yaml", "Lot Design Evidence Gate", "validate_lot_contract.py"],
    "prompts/es/08_define_sr_passes_from_lots.md": ["SR_PASSES.yaml", "Lot Design Evidence Gate", "validate_pass_contract.py"],
    "prompts/es/09_define_sr_lots_from_scope.md": ["SR_LOTS.yaml", "Lot Design Evidence Gate", "validate_lot_contract.py"],
    "prompts/de/08_define_sr_passes_from_lots.md": ["SR_PASSES.yaml", "Lot Design Evidence Gate", "validate_pass_contract.py"],
    "prompts/de/09_define_sr_lots_from_scope.md": ["SR_LOTS.yaml", "Lot Design Evidence Gate", "validate_lot_contract.py"],
    "prompts/pt/08_define_sr_passes_from_lots.md": ["SR_PASSES.yaml", "Lot Design Evidence Gate", "validate_pass_contract.py"],
    "prompts/pt/09_define_sr_lots_from_scope.md": ["SR_LOTS.yaml", "Lot Design Evidence Gate", "validate_lot_contract.py"],
    "scripts/install_codex_pack.py": ["default", "docs/codex/SR_BOOTSTRAP.md", "Fact Gate", "Lot Completion Gate", "Tests E2E utilisateur", "validate_lot_contract.py", "Lot Design Evidence Gate", "Propagation Gate", "existing SR installation detected", "SR_INSTALL_MARKERS"],
    "blueprints/sr_passes.template.yaml": ["passes: []"],
    "scripts/codex/fixtures/install_upgrade/legacy_layouts.json": ["2.2.0", "2.3.0", "2.3.5", "2.4.1", "3.0.0", "unknown_partial"],
    "scripts/codex/verify_codex_pack.py": ["source_mode"],
    "scripts/codex/sr_post_install_check.py": ["SR post-install check", "Propagation Gate", "ui_validation"],
    "scripts/codex/validate_pass_contract.py": ["SR_PASSES.yaml"],
    "scripts/codex/build_pass_runtime_goal.py": ["Pass Runtime Goal", "DEFAULT_MAX_GOAL_COMMAND_CHARS", "DEFAULT_HARD_LIMIT"],
    "scripts/codex/validate_loop_contract.py": ["SR loop contract", "propagation_gate"],
    "scripts/codex/validate_sr_contract.py": ["SR 3.0.0", "validated_requests", "propagation", "ui_validation"],
    "scripts/codex/validate_release_docs.py": ["PUBLIC_PROMPTS", "RELEASE_HISTORY", "release_status"],
    "scripts/codex/sr_completion_rules.py": ["implementation_status", "evidence_status", "derive_contract_decision"],
    "scripts/codex/sr_ui_verify.mjs": ["ui_test_readiness_gate", "ui_visual_evidence_gate", "storageState"],
    "skills-method/aurora-ui-visual-qa/SKILL.md": ["UI Test Readiness Gate", "UI Visual Evidence Gate"],
    "profiles/default/PROJECT_PROFILE.yaml": ["default-project", "knowledge:", "context_budget:", "require_propagation_gate_for_reference_changes", "ui_validation:"],
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
    stale.extend(f"release_docs: {error}" for error in audit_release_docs(root))
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
