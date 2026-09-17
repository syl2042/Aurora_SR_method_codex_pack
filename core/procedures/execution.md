# execution — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Objectif

Transformer la **SR Development Method** en harness operationnel pour Codex : specs executables, backlog vivant, contexte court, gates de verification, design coherence, handoff et autonomie bornee.

La SR Development Method est la branche de la SR Method dediee au developpement assiste par IA. SR signifie **Specification Runtime**.

SR-Harness ne remplace pas :

- les task memories `docs/codex/tasks/...` ;
- `CURRENT_STATE.md` ;
- les skills methode existantes ;
- les skills metier Codex ;
- les skills runtime applicatives.

Il les orchestre.

## Principe central

Pour toute tache non triviale, Codex doit traiter la demande comme un evenement de backlog avant de coder.

```text
demande utilisateur
→ classer : nouveau lot / lot rouvert / bug / decision / question / execution
→ mettre a jour SR_INBOX ou SR_LOTS si necessaire
→ construire un contexte court
→ si fonction structurante : analyser l'impact global et les lots lies
→ verifier les preuves avant plan avec RepoMap/KG puis code reel
→ executer un lot borne
→ auto-evaluer le resultat
→ produire gate report
→ mettre a jour memoire
```

Quand l'utilisateur valide explicitement un lot, une passe ou un plan, ce perimetre devient contractuel. SR-Harness doit ensuite chercher l'implementation la plus simple pour couvrir tout ce perimetre, sans le reduire silencieusement.

## SR Core

Mode standard sans Nexus KG.

Sources de connaissance :

- `docs/codex/CODEBASE_MAP.md` ;
- `docs/codex/CODEBASE_MAP.generated.md` si besoin ;
- `SR_LOTS.yaml`, `CURRENT_STATE.md` et task memories ;
- lecture ciblee du code reel ;
- tests, logs, screenshots et diff.

Repomix et Gitingest ne font pas partie de la methode standard.

## SR Nexus

Mode avance quand Nexus expose un Knowledge Graph du repository via MCP, SDK ou API.

- toutes les sources SR Core ;
- Nexus KG pour identifier fichiers, routes, composants, services, dependances, tests et zones a risque ;
- context pack Nexus court pour limiter les tokens.

Doctrine non negociable : RepoMap et KG orientent. Le code reel, les tests et les logs restent la source finale.

## Fichiers SR-Harness

```text
docs/codex/SR_INBOX.yaml
docs/codex/SR_LOTS.yaml
docs/codex/SR_PASSES.yaml
docs/codex/SR_CONTEXT_PACK.md
docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
docs/codex/tasks/YYYY-MM-DD_slug/gate_report.md
docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
docs/codex/tasks/YYYY-MM-DD_slug/NEXT_SESSION_PROMPT.md
```

## `SR_INBOX.yaml`

Capture a chaud :

- bug utilisateur ;
- idee ;
- decision ;
- retour test ;
- dette ;
- point design ;
- point a reouvrir.

Il peut contenir du bruit temporaire.

## `SR_LOTS.yaml`

Backlog vivant structure.

Il contient uniquement des lots cadrees ou validables, avec statut, perimetre, criteres d'acceptation, commandes de verification et stop conditions.

Pour les fonctions structurantes, il peut aussi declarer les relations entre lots :

- `depends_on` : lots qui doivent etre termines avant celui-ci ;
- `blocked_by` : lots ou decisions qui bloquent l'execution ;
- `impacts` : lots, surfaces ou contrats que ce lot modifie potentiellement ;
- `impacted_by` : origine d'une modification ou d'une reouverture ;
- `supersedes` / `superseded_by` : remplacement explicite d'un lot ou d'une approche ;
- `global_impact` : trace courte de l'analyse d'impact transverse quand elle est requise.

## `SR_CONTEXT_PACK.md`

Contexte court pour la session ou le lot courant.

Il doit reduire les tokens en evitant de relire toutes les specs, tasks et fichiers.

## Nommage des lots

Convention recommandee pour les nouveaux lots :

```text
<PROJECT_KEY>-<AREA>-<SEQ>
```

Exemples :

- `NP-DESIGN-001`
- `CIA-REV360-001`
- `NX-METAKG-001`

`PROJECT_KEY` vient de `docs/codex/PROJECT_PROFILE.yaml`.
`AREA` est une famille stable du projet.
`SEQ` est numerique, recommande sur 3 chiffres.

Les dates doivent rester dans `created_at`, `updated_at` et le nom du dossier de task memory. Ne pas renommer brutalement les lots existants : utiliser `legacy_lot_id` ou `aliases` pendant une migration.

## Statuts de lot

```text
proposed      idee ou retour a cadrer
planned       lot structure mais non valide
validated     lot valide par l'humain ou par regle projet
in_progress   lot en cours
done          toutes les exigences implementees et preuves suffisantes
user_testing  attente test reel utilisateur
repair        au moins une exigence est absente, partielle, defectueuse ou en echec
reopened      lot rouvert apres bug, oubli ou regression
blocked       attente decision, acces, source, spec ou architecture
deferred      reporte volontairement
superseded    remplace par une decision ou un autre lot
```

`done` exige que toutes les exigences soient implementees et suffisamment prouvees. `user_testing` est reserve a une implementation technique complete dont il manque seulement un E2E, une preuve visuelle reelle ou une acceptation humaine. Une verification unitaire, build ou runtime requise mais manquante reste `repair`. Une UI absente ou partielle reste `repair`, meme si le build et les tests unitaires sont verts.

## Niveau 0 - Assistance ponctuelle

Question, lecture, micro-fix.

SR_LOTS peut etre ignore si la tache est simple et sans modification durable.

## Niveau 1 - Lot unique

Codex execute un seul lot valide, puis stoppe.

## Niveau 3 - PR autonome bornee

Codex prepare un ensemble coherent de lots dans une branche ou PR, avec verification complete.

Validation humaine obligatoire.

## Niveau 4 - Autonomie continue

Non recommande par defaut.

## Scope gate

Le diff doit rester dans `allowed_paths` et hors `forbidden_paths` du lot.

## Spec gate

Les criteres d'acceptation doivent etre couverts ou explicitement marques incomplets.

Le Spec gate ne remplace pas le Lot Completion Gate : il verifie les criteres, tandis que le Lot Completion Gate verifie toutes les exigences validees, y compris produit, UI/UX, E2E, documentation, i18n, rebuild ou integrations.

## Nexus context gate

Si le projet utilise Nexus/RAG ou Nexus KG :

- identifier les sources documentaires utiles ;
- identifier les noeuds/fichiers KG utiles si disponibles ;
- ne pas injecter tout le corpus ;
- produire un context pack court ;
- separer decisions, specs, preuves, code et risques.

Quand un outil MCP/SDK Nexus existe, la mise a jour KG doit etre deterministe autant que possible : fichiers modifies, diff, routes, imports, composants, services et tests. Le LLM ne doit pas etre necessaire pour parser la structure.

## Comportement implicite attendu

L'utilisateur ne doit pas avoir a dire "mets a jour SR_LOTS".

Quand une demande modifie le plan, Codex doit proposer ou appliquer selon risque :

- ajouter une entree `SR_INBOX` ;
- rouvrir un lot ;
- creer un lot `proposed` ;
- marquer un lot `user_testing`, `done`, `blocked`, `deferred` ou `superseded`.

Pour les changements significatifs, Codex montre le delta et attend validation avant codage.

## Visibilite utilisateur obligatoire

Pour une tache non triviale, Codex doit rendre la methode visible sans verbiage long :

- debut : `Memoire SR : ...`, objectif verifiable, sources SR lues, skills selectionnees ;
- pendant : signaler les gates rouges ou decisions qui changent le lot ;
- fin : lots traites, gates, fichiers SR mis a jour, tests E2E utilisateur, prochain lot recommande.

## Relation avec les task memories

`SR_LOTS.yaml` est le backlog.

`docs/codex/tasks/...` est le journal d'execution.

Un lot peut avoir plusieurs task memories si plusieurs sessions ou reprises sont necessaires.

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

## 1. Selection

Choisir le prochain lot executable :

- statut `repair`, `reopened` ou `validated` ;
- dependances terminees ;
- non bloque ;
- risque compatible avec le niveau d'autonomie.

Priorite recommandee :

```text
repair/reopened > validated > planned/proposed a cadrer
```

Ne pas coder un lot `proposed` sans validation si le changement est significatif.

Si plusieurs lots sont executables et que l'utilisateur a valide une phase autonome, une roadmap ou un gros brief, preparer une passe jusqu'a `max_lots_per_session` en commencant par les lots `repair`/`reopened`, puis `validated`.

Quand `docs/codex/SR_PASSES.yaml` existe, choisir une passe `validated` ou proposer une passe `planned` avant de coder. Une passe ne remplace pas les lots : elle declare seulement l'ordre, le preflight commun, les validations humaines et l'E2E groupe.

## 2. Intake

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

## 4. Plan court

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

## 4b. Validated Lot Execution Contract

Une validation utilisateur d'un lot ou d'une passe engage tout le perimetre decrit juste avant validation.

Hierarchie d'arbitrage :

1. securite, secrets, actions externes et validations humaines ;
2. perimetre valide utilisateur ;
3. contrat de lot ou de passe SR ;
4. criteres d'acceptation ;
5. simplicite, changements chirurgicaux et absence de refactor hors besoin ;
6. style local.

La simplicite s'applique donc a l'implementation de chaque exigence validee, jamais a la suppression silencieuse d'une exigence.

Avant codage significatif, extraire les exigences validees dans `validated_requests`. Ne jamais condenser une passe multi-lots en une exigence globale. Creer des identifiants stables pour chaque lot, critere produit important, demande UI/UX explicite, exclusion et validation humaine/E2E attendue. Pour chaque exigence, indiquer la preuve minimale prevue : fichier, test, log, endpoint, capture, build, E2E ou justification.

Si le lot contient une exigence UI/UX explicite, prevoir une verification visuelle ou E2E ciblee. Un build, lint ou smoke HTTP ne suffit pas pour declarer une UI alignee sur une reference produit.

## 5. Implementation

Modifier uniquement les fichiers necessaires.

Respecter :

- `allowed_paths` ;
- `forbidden_paths` ;
- interdictions metier ;
- design gate si UI ;
- architecture gate si DB/RAG/service/runtime agent.

Si le Propagation Gate est requis, propager explicitement les appels, imports/exports, signatures, schemas et tests consommateurs identifies. Si une propagation complete n'est pas souhaitable, ajouter une compatibilite temporaire seulement avec justification, expiration ou lot de retrait.

## 8. Gate report

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

## 10. Continue ou stop

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

## SR Bootstrap obligatoire

- Au debut de chaque nouvelle conversation, apres compact, apres resume ou apres handoff, relire `docs/codex/SR_BOOTSTRAP.md` avant toute tache non triviale.
- Pour une tache non triviale, annoncer l'objectif verifiable, les hypotheses, l'approche simple suffisante, les skills selectionnees et la verification prevue avant de coder.
- Si le contexte precedent semble connu, verifier quand meme `docs/CURRENT_STATE.md` et la derniere memoire de tache pertinente.
- Au demarrage ou apres compact/resume, chercher le dernier `NEXT_SESSION_PROMPT.md` avec `python3 scripts/codex/find_next_session_prompt.py --root . --json` si disponible, puis le lire s'il existe.
- Si l'utilisateur dit seulement `reprends`, `resume`, `continue` ou une formule vague equivalente apres une nouvelle conversation, appliquer `Reprise SR stricte` : lire uniquement le dernier `NEXT_SESSION_PROMPT.md`, le `sr_contract.json` et le `loop_contract.json` associes si indiques, resumer, ne pas coder, ne pas lancer le lot suivant, attendre validation.
- Annoncer systematiquement le statut de memoire sous la forme : `Memoire SR : existante / absente a creer / non creee car simple question`.
- Avant toute reponse non triviale qui affirme un fait verifiable sur l'existant, appliquer le Fact Gate : si une source locale ou officielle peut trancher, la lire avant de conclure ; sinon marquer explicitement l'element comme hypothese non verifiee et indiquer la verification minimale.
- Avant toute reponse de cloture ou d'avancement significatif, executer `python3 scripts/codex/context_budget_report.py --root . --compact` si disponible. Si le statut est `green`, ne pas l'afficher ; sinon appliquer le Context budget gate.
- En fin de tache non triviale, indiquer la memoire SR utilisee, les fichiers SR mis a jour, les gates, les tests E2E utilisateur a faire et le prochain lot recommande.
- En fin de tache non triviale, indiquer `NEXT_SESSION_PROMPT.md : cree / mis a jour / non requis` avec la raison.
- SR plein regime : mettre a jour `docs/CURRENT_STATE.md` apres tout upgrade SR, realignement SR, changement de version SR, creation de `NEXT_SESSION_PROMPT.md`, modification structurante de `SR_LOTS.yaml`, lot applicatif significatif passe en `done` ou `user_testing`, ou fin de session significative.
- SR Contract 3.1.0 : creer ou mettre a jour `docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json` quand `PROJECT_PROFILE.yaml` declare `require_sr_contract`, suivre chaque intention granulaire dans `validated_requests`, separer `implementation_status` et `evidence_status`, puis verifier avec `python3 scripts/codex/validate_sr_contract.py --file <chemin>`. Les contrats 3.0.0 restent lisibles.
- Loop Contract obligatoire pour toute tache non triviale : creer ou mettre a jour `docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json`, declarer `conversation_transition`, puis verifier avec `python3 scripts/codex/validate_loop_contract.py --file <chemin>`.
- Lot Completion Gate obligatoire : produire une table derivee des exigences validees avec implementation, preuve et reste a faire. `simple/chirurgical` ne reduit jamais le perimetre valide. Une implementation partielle, absente ou defectueuse impose `repair`; `user_testing` est reserve au code techniquement complet dont seule une preuve E2E ou acceptation manque.
- Reprise consolidee obligatoire : un retour sur une exigence validee est par defaut `existing_requirement_repair`; rouvrir le lot d'origine, heriter de toutes ses exigences ouvertes et ne creer un nouveau lot que pour un scope reellement nouveau avec justification explicite.
- UI Test Readiness Gate et UI Visual Evidence Gate obligatoires pour UI/UX significative quand `ui_validation.required` vaut `true` : lancer `node scripts/codex/sr_ui_verify.mjs` sur les routes/viewports requis, renseigner `sr_contract.json.ui_validation`, et ne jamais accepter une capture de login comme preuve UI.
- Propagation Gate obligatoire : si un changement touche un symbole ou contrat partage (fonction, signature, type, schema, endpoint, champ DB, config, import/export, composant, agent runtime), annoncer avant mutation les consommateurs et surfaces a risque, demander validation humaine si le risque depasse le local, puis verifier apres mutation les references, appels, imports/exports, signatures, tests et smokes proportionnes. Un lot ne peut pas etre `done` si le gate requis n'est pas `pass`.
- Backlog Contract obligatoire : si `docs/codex/SR_LOTS.yaml` est modifie, executer `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` avant cloture. `git diff --check` ne remplace jamais cette validation.
- Backlog Mutation Gate obligatoire : si une demande, une decouverte ou une reparation introduit une fonction structurante ou un impact durable, ne pas la traiter comme un simple detail du lot courant. Classer l'evenement, analyser les implications globales, puis mettre a jour `SR_INBOX.yaml` ou `SR_LOTS.yaml`, ou documenter explicitement pourquoi aucune mutation de backlog n'est requise.
- Global Impact Gate obligatoire : avant de cadrer ou coder une fonction structurante, analyser son impact sur le produit global, les parcours, donnees, permissions, API/services, UI, tests, lots existants, dependances, migrations et risques. Cette analyse doit rester agnostique du domaine et s'appliquer a toute fonction transversale.
- Cloture standard de lot : `Ce qui est fait`, `Resultat observe`, `Lecture expert / produit`, `Verifications executees`, `Memoire SR`, `Tests E2E utilisateur`, `Prochaine etape`.

## Mission

- Repo Auroramind. Codex travaille comme agent de developpement encadre.
- Ne pas coder si le besoin, les risques ou les sources de verite ne sont pas clairs.

## SR-Harness lots

Pour toute demande qui modifie le backlog, lire `docs/codex/SR_HARNESS_METHOD.md`, `docs/codex/LOT_EXECUTION_METHOD.md`, `docs/codex/SR_LOTS.yaml` et `docs/codex/SR_INBOX.yaml`.

Pour toute execution multi-lots, lire ou proposer `docs/codex/SR_PASSES.yaml` avant codage significatif. Une passe doit declarer les lots inclus, l'ordre, les prerequis, validations humaines, secrets/actions externes, migrations, criteres d'arret et tests E2E groupes.

Politique par defaut :
- traiter les lots `repair`/`reopened` puis `validated` ;
- enchainer jusqu'a 3 lots par passe si les gates restent verts ;
- appliquer le Pass Planning Gate avant de coder une passe ;
- valider `SR_PASSES.yaml` avec `validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` si le fichier existe ou vient d'etre cree ;
- Pass Runtime Goal : si `sr_passes.pass_runtime_goal.enabled` est actif et qu'une passe `validated`/`in_progress` est executee avec `/goal`, generer `pass_runtime_goal.md` avec `build_pass_runtime_goal.py`, appliquer le Goal Length Gate (`max_goal_command_chars: 1000`, `hard_limit: 4000`) et ne pas enchainer la passe suivante sans validation utilisateur ;
- stopper sur gate rouge, migration ambigue, dependance, regle metier absente, action sensible, test bloquant ou contexte a risque ;
- mettre a jour `SR_LOTS.yaml` apres chaque decision de statut ;
- valider `SR_LOTS.yaml` avec `validate_lot_contract.py` apres toute modification du backlog ;
- passer en `user_testing` si un test reel utilisateur est necessaire.
- quand une nouvelle fonction structurante apparait, appliquer `Global Impact Gate` puis `Lot Dependency Reconciliation` avant codage significatif ;
- classer les lots existants pertinents comme `unaffected`, `impacted`, `blocked_by`, `reopened`, `superseded`, `split_required` ou `depends_on` ;
- consigner le resultat dans `backlog_mutation_gate`, `global_impact_gate`, `SR_INBOX.yaml`, `SR_LOTS.yaml` ou le gate report.

Propagation Gate obligatoire :
- avant mutation, si un symbole ou contrat partage change, declarer le changement, les consommateurs detectes, les surfaces a risque, le niveau `low/medium/high/critical`, la strategie de propagation et les verifications prevues ;
- stopper avant mutation si validation humaine requise non recue : risque `high/critical`, ou `medium` quand la validation humaine stricte est active ;
- apres mutation, rechercher les anciennes et nouvelles references, verifier les imports/exports, signatures, schemas, tests consommateurs et smokes proportionnes ;
- documenter les references restantes comme `ignored_references` avec justification, sinon rester en `repair` ou `blocked` ;
- ne jamais clore `done` avec `propagation_gate.required=true` et `status` different de `pass`.

Evidence gate obligatoire avant recommandation :
- suivre la chaine `RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs` ;
- citer les fichiers ou sources lus ;
- distinguer `verifie`, `hypotheses restantes` et `questions bloquantes` ;
- si une verification locale est possible, la faire avant de repondre.

Lot Design Evidence Gate obligatoire avant lot executable :
- un lot peut etre `proposed` avec hypotheses et fichiers candidats ;
- un lot `planned`, `validated`, `in_progress`, `repair` ou `reopened` doit declarer `design_evidence.status: pass` ou `not_applicable` justifie ;
- si `code_read_required: true`, le lot doit lister `confirmed_files_read` ;
- sans preuve suffisante, garder le lot en `proposed` et ne pas le mettre dans une passe executable.

Fact Gate obligatoire avant conclusion factuelle :
- classer la reponse attendue : `opinion/methode`, `fait_verifiable` ou `hypothese_non_verifiee` ;
- pour tout `fait_verifiable` sur un repo, produit, API, migration, flux UI, donnee, configuration ou comportement existant, lire la source disponible avant de repondre ;
- si la source est accessible mais non lue, ne pas conclure et annoncer `Fact Gate non satisfait` avec la source a verifier ;
- si la verification est impossible ou disproportionnee, repondre uniquement sous forme d'hypothese non verifiee avec la verification minimale ;
- les formulations de probabilite ne remplacent jamais une preuve quand les sources peuvent trancher.

Context budget gate obligatoire :
- executer `python3 scripts/codex/context_budget_report.py --root . --compact` si disponible avant chaque reponse de cloture ou d'avancement significatif ;
- si le statut est `green`, ne rien dire a l'utilisateur sauf besoin de verification explicite ;
- si le statut est `yellow`, signaler sobrement qu'une reprise sera recommandee si la prochaine tache est longue ;
- si le statut est `orange`, `red`, `stale`, `ambiguous` ou `unknown`, creer ou mettre a jour le `NEXT_SESSION_PROMPT.md` du lot courant et donner un prompt court avec son chemin explicite ;
- apres 2 lots, 20 tours utilisateur, une session longue, un changement de macro-fonction ou un risque de perte de contexte, creer ou mettre a jour `NEXT_SESSION_PROMPT.md` ;
- en cloture, declarer dans `loop_contract.json` la decision `conversation_transition` : `continue_current`, `recommend_new_conversation` ou `stop_for_new_conversation` ;
- recommander un handoff si la prochaine action depend fortement de decisions anterieures.

Self Evaluation Gate obligatoire :
- apres patch, relire le diff et les fichiers critiques modifies ;
- verifier l'objectif initial, les preuves, les risques restants et ce qui aurait pu etre oublie ;
- decider explicitement `done`, `user_testing`, `repair` ou `blocked`.

Lot Completion Gate obligatoire :
- relire le perimetre valide juste avant validation utilisateur ;
- couvrir chaque exigence dans `validated_requests` et dans la table de couverture ;
- fournir une preuve par exigence : fichier, test, log, endpoint, capture, build, E2E ou justification ;
- si une exigence UI/UX est explicite, fournir une preuve visuelle ou E2E ciblee ; une implementation complete sans preuve reste `user_testing`, une implementation absente/partielle/defectueuse reste `repair` ;
- ne jamais presenter un sous-ensemble comme lot complet.

Loop Contract obligatoire :
- pour toute tache non triviale, creer ou mettre a jour `loop_contract.json` dans la memoire de tache ;
- si `status_decision: user_testing`, fournir une vraie liste `e2e_user_tests.items`, pas une simple mention d'attente E2E ;
- si du code applicatif change, declarer `changed_files` et les verifications executees ou la raison de non-execution ;
- si un symbole ou contrat partage change, declarer `propagation_gate` et les preuves de propagation ;
- declarer `conversation_transition` pour dire clairement si la prochaine action peut rester dans la conversation courante ou doit partir dans une nouvelle conversation ;
- declarer `resume_protocol` si une nouvelle conversation est recommandee ou imposee, avec le prompt exact a donner a l'utilisateur ;
- valider avec `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json`.

## Agents IA runtime

Avant de creer ou modifier un agent IA applicatif, lire `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
Pattern obligatoire : action produit bornee + representation interne stable + contrat runtime type + prompt contract + message builder + bindings SQL/Nexus controles + skills runtime + tools/actions + routing/fallback + output JSON schema + validation + traces + validation humaine si action critique.
Ne jamais laisser un LLM generer puis executer librement du SQL.

## RepoMap

Lire `docs/codex/CODEBASE_MAP.md` avant tache multi-fichiers ou reprise. Consulter le generated seulement si besoin.
Si Nexus KG est active dans `PROJECT_PROFILE.yaml`, consulter le KG avant de choisir les fichiers candidats et indiquer si le KG doit etre mis a jour en cloture.

## Objectif

Garantir que Codex reprend systematiquement la methode SR apres nouvelle conversation, compact, resume, handoff ou changement de contexte.

## Declenchement obligatoire

Executer ce bootstrap mentalement et explicitement avant toute tache non triviale :
- debut de conversation dans un repo installe ;
- reprise apres compact ;
- reprise apres `resume` ou handoff ;
- demande multi-fichiers, metier, architecture, securite, agents IA, DB ou integration ;
- doute sur l'etat courant du projet.

## Rituel minimal avant action

Pour toute tache non triviale, Codex doit annoncer :
- objectif verifiable ;
- hypotheses retenues ;
- approche simple suffisante pour couvrir tout le perimetre valide, sans reduction silencieuse ;
- skills methode selectionnees ;
- skills metier Codex selectionnees ou raison de leur absence ;
- digest skills consulte ou raison de non-consultation ;
- mode connaissance detecte (`core` ou `nexus_kg`) ;
- methode de verification prevue.

## Exceptions

Pour une question simple ou une commande ponctuelle sans modification, la memoire de tache peut etre omise. Si la demande devient multi-etapes, revenir au bootstrap complet.

## Workflow standard

Bootstrap SR, comprendre, reformuler, identifier hypotheses, consulter `SKILL_DIGEST.md`, selectionner skills methode et metier, lire uniquement les `SKILL.md` selectionnes, lire sources, creer task memory, planifier, attendre validation si risque, implementer petite tranche, verifier, reviewer diff, cloturer.

Avant une reponse non triviale, appliquer le Fact Gate : classer les elements de reponse en `opinion/methode`, `fait_verifiable` ou `hypothese_non_verifiee`. Tout fait verifiable doit etre prouve par une source locale ou officielle accessible avant conclusion, sinon rester explicitement au statut d'hypothese.

Si le mode validation humaine stricte est actif dans `AGENTS.md`, un lot, une reprise ou la demande utilisateur, Codex peut analyser sans validation mais ne modifie aucun fichier et ne lance aucune action de mutation tant que l'utilisateur n'a pas ecrit exactement `je valide`. La validation ne couvre que le perimetre decrit juste avant.

## Agents IA runtime

Si la tache touche LLM, agent IA applicatif, prompt, outil, orchestration, structured output, RAG/Nexus ou skill runtime :
- lire `AI_AGENT_RUNTIME_METHOD.md` ;
- utiliser le pattern action produit bornee + representation interne stable + contrat runtime type + prompt contract + message builder + bindings controles + tools/actions + routing/fallback + JSON schema + validation + traces ;
- exiger validation humaine pour les actions critiques.

## SR Development Method et lots

Si la tache concerne une roadmap, un gros brief, une reprise longue, plusieurs lots ou une phase autonome bornee :
- lire `SR_HARNESS_METHOD.md` et `LOT_EXECUTION_METHOD.md` ;
- utiliser `aurora-lot-runner` ;
- maintenir `SR_INBOX.yaml` et `SR_LOTS.yaml` ;
- verifier ou proposer `SR_PASSES.yaml` avant toute execution multi-lots ;
- appliquer le Pass Planning Gate : ordre, dependances, preflight, validations humaines et E2E groupe ;
- generer `pass_runtime_goal.md` avec `build_pass_runtime_goal.py` pour une passe validee executee avec `/goal`, puis appliquer le Goal Length Gate (`max_goal_command_chars: 1000`, `hard_limit: 4000`) ;
- appliquer knowledge_gate puis evidence_gate avant plan/faisabilite ;
- appliquer fact_gate avant toute conclusion factuelle sur l'existant ;
- produire `gate_report.md` apres execution d'un lot ;
- produire et valider `loop_contract.json` pour toute tache non triviale ;
- appliquer le Self Evaluation Gate apres patch et avant cloture ;
- verifier `context_budget_report.py` avant d'enchainer un lot long si le script existe ;
- stopper si un gate critique est rouge ou si une validation humaine est requise.

## Stop conditions

S'arreter si regle metier absente, skill metier manquante, architecture, dependance, migration, securite, secret, connecteur externe, agent runtime non valide, SQL libre LLM, plan invalide, hors-perimetre, gate SR-Harness rouge ou contexte trop long sans handoff.

## Fin de tache SR obligatoire

- Resume.
- Fichiers modifies.
- Verifications executees.
- Loop Contract valide ou raison de non-applicabilite.
- Risques restants.
- Decisions prises.
- Prochaine etape.
- CURRENT_STATE.md a mettre a jour ?
- RepoMap/KG a mettre a jour ?

## CURRENT_STATE.md

Mettre a jour apres tranche significative, architecture, route majeure, agent runtime, integration, bug bloquant.

En mode SR plein regime, `CURRENT_STATE.md` est obligatoire apres tout upgrade SR, realignement SR, changement de version SR, creation de `NEXT_SESSION_PROMPT.md`, modification structurante de `SR_LOTS.yaml`, lot applicatif significatif passe en `done` ou `user_testing`, ou fin de session significative. Pas obligatoire pour micro-corrections sans impact de reprise.

## Regle distribuee par ancien installateur

- Ne pas proposer une recommandation technique ou un plan engageant sans avoir lu les fichiers verifiables quand ils peuvent trancher.

## Regle distribuee par ancien installateur

- Avant de creer ou modifier un agent IA applicatif, lire `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.

## Regle distribuee par ancien installateur

- Reprise consolidee : un retour sur une exigence validee rouvre par defaut le lot d'origine ; ne creer un nouveau lot que pour un scope reellement nouveau avec justification explicite.

## Regle distribuee par ancien installateur

- Pour les lots SR-Harness, lire `docs/codex/SR_HARNESS_METHOD.md`, `docs/codex/LOT_EXECUTION_METHOD.md`, `docs/codex/SR_LOTS.yaml` et `docs/codex/SR_INBOX.yaml`.
