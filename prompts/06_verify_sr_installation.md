# Verifier l'installation SR

Tu travailles dans un repo equipe de la SR Method.

Objectif : verifier que l'installation ou l'upgrade SR est complet, coherent et utilisable avant de reprendre le developpement.

Ce n'est pas une passe de developpement applicatif.

Regles :

- Ne modifie aucun code applicatif.
- Ne cree aucune migration.
- Ne change aucune dependance.
- Ne touche pas aux secrets.
- Ne change jamais `knowledge.mode` de ta propre initiative.
- Ne renomme pas les lots legacy.
- Ne supprime pas de consignes projet non balisees sans validation.

Sources a lire :

1. `AGENTS.md`
2. `docs/codex/PROJECT_PROFILE.yaml`
3. `docs/codex/SKILL_MAP.md`
4. `docs/codex/SR_PACK_VERSION.json`
5. `docs/codex/SR_LOTS.yaml`
6. `docs/codex/SR_INBOX.yaml`
7. `docs/codex/SR_BOOTSTRAP.md`
8. `docs/codex/SR_HARNESS_METHOD.md`
9. `docs/codex/LOT_EXECUTION_METHOD.md`
10. `docs/codex/SR_METHOD.md`
11. `docs/codex/SR_DEVELOPMENT_METHOD.md`
12. `docs/codex/SR_AGENT_METHOD.md`

Etapes :

1. Lancer en lecture seule :

```bash
python3 scripts/codex/sr_post_install_check.py --root . --json
```

1b. Verifier aussi la reprise automatique :

```bash
python3 scripts/codex/find_next_session_prompt.py --root . --json
```

1c. Verifier aussi le contrat de boucle :

```bash
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json
```

1d. Verifier aussi le contrat SR 3.0.0 :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json
```

1e. Auditer les task memories legacy en lecture seule :

```bash
python3 scripts/codex/audit_sr_task_contracts.py --root .
```

1f. Valider le backlog vivant :

```bash
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
```

2. Analyser le resultat :
   - `errors` : bloquant ;
   - `warnings` : a expliquer ou corriger si mecanique ;
   - `fixed` : uniquement si `--fix-safe` a ete lance.

3. Si les erreurs sont mecaniques et non applicatives, proposer puis lancer :

```bash
python3 scripts/codex/sr_post_install_check.py --root . --fix-safe --json
```

4. Relancer ensuite :

```bash
python3 scripts/codex/sr_post_install_check.py --root . --json
```

5. Si des warnings restent, classer :
   - acceptable legacy ;
   - a documenter ;
   - a corriger avec validation ;
   - bloquant.

Corrections autorisees en `--fix-safe` :

- creer `agents/openai.yaml` manquant dans une skill locale si `SKILL.md` existe ;
- ajouter des champs SR manquants dans `PROJECT_PROFILE.yaml` sans ecraser l'existant ;
- creer un rapport dans `docs/codex/tasks/YYYY-MM-DD_sr-post-install-check/`.

Corrections interdites sans validation :

- renommer des lots ;
- passer `knowledge.mode` de `core` a `nexus_kg` ou inversement ;
- modifier du code applicatif ;
- supprimer des instructions projet dans `AGENTS.md` ;
- supprimer des task memories historiques ;
- modifier des skills globales.
- creer des contrats retroactifs pour toutes les anciennes taches.

Sortie attendue :

- version SR installee ;
- resultat du post-install check ;
- corrections appliquees, le cas echeant ;
- warnings restants ;
- dernier `NEXT_SESSION_PROMPT.md` detecte ou absent ;
- presence et validation du Loop Contract, incluant `conversation_transition` et `resume_protocol` ;
- presence et validation du SR Contract 3.0.0, incluant `validated_requests` ;
- resultat de `validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` ;
- resultat de `audit_sr_task_contracts.py`, avec contrats manquants acceptables en legacy, contrats invalides et migrations eventuelles a valider ;
- points bloquants ;
- prochaine etape recommandee : reprise normale, realignement SR, ou correction manuelle.
