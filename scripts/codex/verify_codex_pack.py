#!/usr/bin/env python3
from pathlib import Path
import sys
installed_req=['AGENTS.md','DESIGN.md','docs/CURRENT_STATE.md','docs/codex/PROJECT_PROFILE.yaml','docs/codex/SKILL_MAP.md','docs/codex/SKILL_DIGEST.md','docs/codex/V3_UPGRADE_TEST_PLAN.md','docs/codex/WORKFLOW_CODEX.md','docs/codex/SR_BOOTSTRAP.md','docs/codex/SR_METHOD.md','docs/codex/SR_DEVELOPMENT_METHOD.md','docs/codex/SR_AGENT_METHOD.md','docs/codex/SR_HARNESS_METHOD.md','docs/codex/LOT_EXECUTION_METHOD.md','docs/codex/SR_PACK_VERSION.json','docs/codex/SR_LOTS.yaml','docs/codex/SR_INBOX.yaml','docs/codex/AI_AGENT_RUNTIME_METHOD.md','docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md','docs/codex/PROJECT_SKILLS_POLICY.md','docs/codex/CODEBASE_MAP.md','docs/codex/REPO_MAP_POLICY.md','docs/codex/TOKEN_OPTIMIZATION.md','docs/codex/project-skills/README.md','docs/codex/prompts/05_upgrade_codex_environment.md','docs/codex/prompts/06_verify_sr_installation.md','docs/codex/prompts/07_realign_sr_state_after_upgrade.md','docs/codex/tasks/_TEMPLATE/task_plan.md','docs/codex/tasks/_TEMPLATE/gate_report.md','docs/codex/tasks/_TEMPLATE/loop_contract.json','docs/codex/tasks/_TEMPLATE/sr_contract.json','docs/codex/tasks/_TEMPLATE/context_pack.md','docs/codex/tasks/_TEMPLATE/NEXT_SESSION_PROMPT.md','docs/codex/tasks/_TEMPLATE/session_resume.md','docs/codex/tasks/_TEMPLATE/verification.md','docs/adr/ADR_TEMPLATE.md','scripts/codex/audit_codex_pack.py','scripts/codex/audit_sr_project.py','scripts/codex/audit_sr_task_contracts.py','scripts/codex/context_budget_report.py','scripts/codex/find_next_session_prompt.py','scripts/codex/sr_post_install_check.py','scripts/codex/generate_repo_map.py','scripts/codex/validate_skills.py','scripts/codex/validate_lot_contract.py','scripts/codex/validate_loop_contract.py','scripts/codex/validate_sr_contract.py','scripts/codex/validate_scope.py','scripts/codex/aurora_token_run.py']
source_req=['README.md','INSTALLATION.md','MANIFEST.json','core/AGENTS.template.md','core/SR_BOOTSTRAP.md','core/SR_METHOD.md','core/SR_HARNESS_METHOD.md','core/LOT_EXECUTION_METHOD.md','core/SR_PACK_VERSION.json','prompts/05_upgrade_codex_environment.md','prompts/06_verify_sr_installation.md','prompts/07_realign_sr_state_after_upgrade.md','tasks/_TEMPLATE/task_plan.md','tasks/_TEMPLATE/gate_report.md','tasks/_TEMPLATE/loop_contract.json','tasks/_TEMPLATE/sr_contract.json','scripts/install_codex_pack.py','scripts/codex/audit_codex_pack.py','scripts/codex/sr_post_install_check.py','scripts/codex/validate_lot_contract.py','scripts/codex/validate_loop_contract.py','scripts/codex/validate_sr_contract.py','profiles/default/PROJECT_PROFILE.yaml']
source_mode=Path('core/SR_BOOTSTRAP.md').exists() and not Path('docs/codex/SR_BOOTSTRAP.md').exists()
req=source_req if source_mode else installed_req
missing=[p for p in req if not Path(p).exists()]
if missing:
    print('Missing files:'); [print('-',p) for p in missing]; sys.exit(1)
if not source_mode:
    lines=Path('AGENTS.md').read_text(encoding='utf-8').splitlines()
    if len(lines)>300: print(f'WARNING: AGENTS.md long ({len(lines)} lines)')
checks={
    'AGENTS.md':['SR Bootstrap obligatoire','AI_AGENT_RUNTIME_METHOD','DOMAIN_EXPERTISE_BOOTSTRAP','Memoire SR','aurora-lot-runner','Evidence gate obligatoire','Fact Gate obligatoire','Backlog Mutation Gate','Global Impact Gate','Tests E2E utilisateur','Context budget gate','Self Evaluation Gate','Loop Contract','find_next_session_prompt.py','SKILL_DIGEST.md','validate_lot_contract.py','Validation humaine stricte'],
    'docs/codex/WORKFLOW_CODEX.md':['Bootstrap obligatoire','Agents IA runtime','Domaine metier'],
    'docs/codex/SR_METHOD.md':['Specification Runtime','SR Development Method','SR Agent Method','Validation humaine stricte'],
    'docs/codex/SR_DEVELOPMENT_METHOD.md':['loop_contract.json','validate_loop_contract.py'],
    'docs/codex/SR_AGENT_METHOD.md':['AI_AGENT_RUNTIME_METHOD.md','output JSON schema','Pydantic Output Contract'],
    'docs/codex/SKILL_MAP.md':['Skills metier Codex','Skills runtime','aurora-lot-runner','SKILL_DIGEST.md'],
    'docs/codex/SKILL_DIGEST.md':['Skills methode globales','Skills metier Codex locales','Skills runtime applicatives','aurora-lot-runner','aurora-domain-skill-factory','docs/codex/project-skills'],
    'docs/codex/V3_UPGRADE_TEST_PLAN.md':['SR 3.0.0','Prompt initial pour projet pilote','validate_sr_contract.py','audit_sr_task_contracts.py'],
    'docs/codex/PROJECT_PROFILE.yaml':['require_sr_bootstrap_on_resume','require_agent_runtime_contract','domain_expertise','knowledge:','context_budget:','lot_naming:','require_sr_contract','require_loop_contract','require_conversation_transition_decision','digest:'],
    'docs/codex/SR_BOOTSTRAP.md':['compact/resume','Memoire de tache','Auto-reprise obligatoire','Reprise SR stricte','Validation humaine stricte'],
    'docs/codex/prompts/01_start_sr_session.md':['find_next_session_prompt.py','NEXT_SESSION_PROMPT.md','Reprise SR stricte','SR Contract 3.0.0','validate_sr_contract.py'],
    'docs/codex/prompts/05_upgrade_codex_environment.md':['https://github.com/syl2042/Aurora_SR_method_codex_pack','commit source','SR_PACK_SOURCE','validate_sr_contract.py','audit_sr_task_contracts.py'],
    'docs/codex/SR_HARNESS_METHOD.md':['SR Development Method','SR_INBOX.yaml','SR_LOTS.yaml','Evidence gate','Fact gate','Backlog Mutation Gate','Global Impact Gate','Lot Dependency Reconciliation','Execution multi-lots par defaut','Visibilite utilisateur obligatoire','Modes de connaissance codebase','Self evaluation gate','Loop Contract','SR Contract 3.0.0','validate_sr_contract.py','validate_lot_contract.py'],
    'docs/codex/LOT_EXECUTION_METHOD.md':['Boucle lot','Backlog Mutation Gate','Global Impact Gate','Design gate minimal','Context budget gate','Self evaluation gate','tests E2E utilisateur','loop_contract.json','sr_contract.json','validate_lot_contract.py'],
    'docs/codex/AI_AGENT_RUNTIME_METHOD.md':['SR Agent Method','output JSON schema','Pydantic Output Contract','invalid_output_policy','SQL libre','Human-in-the-loop'],
    'docs/codex/prompts/15_define_runtime_agents.md':['Pydantic obligatoire','politique d\'echec','tests de sortie typee'],
    'docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md':['DOMAIN_PROFILE','Regle de blocage'],
    'docs/codex/PROJECT_SKILLS_POLICY.md':['~/.codex/skills','docs/codex/project-skills','1024 caracteres'],
    'docs/codex/project-skills/README.md':['skills metier du projet','300 a 800 caracteres','25 a 64 caracteres'],
    'docs/codex/tasks/_TEMPLATE/gate_report.md':['Tests E2E utilisateur a faire','Backlog Mutation Gate','Global Impact Gate','Lot Dependency Reconciliation','Context Budget Gate','Self Evaluation Gate','Fact Gate','Knowledge Gate','Loop Contract'],
    'docs/codex/tasks/_TEMPLATE/loop_contract.json':['schema_version','status_decision','backlog_mutation_gate','global_impact_gate','e2e_user_tests','conversation_transition','resume_protocol'],
    'docs/codex/tasks/_TEMPLATE/sr_contract.json':['schema_version','validated_requests','backlog_mutation','global_impact','transition'],
    'docs/codex/tasks/_TEMPLATE/NEXT_SESSION_PROMPT.md':['NEXT_SESSION_PROMPT','Reprise SR stricte'],
    'scripts/codex/context_budget_report.py':['Context budget'],
    'scripts/codex/audit_sr_project.py':['SR project audit'],
    'scripts/codex/audit_sr_task_contracts.py':['SR 3.0.0','legacy task memories'],
    'scripts/codex/sr_post_install_check.py':['SR post-install check'],
    'scripts/codex/validate_loop_contract.py':['SR loop contract'],
    'scripts/codex/validate_sr_contract.py':['SR 3.0.0','validated_requests'],
    'scripts/codex/find_next_session_prompt.py':['NEXT_SESSION_PROMPT.md'],
    'docs/codex/prompts/06_verify_sr_installation.md':['sr_post_install_check.py','--fix-safe','SR Contract 3.0.0','audit_sr_task_contracts.py'],
    'docs/codex/prompts/07_realign_sr_state_after_upgrade.md':['audit SR de reprise','audit_sr_task_contracts.py','sr_contract.json'],
    'docs/codex/prompts/60_review_diff_before_close.md':['SR Contract 3.0.0','validate_sr_contract.py','validated_requests','validate_lot_contract.py'],
}
if source_mode:
    checks={
        'core/SR_BOOTSTRAP.md':['Memoire de tache','Auto-reprise obligatoire','Validation humaine stricte'],
        'core/SR_METHOD.md':['Specification Runtime','SR Development Method','SR Agent Method'],
        'core/SR_HARNESS_METHOD.md':['Backlog Mutation Gate','Global Impact Gate','Lot Dependency Reconciliation'],
        'core/LOT_EXECUTION_METHOD.md':['Backlog Mutation Gate','Global Impact Gate'],
        'core/V3_UPGRADE_TEST_PLAN.md':['SR 3.0.0','Prompt initial pour projet pilote','validate_sr_contract.py','audit_sr_task_contracts.py'],
        'prompts/05_upgrade_codex_environment.md':['https://github.com/syl2042/Aurora_SR_method_codex_pack','commit source','SR_PACK_SOURCE'],
        'scripts/install_codex_pack.py':['default','docs/codex/SR_BOOTSTRAP.md'],
        'scripts/codex/audit_codex_pack.py':['TARGET_VERSION'],
        'scripts/codex/sr_post_install_check.py':['SR post-install check'],
        'profiles/default/PROJECT_PROFILE.yaml':['default-project','knowledge:','context_budget:'],
    }
errors=[]
for path, markers in checks.items():
    txt=Path(path).read_text(encoding='utf-8')
    for marker in markers:
        if marker not in txt:
            errors.append(f'{path}: missing marker {marker!r}')
if errors:
    print('Content check errors:')
    [print('-',e) for e in errors]
    sys.exit(1)
print('OK: Codex pack files present')
