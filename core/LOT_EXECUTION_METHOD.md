# LOT_EXECUTION_METHOD.md

## Objectif

Definir la boucle d'execution standard d'un lot de la SR Development Method.

Cette methode est utilisee par `aurora-lot-runner`.

## Entrees attendues

- `docs/codex/SR_LOTS.yaml`
- `docs/codex/SR_INBOX.yaml` si present
- `docs/CURRENT_STATE.md`
- `docs/codex/CODEBASE_MAP.md`
- `docs/codex/CODEBASE_MAP.generated.md` si besoin
- `docs/codex/SKILL_MAP.md`
- Nexus KG si `PROJECT_PROFILE.yaml` active le mode `nexus_kg`
- specs indiquees par le lot
- skills metier pertinentes

## Boucle lot

### 1. Selection

Choisir le prochain lot executable :

- statut `validated` ou `reopened` ;
- dependances terminees ;
- non bloque ;
- risque compatible avec le niveau d'autonomie.

Priorite recommandee :

```text
reopened > validated > planned/proposed a cadrer
```

Ne pas coder un lot `proposed` sans validation si le changement est significatif.

Si plusieurs lots sont executables et que l'utilisateur a valide une phase autonome, une roadmap ou un gros brief, preparer une passe jusqu'a `max_lots_per_session` en commencant par `reopened`, puis `validated`.

Quand `docs/codex/SR_PASSES.yaml` existe, choisir une passe `validated` ou proposer une passe `planned` avant de coder. Une passe ne remplace pas les lots : elle declare seulement l'ordre, le preflight commun, les validations humaines et l'E2E groupe.

### 1b. Pass Planning Gate

Avant toute execution multi-lots, verifier la passe :

- les lots inclus existent dans `SR_LOTS.yaml` ;
- les dependances sont terminees, incluses plus tot dans la passe, ou placees dans une passe strictement anterieure quand la passe courante est encore `proposed` ou `planned` ;
- les passes `validated` et `in_progress` n'ont que des dependances anterieures reellement satisfaites (`done` ou `user_testing`) ;
- aucune dependance ne pointe vers une passe posterieure et aucun lot n'apparait dans plusieurs passes ;
- les lots `blocked`, `proposed` ou `superseded` ne sont pas executes silencieusement ;
- les secrets, identifiants, assets, URLs, services Docker ou comptes de test requis sont listes ;
- les migrations, actions externes et validations humaines sont explicites ;
- la strategie E2E indique `per_lot`, `grouped_at_pass_end` ou `not_required` ;
- les stop conditions couvrent gates, dependances, validation humaine et contexte.

Valider si possible :

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

Si le gate est rouge, stopper avant codage significatif et proposer le delta `SR_PASSES.yaml` ou `SR_LOTS.yaml`.

### 1c. Pass Runtime Goal

Si la passe est `validated` ou `in_progress` et que `PROJECT_PROFILE.yaml` active `sr_passes.pass_runtime_goal.enabled`, generer un artefact runtime avant l'execution :

```bash
python3 scripts/codex/build_pass_runtime_goal.py --pass-id <PASS_ID> --output docs/codex/tasks/YYYY-MM-DD_<pass-id>/pass_runtime_goal.md
```

Le goal est derive de `SR_PASSES.yaml` et `SR_LOTS.yaml`. Il ne remplace jamais les contrats SR.

Goal Length Gate obligatoire :

- `max_goal_command_chars: 1000` ;
- `hard_limit: 4000` ;
- si la commande `/goal` depasse `1000` caracteres apres regeneration compacte, stopper ;
- si elle depasse `4000` caracteres, stopper obligatoirement ;
- ne pas lancer un goal pour une passe `proposed` ;
- ne pas executer une passe `planned` sauf validation utilisateur explicite et changement de statut SR.

Si `e2e_strategy.mode` vaut `grouped_at_pass_end`, le goal doit interdire la demande d'E2E utilisateur lot par lot. Codex accumule les preuves automatisees puis produit une checklist E2E groupee en fin de passe.

### 2. Intake

Lire uniquement les sources requises :

- `required_sources` du lot ;
- RepoMap ;
- Nexus KG si actif ;
- fichiers candidats ;
- current state ;
- skill metier pertinente.

Creer ou reprendre une task memory.

Classer aussi l'evenement de backlog :

- execution d'un lot existant sans mutation ;
- precision dans le scope ;
- nouvelle fonction structurante ;
- dette ou bug qui depasse le lot courant ;
- decision produit ou technique impactant d'autres lots.

Si une fonction structurante ou une mutation durable est detectee, declencher `Backlog Mutation Gate` et, si plusieurs surfaces peuvent etre impactees, `Global Impact Gate` avant le plan court.

### 2b. Knowledge gate

Construire la carte du changement :

```text
RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs
```

En mode `core`, RepoMap suffit pour orienter.

En mode `nexus_kg`, interroger le KG avant de figer le scope et verifier la fraicheur si l'outil existe.

### 2c. Lot Design Evidence Gate

Avant de creer ou promouvoir un lot en `planned`, `validated`, `in_progress` ou `reopened`, prouver que le cadrage repose sur le code reel :

- fichiers candidats identifies depuis RepoMap/KG, recherche locale ou sources SR ;
- fichiers reellement lus avant plan engageant ;
- routes, composants, services, schemas, contrats, tests ou logs verifies quand ils existent ;
- hypotheses restantes et questions bloquantes listees ;
- justification explicite si le lot est greenfield ou pure documentation et que la lecture code est `not_applicable`.

Sans gate `pass` ou `not_applicable` justifie, le statut maximal est `proposed`.

### 3. Evidence gate

Avant de planifier ou coder, noter :

- fichiers lus ;
- faits verifies ;
- hypotheses restantes ;
- questions bloquantes.

Si la demande implique une supposition non verifiee et que les fichiers peuvent trancher, lire les fichiers avant de repondre.

Si l'evidence gate n'est pas fait, ne pas donner de plan engageant. Repondre d'abord par ce qui doit etre verifie ou effectuer la verification locale.

### 3b. Fact gate

Avant toute conclusion factuelle, y compris hors patch, classer les elements de reponse :

- `opinion/methode` : conseil general ou preference ; pas de preuve locale obligatoire ;
- `fait_verifiable` : affirmation sur un repo, produit, code, API, migration, flux UI, donnee, configuration ou comportement existant ;
- `hypothese_non_verifiee` : piste utile non encore prouvee.

Pour tout `fait_verifiable`, verifier la source disponible avant de repondre :

- code reel, tests, logs ou diff pour un comportement applicatif ;
- fichiers SR, task memory, contrats, backlog ou `CURRENT_STATE.md` pour l'etat methode/projet ;
- documentation officielle ou source primaire pour une API externe ;
- source metier documentee ou validation humaine pour une regle metier.

Si la source est accessible mais non lue, le gate est rouge : ne pas conclure, annoncer `Fact Gate non satisfait` et indiquer la source a verifier.

Si la verification est impossible ou disproportionnee, la reponse doit rester explicitement une `hypothese_non_verifiee` et fournir la verification minimale. Les formulations probabilistes ne remplacent pas une preuve.

### 3c. Backlog Mutation Gate

Avant le plan court et avant la cloture, determiner si la demande ou les preuves lues changent le backlog :

- nouvelle fonction structurante ou capacite transversale ;
- implication nouvelle sur un lot existant ;
- bug/reparation qui revele une dette hors scope ;
- changement de dependance, statut, priorite ou stop condition ;
- besoin de creer, rouvrir, bloquer, reporter, decouper ou remplacer un lot.

Si oui, mettre a jour `SR_INBOX.yaml` ou `SR_LOTS.yaml` selon le niveau de cadrage et le risque. Si le changement est significatif et non valide, creer une entree `proposed` ou `SR_INBOX` puis stopper avant codage significatif.

La task memory doit indiquer :

- `structural_change_detected` ;
- `mutation_required` ;
- fichiers backlog modifies ou raison de non-mutation ;
- lots affectes ;
- decision de sequence.

### 3d. Global Impact Gate

Si une fonction structurante est detectee, analyser l'impact global avant de figer le scope.

Surfaces a verifier quand elles existent :

- objectifs produit, parcours et roles ;
- donnees, schema, migration, retention, import/export ;
- permissions, validation humaine et securite applicative ;
- API, services, jobs, agents runtime et integrations ;
- navigation, UI, design system et accessibilite ;
- tests, fixtures, observabilite, logs et donnees de demonstration ;
- lots SR existants, decisions, task memories et stop conditions.

La sortie doit lister :

- surfaces revues ;
- lots impactes ;
- lots a creer ;
- lots a rouvrir, bloquer, reporter, decouper ou marquer `superseded` ;
- hypotheses restantes ;
- questions bloquantes ;
- recommandation de sequence.

Si l'impact global n'est pas analysable avec les sources disponibles, stopper avec `blocked` ou creer une entree `SR_INBOX` au lieu de coder.

### 3e. Lot Dependency Reconciliation

Apres un Global Impact Gate requis, relire les lots existants pertinents et les classer :

```text
unaffected, impacted, blocked_by, reopened, superseded, split_required, depends_on
```

Mettre a jour `depends_on`, `blocked_by`, `impacts`, `impacted_by`, `supersedes`, `superseded_by` ou le statut du lot si necessaire. Les lots non verifies ne doivent pas etre declares `unaffected` sans source.

### 3f. Propagation Gate preflight

Avant codage significatif, determiner si le changement prevu modifie un symbole ou contrat partage :

- fonction, methode, classe, hook, composant exporte, helper reutilise ;
- signature, parametre, type, interface ou schema ;
- endpoint, payload API, route, evenement, message ou champ DB ;
- cle de configuration, variable d'environnement, import/export public ;
- contrat agent runtime, prompt, tool/action, output schema ou binding controle.

Si oui, produire un preflight court :

- symboles ou contrats touches, ancien et nouveau comportement ;
- portee estimee : local, module, cross-module, API, DB ou runtime ;
- consommateurs detectes avec RepoMap/KG, `rg`, lecture code reel ou tests ;
- surfaces a risque et niveau `low`, `medium`, `high` ou `critical` ;
- strategie : propagation complete, shim de compatibilite, migration en deux temps ou non requis ;
- verifications prevues : recherches de references, typecheck/build/lint, tests consommateurs, smoke, E2E ;
- validation humaine requise et recue.

Stopper avant mutation si le risque est `high` ou `critical` et que la validation humaine n'est pas recue. En mode validation humaine stricte, stopper aussi pour un risque `medium`.

### 4. Plan court

Produire un plan de lot limite :

- modifications prevues ;
- fichiers candidats ;
- fichiers deja verifies par le Lot Design Evidence Gate ;
- tests ;
- risques ;
- stop conditions.

Ne pas elargir le lot sans enregistrer une decision.

Ne pas reduire le lot valide au nom de la simplicite. Si une exigence validee ne peut pas etre couverte dans ce lot, stopper avant mutation ou proposer explicitement un decoupage avec impacts et attendre une nouvelle validation.

Si `Global Impact Gate` est requis, le plan doit inclure la sequence de livraison recommandee et les lots qui ne doivent pas etre executes avant reconciliation.

### 4b. Validated Lot Execution Contract

Une validation utilisateur d'un lot ou d'une passe engage tout le perimetre decrit juste avant validation.

Hierarchie d'arbitrage :

1. securite, secrets, actions externes et validations humaines ;
2. perimetre valide utilisateur ;
3. contrat de lot ou de passe SR ;
4. criteres d'acceptation ;
5. simplicite, changements chirurgicaux et absence de refactor hors besoin ;
6. style local.

La simplicite s'applique donc a l'implementation de chaque exigence validee, jamais a la suppression silencieuse d'une exigence.

Avant codage significatif, extraire les exigences validees dans `validated_requests` et preparer la table de couverture attendue. Pour chaque exigence, indiquer la preuve minimale prevue : fichier, test, log, endpoint, capture, build, E2E ou justification.

Si le lot contient une exigence UI/UX explicite, prevoir une verification visuelle ou E2E ciblee. Un build, lint ou smoke HTTP ne suffit pas pour declarer une UI alignee sur une reference produit.

### 5. Implementation

Modifier uniquement les fichiers necessaires.

Respecter :

- `allowed_paths` ;
- `forbidden_paths` ;
- interdictions metier ;
- design gate si UI ;
- architecture gate si DB/RAG/service/runtime agent.

Si le Propagation Gate est requis, propager explicitement les appels, imports/exports, signatures, schemas et tests consommateurs identifies. Si une propagation complete n'est pas souhaitable, ajouter une compatibilite temporaire seulement avec justification, expiration ou lot de retrait.

### 6. Verification

Executer les commandes `verification_commands` du lot.

Si le Propagation Gate est requis, executer aussi le postcheck :

- recherches sur ancien et nouveau symbole ou contrat ;
- controle des references restantes et justification des exceptions ;
- verification des consommateurs directs ;
- typecheck/build/lint/tests/smoke/E2E proportionnes au risque.

Si une commande est impossible :

- expliquer pourquoi ;
- proposer un smoke alternatif ;
- ne pas masquer l'echec.

### 7. Repair loop

Si une verification echoue :

- diagnostiquer ;
- corriger au maximum `max_repair_attempts_per_lot` ;
- relancer la verification ciblee.

Si toujours rouge, stopper avec blocker clair.

### 8. Gate report

Completer `gate_report.md` :

- pass planning gate si execution multi-lots ;
- lot completion gate ;
- evidence gate ;
- fact gate ;
- backlog mutation gate ;
- global impact gate si fonction structurante ;
- lot dependency reconciliation si applicable ;
- propagation gate si symbole ou contrat partage modifie ;
- knowledge gate ;
- scope gate ;
- spec gate ;
- design gate si UI ;
- security gate ;
- architecture gate ;
- verification gate ;
- self evaluation gate ;
- diff gate ;
- context budget gate ;
- tests E2E utilisateur a faire ;
- decision continuer/reparer/stopper.

### 8b. Loop contract

Completer `loop_contract.json` dans la memoire de tache.

Le contrat doit rester court et ne pas dupliquer les logs. Il doit declarer :

- `status_decision` ;
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

### 8c. SR contract 3.0.0

Pour les projets SR 3.0.0, completer aussi `sr_contract.json`.

Ce contrat doit etre mis a jour a chaque modification du lot :

- nouvelle demande utilisateur ;
- precision ou amendement du lot ;
- reparation apres test ;
- decision de sortir une demande vers un autre lot ;
- cloture technique ou passage en `user_testing`.

Le champ central est `validated_requests`. Chaque intention validee doit avoir un statut explicite :

```text
todo, doing, done, requires_e2e, blocked, moved_to_new_lot, cancelled
```

Un lot ne peut pas etre `done` tant qu'une intention validee reste ouverte.

Le contrat doit aussi renseigner `lot_completion_gate` avant cloture :

```text
status: pass/fail/not_applicable
coverage_table:
  - requirement_id
  - requirement
  - status: fait/partiel/non fait/bloque/hors perimetre valide/requires_e2e
  - proof
  - comment
ui_ux_required: true/false
visual_evidence: [...]
decision: done/user_testing/repair/blocked
```

Si une ligne est `partiel`, `non fait`, `bloque` ou `requires_e2e`, le lot ne peut pas etre `done`. Il doit rester en `repair`, `user_testing` ou `blocked` avec les actions restantes visibles.

Pour une exigence UI/UX, le gate exige une preuve visuelle ou E2E ciblee : capture Playwright, smoke visuel, checklist de composants/patterns ou justification d'impossibilite avec statut non `done`.

A partir de SR 3.6.0, pour une exigence UI/UX significative, un build, un lint, un test unitaire ou un HTTP 200 ne suffisent pas. Si `ui_validation.required` vaut `true`, le contrat doit declarer :

```text
ui_validation.test_readiness.status: pass
ui_validation.visual_evidence.status: pass
ui_validation.visual_evidence.report_file: output/playwright/ui-verification-report.json
```

Si l'authentification, le MFA, les secrets ou des donnees de test empechent l'automatisation, utiliser `blocked` ou `user_testing` avec une checklist E2E concrete, pas `done`.

Si une intention validee est sortie du lot courant, utiliser `moved_to_new_lot` et renseigner le lot cible, l'entree inbox ou la raison de blocage dans la couverture, les notes ou `backlog_mutation`.

Le contrat doit aussi renseigner `propagation` quand un symbole ou contrat partage est modifie. Si `propagation.required` vaut `true`, `status` doit etre `pass` avant `done`, avec preflight, validation humaine si requise, recherches de references, consommateurs verifies et verification proportionnee.

Valider :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Pendant la transition SR 2.x -> 3.0.0, conserver aussi les fichiers legacy requis par le projet. Le lot de migration des anciennes tasks et la mise a jour du prompt 07 sont separes de la creation du schema.

### 9. Mise a jour memoire

Mettre a jour :

- `progress.md` ;
- `verification.md` ;
- `decisions.md` ;
- `SR_LOTS.yaml` ;
- `CURRENT_STATE.md` pour tout upgrade SR, realignement SR, changement de version SR, creation de `NEXT_SESSION_PROMPT.md`, modification structurante de `SR_LOTS.yaml`, lot applicatif significatif passe en `done` ou `user_testing`, ou fin de session significative ;
- RepoMap si structure changee.
- Nexus KG si mode `nexus_kg` et changement structurel ou lot termine.

Si `SR_LOTS.yaml` a ete modifie pendant le lot, valider le backlog avant cloture :

```bash
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
```

Si `SR_PASSES.yaml` a ete modifie ou utilise pour une execution multi-lots, valider la passe avant cloture :

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

Si un `pass_runtime_goal.md` a ete utilise, verifier que le Goal Length Gate a ete documente et que la commande `/goal` ne depasse pas `max_goal_command_chars`. La passe ne doit pas etre marquee `done` si des E2E utilisateur ou une validation humaine restent requis ; utiliser `user_testing` avec checklist E2E concrete.

Cette validation est obligatoire meme si `git diff --check` est vert. `git diff --check` ne valide pas les champs obligatoires du contrat de lot et peut manquer un fichier non suivi.

Si `SR_LOTS.yaml` n'a pas ete modifie apres une tache non triviale, documenter dans `gate_report.md` ou le contrat pourquoi le Backlog Mutation Gate conclut `no_backlog_mutation_required`.

### 10. Continue ou stop

Continuer uniquement si :

- tous les gates critiques sont verts ;
- le Lot Completion Gate confirme que toutes les exigences validees du lot courant sont couvertes ou explicitement sorties avec validation ;
- le Propagation Gate est `pass` si un symbole ou contrat partage a ete modifie ;
- le niveau d'autonomie autorise un lot suivant ;
- le contexte reste sain ;
- aucune validation humaine n'est requise.

Sinon stopper avec :

- ce qui est fait ;
- ce qui reste ;
- raison du stop ;
- prochain lot recommande.

Apres chaque lot, si des tests reels utilisateur sont necessaires, passer le lot en `user_testing` et donner la checklist E2E utilisateur dans la reponse finale.

Le `Loop Contract` doit refuser une simple mention "tests E2E a faire" sans liste d'actions et resultats attendus.

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

## Design gate minimal

Pour une tache UI :

1. Identifier les composants/patterns existants.
2. Eviter les composants locaux one-shot si un wrapper existe.
3. Eviter l'empilement de cartes et sections sans hierarchy.
4. Respecter tokens/theme existants.
5. Produire screenshot Playwright si l'application peut tourner.
6. Documenter toute exception.

## Context budget gate

Declencher un handoff ou `NEXT_SESSION_PROMPT.md` si :

- plus de 2 lots ont ete executes ;
- le rapport `context_budget_report.py` est `orange` ou `red` selon le statut hybride ;
- plus de 20 tours utilisateur ont eu lieu depuis le dernier compact ;
- une nouvelle macro-fonction commence ;
- un upgrade SR ou realignement SR vient d'etre effectue ;
- une decision structurante vient d'etre prise ;
- la session dure depuis plusieurs jours ;
- l'utilisateur signale qu'il s'absente ;
- la prochaine action depend fortement de decisions anterieures.

Si aucun handoff ou `NEXT_SESSION_PROMPT.md` n'est cree apres une tache non triviale, documenter dans `gate_report.md` pourquoi le contexte reste sain.

La cloture doit aussi renseigner `conversation_transition` dans `loop_contract.json` :

- `continue_current` si le contexte est green et la suite courte ;
- `recommend_new_conversation` si le contexte est yellow, si un lot significatif vient de se terminer ou si la prochaine action est longue ;
- `stop_for_new_conversation` si le contexte hybride est orange/red ou si la reprise devient fragile.

Si `conversation_transition` vaut `recommend_new_conversation` ou `stop_for_new_conversation`, renseigner aussi `resume_protocol` :

- `required: true` ;
- `mode: strict_resume` par defaut apres un stop orange/red ;
- `next_user_prompt` avec le texte exact a copier dans la nouvelle conversation ;
- `default_on_plain_resume: strict_resume` ;
- `must_not_code_before_user_validation: true` si le contexte hybride est orange/red.

## Nexus context gate

Si Nexus/RAG est disponible :

- utiliser un context pack court ;
- interroger le KG du repository si disponible ;
- verifier la fraicheur du KG si l'outil existe ;
- citer les sources utiles ;
- ne pas injecter tout l'historique ;
- privilegier decisions, specs, preuves et risques.

## Sortie finale attendue

La reponse finale doit contenir :

- memoire SR utilisee ;
- lot(s) traites ;
- ce qui est fait ;
- resultat observe ;
- lecture expert / produit ;
- fichiers touches ;
- verifications executees ;
- statut des gates, dont self evaluation et context budget ;
- tests E2E utilisateur a faire ;
- mise a jour backlog ;
- risques restants ;
- prochain lot recommande.
