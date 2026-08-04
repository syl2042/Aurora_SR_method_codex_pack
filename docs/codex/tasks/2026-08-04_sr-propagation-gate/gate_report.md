# Gate Report - SR propagation gate

## Evidence Gate

- Statut : pass
- Sources lues : `core/SR_HARNESS_METHOD.md`, `core/LOT_EXECUTION_METHOD.md`, `core/SR_METHOD.md`, `core/SR_BOOTSTRAP.md`, `core/AGENTS.template.md`, `tasks/_TEMPLATE/**`, `prompts/**`, `profiles/default/PROJECT_PROFILE.yaml`, validateurs et scripts d'audit.
- Preuves : implementation et tests listes dans `verification.md`.

## Fact Gate

- Statut : pass
- Fait verifie : le pack 3.2.2 ne contenait pas de gate dedie a la propagation des changements de symboles ou contrats partages.
- Fait verifie : les validateurs 3.3.0 refusent maintenant la cloture `done` si `propagation` ou `propagation_gate` est requis mais incomplet.

## Global Impact Gate

- Statut : pass
- Surfaces examinees : methode, templates, validateurs, audits, prompts, profil projet, script d'installation, post-install check et politique legacy.
- Decision : changement additif, sans migration applicative, avec warning non bloquant pour les contrats historiques.

## Propagation Gate

- Statut : pass
- Risque : high
- Symboles/contrats touches : `propagation_gate`, `propagation`, `require_propagation_gate_for_reference_changes`, `Propagation Gate`.
- Validation humaine : recue le 2026-08-04 via `je valide`.
- References verifiees : `rg -n "3\\.2\\.2|TARGET_VERSION|EXPECTED_VERSION|Propagation Gate|propagation_gate" core prompts tasks blueprints profiles scripts MANIFEST.json`.
- Consommateurs verifies : validateurs, tests unitaires, audits, post-install check, install upgrade block, templates et prompts.
- References restantes : aucune reference active a la version cible 3.2.2 ; les anciennes task memories restent historiques.
- Decision : pass.

## Lot Completion Gate

| Exigence | Statut | Preuve |
|---|---|---|
| Preflight d'impact avant mutation | fait | Methode, boucle lot, task template |
| Validation humaine proportionnee | fait | Methode, AGENTS template, profil projet |
| Postcheck de propagation | fait | Methode, gate report, contrats |
| Blocage `done` si gate incomplet | fait | Validateurs et tests |
| Upgrade multi-projets additif | fait | Audits, post-install, install script, version 3.3.0 |

Decision : done.

## Verification Gate

- Statut : pass
- Tests unitaires : OK, 31 tests.
- Templates contractuels : OK.
- Audit source pack : OK.
- Verification pack : OK.
- Installation temporaire + post-install : OK, warning context budget non bloquant.

## Self Evaluation Gate

- Statut : pass
- Risque restant : les projets deja installes devront executer l'upgrade du pack pour recevoir 3.3.0.
- Risque accepte : les task memories historiques sans gate restent des warnings legacy, ce qui est intentionnel pour ne pas casser l'historique.
