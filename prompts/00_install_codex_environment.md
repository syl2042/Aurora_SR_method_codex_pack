# Installer / verifier l'environnement SR Codex

Tu travailles dans un repo applicatif qui doit recevoir la SR Method.

Objectif : installer ou verifier l'environnement SR Method apres une premiere installation, sans modifier le code applicatif.

Terminologie :
- SR Method = doctrine generale Specification Runtime.
- SR Development Method = cadrage du developpement assiste par IA.
- SR Agent Method = agents IA runtime applicatifs.

Regles : ne modifie aucun code applicatif, ne cree aucune migration, n'ajoute aucune dependance applicative, ne touche pas aux secrets.

Etapes :
1. Lire AGENTS.md, PROJECT_PROFILE.yaml, WORKFLOW_CODEX.md, SR_BOOTSTRAP.md, SR_METHOD.md, SR_DEVELOPMENT_METHOD.md, SR_AGENT_METHOD.md, SR_HARNESS_METHOD.md, LOT_EXECUTION_METHOD.md, SKILL_MAP.md, SKILL_DIGEST.md, AI_AGENT_RUNTIME_METHOD.md, DOMAIN_EXPERTISE_BOOTSTRAP.md, PROJECT_SKILLS_POLICY.md, REPO_MAP_POLICY.md, TOKEN_OPTIMIZATION.md.
2. Verifier les skills methode dans ~/.codex/skills.
3. Creer docs/codex/tasks/YYYY-MM-DD_install-codex-environment/.
4. Verifier si les livrables domaine existent : DOMAIN_PROFILE, GLOSSARY, BUSINESS_RULES, RISK_REGISTER, HUMAN_VALIDATION_RULES.
5. Verifier que les skills metier projet sont prevues dans `docs/codex/project-skills/` et non copiees globalement par defaut.
6. Si le projet contient ou prevoit des agents IA, verifier la presence d'une section agents runtime dans SKILL_MAP et PROJECT_PROFILE.
7. Identifier le mode connaissance :
   - `core` : RepoMap obligatoire ;
   - `nexus_kg` : RepoMap + Nexus KG si le connecteur existe.
8. Lancer si possible verify_codex_pack.py, audit_codex_pack.py, audit_sr_project.py --root ., validate_lot_contract.py --file docs/codex/SR_LOTS.yaml, generate_repo_map.py --write, context_budget_report.py --root . --compact, validate_skills.py.
9. Verifier la presence de `docs/codex/tasks/_TEMPLATE/loop_contract.json` et `scripts/codex/validate_loop_contract.py`.
10. Valider le template : `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json`.
11. Verifier la presence de `docs/codex/tasks/_TEMPLATE/sr_contract.json` et `scripts/codex/validate_sr_contract.py`.
12. Valider le template : `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json`.
13. Auditer les task memories avec `python3 scripts/codex/audit_sr_task_contracts.py --root . --json`.
14. Si le projet contient ou prevoit des agents IA runtime, confirmer que `docs/codex/SR_AGENT_METHOD.md`, `docs/codex/AI_AGENT_RUNTIME_METHOD.md` et `docs/codex/prompts/15_define_runtime_agents.md` existent, puis recommander le prompt `15` apres validation.
15. Verifier RTK avec verify_rtk.sh si le script existe.
16. Produire rapport presents/manquants/prochaines actions.

Fin obligatoire : J'attends validation avant toute modification applicative.
