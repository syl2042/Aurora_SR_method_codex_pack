# V3_UPGRADE_TEST_PLAN.md

## Objectif
Guider l'upgrade SR 3.x d'un repository cible et le premier test de reprise sans modifier le code applicatif.

## Perimetre V3
SR 3.0.0 est la base de schema V3 ; le pack 3.0.3 distribue ces controles avec les corrections contexte, Fact Gate, CURRENT_STATE plein regime et Pydantic Output Contract pour les agents IA runtime. SR V3 ajoute notamment :
- `sr_contract.json` comme contrat vivant de lot ;
- `validate_sr_contract.py` et `audit_sr_task_contracts.py` ;
- `SKILL_DIGEST.md` comme routeur court de selection skills ;
- contexte hybride base sur cache, tokens non caches, tours et lots ;
- reprise stricte via `NEXT_SESSION_PROMPT.md`, `sr_contract.json` et `loop_contract.json`.

## Pre-requis
- Le repo cible doit etre propre ou les changements existants doivent etre identifies.
- Aucun secret ne doit etre affiche, copie ou commite.
- L'upgrade ne doit pas modifier le code applicatif, les migrations, les dependances ou la configuration sensible.
- Le repo source officiel doit etre disponible :

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

## Methode d'upgrade cible
Depuis le repo cible :

1. Verifier l'etat Git et le contexte SR existant.
2. Preparer `SR_PACK_SOURCE` vers un clone a jour du repo officiel.
3. Lire le prompt officiel a jour :

```text
<SR_PACK_SOURCE>/prompts/05_upgrade_codex_environment.md
```

4. Appliquer l'upgrade depuis la source officielle.
5. Verifier l'installation :

```bash
python3 scripts/codex/verify_codex_pack.py
python3 scripts/codex/audit_codex_pack.py --json
python3 scripts/codex/sr_post_install_check.py --root . --json
python3 scripts/codex/find_next_session_prompt.py --root . --json
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json
python3 scripts/codex/audit_sr_task_contracts.py --root . --json
git diff --check
```

6. Decider si un realignement projet est requis avant tout code applicatif :

```text
docs/codex/prompts/07_realign_sr_state_after_upgrade.md
```

Le `07` est obligatoire apres tout changement de version SR. Pour un upgrade mineur `3.x`, il peut rester court, mais il doit realigner `docs/CURRENT_STATE.md`, confirmer les prochains lots et stopper avant tout code applicatif.

## Test V3 minimal
Le test minimal attendu apres upgrade :
- `SR_PACK_VERSION.json` indique `3.0.3` ;
- `docs/codex/SKILL_DIGEST.md` existe et est reference par `AGENTS.md` / `SKILL_MAP.md` ;
- le template `sr_contract.json` est present et valide ;
- `audit_sr_task_contracts.py --root . --json` distingue les task memories legacy des contrats invalides ;
- `context_budget_report.py --root . --compact` retourne un statut fiable ou demande une reprise stricte ;
- aucune modification applicative n'a ete faite pendant l'upgrade.
- `docs/CURRENT_STATE.md` contient une entree structuree de l'upgrade SR et de la prochaine etape.

## Prompt initial pour projet pilote

```text
Utilise la methode SR.

Projet cible : /path/to/project
Objectif verifiable : mettre a jour uniquement la SR Method vers la version 3.0.3 depuis le repo officiel, verifier l'installation, puis stopper avant tout developpement applicatif.

Source officielle :
https://github.com/syl2042/Aurora_SR_method_codex_pack

Contraintes :
- ne modifie aucun code applicatif ;
- ne cree aucune migration ;
- ne change aucune dependance ;
- ne touche a aucun secret ;
- preserve les instructions projet existantes, docs metier, task memories, handoffs, SR_LOTS, SR_INBOX et project-skills ;
- si le contexte devient orange/rouge/stale/ambiguous, cree ou mets a jour un NEXT_SESSION_PROMPT.md et stoppe.

Etapes attendues :
1. Dans le projet cible, lis AGENTS.md s'il existe, docs/CURRENT_STATE.md si present et l'etat Git.
2. Prepare une source locale a jour du pack officiel dans SR_PACK_SOURCE ou dans un clone local fiable.
3. Verifie le remote et le commit source du pack.
4. Lis le prompt officiel a jour <SR_PACK_SOURCE>/prompts/05_upgrade_codex_environment.md.
5. Propose le plan d'upgrade, puis applique uniquement l'upgrade SR si les gates sont verts.
6. Lance les verifications V3 : verify_codex_pack.py, audit_codex_pack.py --json, sr_post_install_check.py --root . --json, find_next_session_prompt.py --root . --json, validate_loop_contract.py, validate_sr_contract.py, audit_sr_task_contracts.py --root . --json et git diff --check.
7. Execute ensuite docs/codex/prompts/07_realign_sr_state_after_upgrade.md apres tout changement de version SR, meme mineur, pour realigner `docs/CURRENT_STATE.md`, confirmer les prochains lots et stopper avant tout code applicatif.
8. Si le projet contient ou prevoit des agents IA runtime, signale que le prompt `15_define_runtime_agents.md` devra etre lance apres installation ou realignement.
9. Donne le rapport final : version avant/apres, commit source, fichiers SR modifies, fichiers projet preserves, verifications, warnings, dernier NEXT_SESSION_PROMPT, statut des contrats SR, decision sur `07`, agents IA runtime detectes, et prochaine etape.

Ne code pas de fonctionnalite applicative pendant cette passe.
```
