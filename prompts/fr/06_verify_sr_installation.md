# Verifier une installation SR Method

## SR 4.0.0 — version publiee

Mode `read_only` : aucune modification de fichier, correction automatique, installation ou restauration. Rapporter les ecarts ; toute correction releve d'un perimetre distinct a valider par `je valide`.

Ne modifie aucun fichier.

Objectif : prouver que chaque installation ou upgrade est complet, coherent et utilisable avant la reprise du developpement applicatif.

Pour chaque repository cible independamment :

1. Lire ses vrais marqueurs `AGENTS.md`, `docs/codex/SR_PACK_VERSION.json`, methode, contrats, lots, passes et task memories. Ne pas deduire la version d'un dossier depuis un autre.
2. Executer `python3 scripts/codex/verify_codex_pack.py`.
3. Executer `python3 scripts/codex/validate_release_docs.py --root . --json`.
4. Executer `python3 scripts/codex/audit_codex_pack.py --root . --json`.
5. Executer `python3 scripts/codex/sr_post_install_check.py --root . --json`.
6. Executer `python3 scripts/codex/audit_sr_task_contracts.py --root . --json`.
7. Valider `SR_LOTS.yaml`, `SR_PASSES.yaml`, les loop contracts actifs et le SR Contract 3.1.0 (ou les contrats legacy 3.0.0 explicitement identifies).
8. Verifier `docs/codex/CHANGELOG.md`, la version cible, les prompts publics localises et la preservation additive des fichiers projet.

Classer chaque warning comme etat legacy compatible, dette documentaire, `repair` ou blocage externe reel. Le code retour `0` de l'installateur ne suffit pas.

Produire une table par repository avec version, controles, erreurs, warnings, contrats, `validated_requests` ouvertes, preuves manquantes et prochaine action. `user_testing` est reserve au travail techniquement complet ; une implementation manquante reste `repair`.

Stopper sans corriger. Demander une validation exacte pour tout perimetre de reparation.

Parcours : installation neuve `00 -> 06` ; installation existante `05 -> 06 -> 07`. Le prompt `06` controle seulement ; `07` propose le realignement puis attend `je valide` avant modification de la memoire. Aucun developpement applicatif n'est autorise par ces parcours.
