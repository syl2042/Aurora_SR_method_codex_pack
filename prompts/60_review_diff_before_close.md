# Revue de diff avant cloture

Verifier demande, scope, securite, dependances/migrations, tests, CURRENT_STATE, RepoMap/KG, risques restants, appliquer le Fact Gate, le Propagation Gate si un symbole ou contrat partage a change, le Lot Completion Gate puis le Self Evaluation Gate, puis valider le SR Contract 3.1.0 (ou legacy 3.0.0) et le Loop Contract si la tache est non triviale.

Avant de dire `done` ou `lot termine`, produire une table de couverture :

| Exigence validee | Statut | Preuve | Commentaire |
|---|---|---|---|

Si une exigence a `implementation_status` `not_started`, `partial` ou `defective`, repondre corrections requises et utiliser `repair` (ou `blocked` pour un blocage externe reel avant demarrage). `user_testing` exige `implementation_status: complete` et seulement une preuve E2E/acceptation manquante. Pour une exigence UI/UX, un build/lint/smoke HTTP ne suffit pas. Commencer la cloture par la table `Demande utilisateur | Etat | Preuve | Reste a faire` et interdire tout langage de completude non qualifie si le gate est rouge.

Pour une UI/UX significative avec `ui_validation.required=true`, verifier dans `sr_contract.json` :

- `ui_validation.test_readiness.status = pass` ;
- `ui_validation.visual_evidence.status = pass` ;
- rapport Playwright present ;
- routes et viewports attendus testes ;
- screenshots attendus presents ;
- pas de redirection login inattendue ;
- pas de `pageerror` ;
- erreurs console/requestfailed traitees ;
- pas d'overflow horizontal inattendu.

Si l'un de ces points manque, ne pas declarer `done`.

Si un changement touche un symbole ou contrat partage, produire aussi :

- Propagation preflight annonce avant mutation : oui/non/N/A ;
- validation humaine requise et recue : oui/non/N/A ;
- symboles ou contrats modifies ;
- consommateurs detectes et verifies ;
- recherches de references executees ;
- references restantes et justifications ;
- typecheck/build/lint/tests/smoke/E2E proportionnes ;
- decision Propagation Gate : pass / repair / blocked / not_applicable.

Si le Propagation Gate est requis et n'est pas `pass`, ne pas declarer `done`.

Commande attendue si un contrat existe :

```bash
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
```

Commande attendue si un SR Contract existe :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Commande obligatoire si `docs/codex/SR_LOTS.yaml` a ete modifie :

```bash
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
```

`git diff --check` ne remplace pas cette validation du backlog.

Repondre OK cloture ou corrections requises avec :

- ce qui est fait ;
- resultat observe ;
- verifications executees ;
- validation `SR_LOTS.yaml` si le backlog a ete modifie ;
- memoire SR mise a jour ;
- Propagation Gate avec decision et preuves si applicable ;
- UI Test Readiness Gate et UI Visual Evidence Gate si UI significative ;
- Lot Completion Gate avec table de couverture et decision ;
- SR Contract 3.1.0 valide ou contrat 3.0.0 legacy explicitement signale, avec couverture granulaire `validated_requests` ;
- Loop Contract valide ou raison de non-applicabilite, avec decision `conversation_transition` et `resume_protocol` si reprise nouvelle conversation ;
- tests E2E utilisateur a faire ;
- prochain lot ou point d'arret.
