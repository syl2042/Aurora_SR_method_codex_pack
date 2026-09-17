# completion — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Lot Completion Gate

Le Lot Completion Gate est obligatoire avant toute cloture de lot ou de passe validee.

But : empecher qu'un sous-ensemble du lot valide soit livre comme si tout le lot etait termine.

Regles :

- une validation utilisateur engage tout le perimetre decrit juste avant validation ;
- `simple`, `chirurgical`, `scope minimal` et `eviter les refactors` ne peuvent jamais retirer une exigence validee ;
- si Codex veut reduire, reporter, decouper ou clarifier le lot valide, il doit stopper avant mutation et attendre une nouvelle validation ;
- `validated_requests` doit distinguer chaque lot, critere produit important, demande UI/UX explicite, exclusion et test humain/E2E ; une ligne globale multi-lots est invalide en 3.1.0 ;
- la cloture doit produire une table de couverture exigence par exigence, derivee du registre canonique ;
- un lot ne peut pas etre `done` si une exigence validee est `partiel`, `non fait`, `blocked` ou `requires_e2e` ;
- une exigence sortie du lot doit etre marquee `moved_to_new_lot` ou justifiee comme hors perimetre valide avec une decision explicite ;
- pour une exigence UI/UX, un build/lint/smoke HTTP ne suffit pas : il faut une preuve visuelle ou E2E ciblee, ou un statut `requires_e2e`.
- pour une exigence UI/UX significative dans SR 3.6.0, `build OK`, `lint OK`, tests unitaires OK et `HTTP 200 OK` ne constituent pas une preuve UI suffisante ;
- quand `ui_validation.required` vaut `true`, un lot ne peut etre `done` que si `UI Test Readiness Gate = pass` et `UI Visual Evidence Gate = pass`.

Format minimal 3.1.0 :

```text
Lot Completion Gate:
- status: pending/pass/fail/not_applicable
- coverage_table:
  | Exigence validee | Implementation | Preuve | Decision | Reste |
  |---|---|---|---|---|
- ui_ux_required: oui/non
- visual_evidence: [...]
- decision: done/user_testing/repair/blocked
```

Axes de ligne autorises :

```text
implementation_status: not_started, partial, complete, defective
evidence_status: not_required, missing, partial, failed, sufficient,
                 awaiting_user_acceptance, user_accepted
```

Decision :

- `done` seulement si toutes les exigences validees sont couvertes et les preuves suffisantes ;
- `user_testing` si la couverture technique est faite mais qu'un E2E utilisateur reste requis ;
- `repair` si une exigence est partielle ou non faite ;
- `blocked` si l'execution depend reellement d'une autorite, d'un acces, d'une source, d'un secret ou d'une decision externe absente.

Le validateur calcule ces decisions. Une implementation manquante ne peut donc pas etre masquee par `user_testing`. Si le gate est `fail`, les termes « termine », « complet », « livre » et « implemente » doivent etre qualifies et les exigences partielles ou absentes doivent etre listees dans la cloture et la reprise.

## Self evaluation gate

Apres implementation et avant cloture, Codex doit auto-evaluer son propre travail avec des preuves falsifiables :

- objectif initial ;
- ce que le code fait maintenant ;
- preuves : tests, logs, routes, screenshots, diff ;
- risques restants ;
- ce qui aurait pu etre oublie ;
- fichiers relus apres patch ;
- decision : `done`, `user_testing`, `repair` ou `blocked`.

## Regle de cloture

Avant de clore une tache SR-Harness :

- mettre a jour `progress.md` ;
- completer `verification.md` ;
- produire `gate_report.md` pour un lot execute ;
- produire le Lot Completion Gate avec table de couverture des exigences validees ;
- produire et valider `loop_contract.json` pour une tache non triviale ;
- mettre a jour `SR_LOTS.yaml` si le statut change ;
- si `SR_LOTS.yaml` a ete modifie, executer `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` et noter le resultat dans `verification.md` ;
- mettre a jour `CURRENT_STATE.md` selon la regle plein regime ;
- utiliser `aurora-review-diff`.

Format de cloture utilisateur recommande :

```text
| Demande utilisateur | Etat | Preuve | Reste a faire |

Resultat observe
Lecture expert / produit
Verifications executees
Memoire SR mise a jour
Tests E2E utilisateur a faire
Prochaine etape recommandee
```

Si le Completion Gate est rouge, cette cloture doit dire `repair` ou `blocked`, ou `user_testing` uniquement lorsque toute implementation technique est complete. Elle ne peut pas qualifier la passe de terminee, complete, livree ou implementee sans expliciter ce qui reste ouvert.

## Self evaluation gate

Apres patch et verification, relire le diff et les fichiers critiques modifies.

Documenter :

- objectif initial ;
- ce que le code fait maintenant ;
- preuves ;
- risques restants ;
- ce qui aurait pu etre oublie ;
- fichiers relus apres patch ;
- decision : `done`, `user_testing`, `repair` ou `blocked`.
- mutation backlog requise ou non ;
- impacts globaux non traites ;
- lots a verifier, rouvrir, bloquer ou creer.
- propagation incomplete possible : anciens appels, imports/exports, signatures, schemas, tests consommateurs ou smokes oublies.

## Cloture obligatoire

Avant de conclure une tache non triviale :
- completer `verification.md` ;
- creer ou mettre a jour `loop_contract.json` ;
- creer ou mettre a jour `sr_contract.json` si le projet declare SR 3.1.0 ; lire les contrats 3.0.0 en compatibilite ;
- appliquer le Lot Completion Gate : table de couverture des exigences validees, statut `fait/partiel/non fait/bloque/hors perimetre valide/requires_e2e`, preuve et commentaire ;
- appliquer le Propagation Gate si un symbole ou contrat partage a change : references ancien/nouveau nom recherchees, consommateurs verifies, imports/exports/signatures controles, references restantes justifiees, verification proportionnee executee ;
- refuser le statut `done` si `propagation_gate.required` ou `propagation.required` vaut `true` et que le gate n'est pas `pass` ;
- refuser le statut `done` si une exigence validee reste partielle, non faite, bloquee ou requiert un E2E non execute ;
- pour toute exigence UI/UX explicite, fournir une preuve visuelle ou E2E ciblee ; si l'implementation est complete mais la preuve manque, utiliser `user_testing`, sinon `repair`, jamais `done` ;
- executer `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json` si le contrat existe ;
- executer `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json` si le script existe ;
- executer ou documenter la verification impossible ;
- appliquer le Self Evaluation Gate : objectif atteint, preuves suffisantes, risques, oublis possibles, statut `done/user_testing/repair/blocked` ;
- utiliser `aurora-review-diff` ;
- mettre a jour `docs/CURRENT_STATE.md` pour tout upgrade SR, realignement SR, changement de version SR, creation de `NEXT_SESSION_PROMPT.md`, modification structurante de `SR_LOTS.yaml`, lot applicatif significatif passe en `done` ou `user_testing`, ou fin de session significative ;
- indiquer si `docs/CURRENT_STATE.md` a ete mis a jour et pourquoi ;
- indiquer si `docs/codex/CODEBASE_MAP.md` doit etre mis a jour.
- indiquer `NEXT_SESSION_PROMPT.md : cree / mis a jour / non requis` avec la raison ;
- indiquer `Conversation : continuer ici / recommander nouvelle conversation / stopper pour nouvelle conversation`.


## Regle distribuee par ancien installateur

- Lot Completion Gate obligatoire : verifier chaque demande validee separement ; une implementation absente, partielle ou defectueuse impose `repair`, tandis que `user_testing` exige une implementation technique complete et seulement une preuve E2E ou acceptation manquante.

## Regle distribuee par ancien installateur

- Self Evaluation Gate : apres patch, relire diff/fichiers critiques, verifier objectif, preuves, risques, oublis possibles, puis decider `done`, `user_testing`, `repair` ou `blocked`.

## Regle distribuee par ancien installateur

- En fin de tache non triviale, indiquer la memoire SR utilisee, les fichiers SR mis a jour, les gates, les tests E2E utilisateur a faire et le prochain lot recommande.

## Regle distribuee par ancien installateur

- Tests E2E utilisateur : les distinguer des tests unitaires et du build ; une implementation technique incomplete reste en `repair` meme si un E2E ou une acceptation manque aussi.

## Regle distribuee par ancien installateur

- En fin de tache non triviale, indiquer `NEXT_SESSION_PROMPT.md : cree / mis a jour / non requis` avec la raison, puis `Conversation : continuer ici / recommander nouvelle conversation / stopper pour nouvelle conversation`, et donner le prompt exact de reprise si une nouvelle conversation est recommandee.

## Regle distribuee par ancien installateur

- Cloture standard de lot : commencer par `Demande utilisateur | Etat | Preuve | Reste a faire`, puis resultat, verifications, memoire SR et prochaine etape. Ne jamais dire termine/complet/livre/implemente avec un Completion Gate rouge.
