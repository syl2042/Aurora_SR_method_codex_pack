# Verifier l'installation SR

Mode `read_only` : aucune modification de fichier, correction automatique, installation ou restauration. Rapporter les ecarts ; toute correction releve d'un perimetre distinct a valider par `je valide`.

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

Sources : lire `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md`, le profil et les marqueurs installes. Utiliser les audits ci-dessous pour verifier les contrats, lots, passes, skills et outils. Charger les procedures specialisees uniquement pour comprendre un ecart ou satisfaire un gate applicable ; ne pas relire toute la methode.

Etapes :

1. Lancer en lecture seule :

```bash
python3 scripts/codex/sr_post_install_check.py --root . --json
```

1a. Verifier la coherence version, changelog et prompts publics localises :

```bash
python3 scripts/codex/validate_release_docs.py --root . --json
```

1b. Verifier aussi la reprise automatique :

```bash
python3 scripts/codex/find_next_session_prompt.py --root . --json
```

1c. Verifier aussi le contrat de boucle :

```bash
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json
```

1d. Verifier aussi le contrat SR 3.1.0 et la compatibilite de lecture 3.0.0 :

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

1g. Valider les passes si `SR_PASSES.yaml` existe :

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

1h. Verifier la presence UI Harness sans lancer d'auth :

```bash
node scripts/codex/sr_ui_verify.mjs --help
```

Pour un projet sans `ui_validation`, classer le resultat en warning legacy. Pour un projet authentifie, ne pas demander de credentials pendant la verification d'installation ; documenter simplement que `storage_state` ou `setup_command` devra etre configure avant un lot UI.

2. Classer chaque erreur comme bloquante et expliquer les warnings : legacy compatible, dette documentaire, correction a valider ou blocage.
3. Rapporter les corrections proposees sans les appliquer. Toute reparation exige un perimetre distinct valide par `je valide`, puis une nouvelle verification.
4. Les anciennes task memories sans `propagation_gate` sont acceptables legacy si elles precedent l'upgrade. Les nouveaux templates sans Propagation Gate sont bloquants.

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
- corrections proposees, aucune appliquee ;
- warnings restants ;
- `NEXT_SESSION_PROMPT.md` selectionne ou absent ; si `ambiguous`, demander un chemin explicite via `--prompt`, sans choisir `latest` silencieusement ;
- presence et validation du Loop Contract, incluant `conversation_transition` et `resume_protocol` ;
- presence et validation du SR Contract 3.1.0, ou compatibilite explicite 3.0.0, incluant un registre `validated_requests` granulaire ;
- resultat de `validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` ;
- resultat de `validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` si applicable ;
- resultat de `audit_sr_task_contracts.py`, avec contrats manquants acceptables en legacy, contrats invalides et migrations eventuelles a valider ;
- points bloquants ;
- prochaine etape recommandee : reprise normale, realignement SR, ou correction manuelle.

## SR 4
Voir le parcours contenu/fichiers de `05_upgrade_codex_environment.md`; aucune version precedente requise, preservation des adaptations, sauvegarde et restauration controlee.

Parcours : installation neuve `00 -> 06` ; installation existante `05 -> 06 -> 07`. Le prompt `06` controle seulement ; `07` propose le realignement puis attend `je valide` avant modification de la memoire. Aucun developpement applicatif n'est autorise par ces parcours.
