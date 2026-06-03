# Gate Report

## Lot

- Lot ID :
- Titre :
- Statut avant :
- Statut apres :

## Evidence Gate

- Statut : OK / KO / N/A
- Fichiers ou sources lus :
- Faits verifies :
- Hypotheses restantes :
- Questions bloquantes :
- Recommandations donnees uniquement apres verification locale possible : oui/non

## Fact Gate

- Statut : OK / KO / N/A
- Classification de la reponse : `opinion/methode` / `fait_verifiable` / `hypothese_non_verifiee`
- Faits verifiables affirmes :
- Sources consultees avant conclusion :
- Sources accessibles mais non consultees :
- Hypotheses non verifiees restantes :
- Verification minimale si hypothese :
- Conclusion factuelle autorisee : oui/non

## Knowledge Gate

- Statut : OK / KO / N/A
- Mode : `core` / `nexus_kg`
- RepoMap consulte :
- KG Nexus consulte :
- Fraicheur KG verifiee :
- Fichiers candidats identifies :
- Fichiers reellement relus :
- KG / RepoMap a mettre a jour :

## Scope Gate

- Statut : OK / KO / N/A
- `allowed_paths` respectes :
- `forbidden_paths` touches :
- Commentaire :

## Spec Gate

- Statut : OK / KO / N/A
- Criteres d'acceptation couverts :
- Criteres incomplets :

## Design Gate

- Statut : OK / KO / N/A
- Sources design lues :
- Composants/patterns utilises :
- Patterns interdits evites :
- Screenshot ou smoke visuel :

## Security Gate

- Statut : OK / KO / N/A
- Secrets ou donnees sensibles :
- Action critique :
- Validation humaine requise :

## Architecture Gate

- Statut : OK / KO / N/A
- DB/migration :
- Dependances :
- Service/runtime/RAG/Nexus :
- Rollback :

## Verification Gate

- Statut : OK / KO / N/A
- Commandes executees :
- Resultats :
- Verifications impossibles :

## Self Evaluation Gate

- Statut : OK / KO / N/A
- Objectif initial couvert :
- Ce que le code fait maintenant :
- Preuves :
- Risques restants :
- Ce qui aurait pu etre oublie :
- Fichiers relus apres patch :
- Decision de statut : `done` / `user_testing` / `repair` / `blocked`

## Loop Contract

- Statut : OK / KO / N/A
- Fichier : `docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json`
- Validation executee :
- Resultat :
- Si `user_testing`, liste E2E concrete presente : oui/non/N/A
- Si code applicatif modifie, `changed_files` et verifications declares : oui/non/N/A

## Tests E2E utilisateur a faire

- Parcours 1 :
- Parcours 2 :
- Donnees ou compte de test :
- Resultat attendu :
- Statut apres test utilisateur attendu : `user_testing` / `done`

## Diff Gate

- Statut : OK / KO / N/A
- Diff coherent :
- Refactor hors scope :
- Fichiers a surveiller :

## Context Budget Gate

- Statut : OK / KO / N/A
- Rapport `context_budget_report.py --root . --compact` :
- Pourcentage contexte :
- Statut contexte hybride : green / yellow / orange / red / unknown / stale / ambiguous
- Selection session fiable : oui/non
- Session utilisee :
- CWD session :
- Input tokens :
- Cached input tokens :
- Uncached input tokens :
- Cache ratio :
- Output tokens :
- Reasoning tokens :
- Rate limits :
- Signaux hybrides :
- Lots executes dans cette passe :
- Contexte sain pour continuer : oui/non
- Dernier `NEXT_SESSION_PROMPT.md` detecte au demarrage :
- `CURRENT_STATE.md` a mettre a jour :
- `NEXT_SESSION_PROMPT.md` cree/mis a jour :
- Handoff recommande :
- Raison si aucun handoff ou prompt de reprise :
- Decision conversation : continuer ici / recommander nouvelle conversation / stopper pour nouvelle conversation
- Raison decision conversation :
- Chemin `NEXT_SESSION_PROMPT.md` si cree/mis a jour :
- Prompt court fourni si reprise requise :

## Decision

- [ ] Continuer lot suivant
- [ ] Continuer jusqu'au maximum de 3 lots tant que gates verts
- [ ] Reparations necessaires
- [ ] Stop validation humaine
- [ ] Stop blocker technique
- [ ] Passer en `user_testing`

## Prochaines actions

-

## Cloture utilisateur recommandee

- Ce qui est fait :
- Resultat observe :
- Lecture expert / produit :
- Verifications executees :
- Memoire SR mise a jour :
- Loop Contract :
- Tests E2E utilisateur a faire :
- Prochaine etape recommandee :
