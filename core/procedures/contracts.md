# contracts — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Loop Contract

A partir de SR 2.4.0, toute tache non triviale doit produire un contrat court et validable :

```text
docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
```

Ce contrat ne contient pas les logs. Il pointe seulement les preuves minimales :

- en schema 1.1, le `sr_contract.json` canonique et toutes ses exigences ouvertes via `requirement_registry` ;
- table de couverture du Lot Completion Gate ;
- sources lues pour l'evidence gate ;
- mutation backlog et impact global si les gates sont applicables ;
- fichiers modifies ;
- commandes executees ou raison de non-execution ;
- liste E2E utilisateur concrete ;
- mises a jour memoire ;
- statut context budget et `NEXT_SESSION_PROMPT.md` ;
- decision de transition conversationnelle ;
- protocole de reprise a donner a l'utilisateur.

Regles critiques :

- si `status_decision` vaut `done`, `lot_completion_gate.status` doit valoir `pass` et aucune ligne de couverture ne doit etre `partiel`, `non fait`, `blocked` ou `requires_e2e` ;
- si `status_decision` vaut `user_testing`, `e2e_user_tests.items` doit contenir une vraie liste de tests ;
- `user_testing` est invalide si une ligne de couverture signale une implementation partielle, absente ou bloquee, ou si le Completion Gate vaut `fail` ;
- si du code applicatif change, `changed_files` et `verification.commands_run` ou `verification.not_run_reason` sont obligatoires ;
- si le contexte est `orange` ou `red`, `next_session_prompt` doit valoir `created` ou `updated`.
- si le contexte est `orange` ou `red`, `conversation_transition.decision` doit valoir `stop_for_new_conversation` ;
- si Codex recommande ou impose une nouvelle conversation, `conversation_transition.next_session_prompt_path` doit pointer vers le `NEXT_SESSION_PROMPT.md`.
- si Codex recommande ou impose une nouvelle conversation, `resume_protocol.required` doit valoir `true` et `resume_protocol.next_user_prompt` doit contenir le prompt exact a copier ;
- si le contexte est `orange` ou `red`, `resume_protocol.mode` doit valoir `strict_resume` et interdire de coder avant validation utilisateur.

Validation :

```bash
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
```

## SR Contract 3.1.0

A partir de SR 3.1.0, le contrat vivant cible d'un nouveau lot est :

```text
docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Il fusionne la partie machine de `task_plan.md`, `findings.md`, `decisions.md`, `verification.md`, `gate_report.md` et `loop_contract.json` autour d'une question principale : toutes les intentions utilisateur validees dans le lot sont-elles couvertes ?

Le validateur conserve la lecture des contrats 3.0.0. Il ne les convertit ni ne les reecrit automatiquement.

Champs structurants :

- `validated_requests` : intentions granulaires stables, origine lot/passe, implementation, preuves attendues/obtenues, travail/tests restants, historique et disposition ;
- `origin`, `intake` et `lineage` : validation d'origine, classification du retour et heritage obligatoire des exigences ouvertes ;
- `lot_completion_gate` : table de couverture avant cloture et decision de completude ;
- `scope` : inclus, exclus, chemins autorises/interdits ;
- `product_truth` : verites produit/metier a preserver ;
- `backlog_mutation` : mutation du backlog requise, effectuee ou justifiee ;
- `global_impact` : impact transverse analyse ou explicitement non requis ;
- `evidence` : sources lues, code lu, tests/logs ;
- `skills` : skills methode et metier ;
- `implementation` : fichiers modifies et code applicatif touche ou non ;
- `verification` : commandes executees, echecs, justification ;
- `gates` : evidence, scope, produit, verification, self evaluation, contexte ;
- `e2e` : tests utilisateur concrets ;
- `context` et `transition` : budget contexte et suite conversationnelle.

- `validated_requests` ne doit pas etre vide pour un lot non trivial ;
- les identifiants de requetes doivent etre uniques ;
- chaque exigence separe `implementation_status` et `evidence_status` ; son statut, le gate et le statut global sont derives ;
- une implementation `not_started`, `partial` ou `defective` impose `repair`, hors blocage externe reel avant demarrage ;
- `user_testing` exige une implementation `complete` pour toutes les exigences techniques ;
- un lot `done` est invalide si `lot_completion_gate.status` n'est pas `pass` ou si une exigence de la table de couverture reste partielle, non faite, bloquee ou en attente E2E ;
- si `lot_completion_gate.ui_ux_required` vaut `true`, une preuve visuelle ou E2E ciblee doit etre declaree avant `done` ;
- si `ui_validation.required` vaut `true`, `ui_validation.test_readiness.status` et `ui_validation.visual_evidence.status` doivent valoir `pass` avant `done` ;
- un lot `done` est invalide si une redirection login, un `pageerror` ou un overflow horizontal inattendu est declare dans `ui_validation` ;
- si une requete est `moved_to_new_lot`, elle doit pointer vers une entree inbox ou un lot cible dans ses notes, sa couverture ou les champs de mutation backlog ;
- si `global_impact.required` vaut `true`, les surfaces revues et la decision de sequence doivent etre renseignees ;
- si `backlog_mutation.mutation_required` vaut `true`, `SR_INBOX.yaml` ou `SR_LOTS.yaml` doit etre mis a jour, ou une raison de blocage/non-mutation doit etre explicite ;
- `product_truth.items` est obligatoire si `product_truth.required` vaut `true` ;
- `e2e.items` est obligatoire si `e2e.required` vaut `true` ;
- contexte `orange` impose `recommend_new_conversation` ou `stop_for_new_conversation` ;
- contexte `red`, `stale` ou `ambiguous` impose `stop_for_new_conversation`.

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Transition : les contrats 3.0.0 et les fichiers legacy restent historiques. Un contrat multi-lots reduit a une seule exigence generique produit un warning et doit etre normalise apres lecture de ses sources avant reprise ou cloture, sans reecriture massive.

## 8b. Loop contract

Completer `loop_contract.json` dans la memoire de tache.

Le contrat doit rester court et ne pas dupliquer les logs. Il doit declarer :

- `status_decision` ;
- en schema 1.1, `requirement_registry` avec le chemin du `sr_contract.json`, les exigences ouvertes, les lots rouverts, les retours utilisateur et le prochain bloc coherent ;
- `lot_completion_gate` avec table de couverture des exigences validees ;
- `evidence_gate.sources_read` ;
- `fact_gate.status` si le contrat local le declare ;
- `backlog_mutation_gate` si le contrat local le declare ;
- `global_impact_gate` si le contrat local le declare ;
- `propagation_gate` si le contrat local le declare ;
- `implementation.changed_files` ;
- `verification.commands_run` ou `verification.not_run_reason` ;
- `e2e_user_tests.items` si test reel requis ;
- `memory_updates` ;
- `context_budget` ;
- `conversation_transition` ;
- `resume_protocol`.

Valider :

```bash
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
```

## 8c. SR contract 3.1.0

Pour les nouveaux lots, completer `sr_contract.json` en schema 3.1.0. Le validateur continue a lire les contrats 3.0.0 sans les reecrire automatiquement.

Ce contrat doit etre mis a jour a chaque modification du lot :

- nouvelle demande utilisateur ;
- precision ou amendement du lot ;
- reparation apres test ;
- decision de sortir une demande vers un autre lot ;
- cloture technique ou passage en `user_testing`.

Le champ central est `validated_requests`. Chaque intention validee porte deux axes independants :

```text
implementation_status: not_started, partial, complete, defective
evidence_status: not_required, missing, partial, failed, sufficient,
                 awaiting_user_acceptance, user_accepted
```

Les preuves attendues et obtenues sont typees (`unit`, `build`, `runtime`, `visual`, `e2e`, `human_acceptance`, etc.). `evidence_status`, la decision de chaque exigence, le Completion Gate et le statut global sont derives par le validateur : ils ne sont pas quatre declarations independantes.

Le contrat doit aussi renseigner `lot_completion_gate` avant cloture :

```text
status: pending/pass/fail/not_applicable
coverage_table:
  - requirement_id
  - requirement
  - implementation_status
  - evidence_status
  - decision
  - proof
  - remaining_work
  - remaining_tests
ui_ux_required: true/false
visual_evidence: [...]
decision: done/user_testing/repair/blocked
```

Semantique obligatoire :

- implementation absente, partielle ou defectueuse : `repair` ;
- implementation complete et seule preuve E2E/acceptation manquante : `user_testing` ;
- verification unitaire, build ou runtime requise mais non executee : `repair` ;
- preuve executee et rouge : `repair` ;
- dependance reelle a une autorite, un acces, un secret ou une decision externe : `blocked` ;
- toutes les exigences implementees et suffisamment prouvees : `done`.

Si le gate est rouge, la cloture liste les exigences ouvertes et ne dit jamais sans qualification que le lot ou la passe est termine, complet, livre ou implemente.

Pour une exigence UI/UX, le gate exige une preuve visuelle ou E2E ciblee : capture Playwright, smoke visuel, checklist de composants/patterns ou justification d'impossibilite avec statut non `done`.

A partir de SR 3.6.0, pour une exigence UI/UX significative, un build, un lint, un test unitaire ou un HTTP 200 ne suffisent pas. Si `ui_validation.required` vaut `true`, le contrat doit declarer :

```text
ui_validation.test_readiness.status: pass
ui_validation.visual_evidence.status: pass
ui_validation.visual_evidence.report_file: output/playwright/ui-verification-report.json
```

Si l'authentification, le MFA, les secrets ou des donnees de test empechent l'automatisation, utiliser `blocked` ou `user_testing` avec une checklist E2E concrete, pas `done`.

Si une intention validee est reportee, annulee ou sortie du lot courant, renseigner `disposition` avec la source de decision et le lot cible pour `moved_to_new_lot`.

Le contrat doit aussi renseigner `propagation` quand un symbole ou contrat partage est modifie. Si `propagation.required` vaut `true`, `status` doit etre `pass` avant `done`, avec preflight, validation humaine si requise, recherches de references, consommateurs verifies et verification proportionnee.

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Pendant la transition 3.0.0 -> 3.1.0, conserver les fichiers legacy. `audit_sr_task_contracts.py` avertit sur les registres generiques ; leur normalisation exige une lecture humaine des sources et ne justifie pas une reecriture historique massive.

## Regle distribuee par ancien installateur

- SR Contract 3.1.0 : creer ou mettre a jour `docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json` quand `PROJECT_PROFILE.yaml` declare `require_sr_contract`, suivre chaque demande granulaire, separer implementation et preuve, heriter des exigences ouvertes, puis verifier avec `python3 scripts/codex/validate_sr_contract.py --file <chemin>`. Lire les contrats 3.0.0 en compatibilite.

## Regle distribuee par ancien installateur

- Loop Contract obligatoire pour toute tache non triviale : creer ou mettre a jour `docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json`, declarer `conversation_transition` et `resume_protocol`, puis verifier avec `python3 scripts/codex/validate_loop_contract.py --file <chemin>`.
