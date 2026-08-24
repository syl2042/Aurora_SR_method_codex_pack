# SR_HARNESS_METHOD.md

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

## Modes de connaissance codebase

SR 2.3 distingue deux modes.

### SR Core

Mode standard sans Nexus KG.

Sources de connaissance :

- `docs/codex/CODEBASE_MAP.md` ;
- `docs/codex/CODEBASE_MAP.generated.md` si besoin ;
- `SR_LOTS.yaml`, `CURRENT_STATE.md` et task memories ;
- lecture ciblee du code reel ;
- tests, logs, screenshots et diff.

Repomix et Gitingest ne font pas partie de la methode standard.

### SR Nexus

Mode avance quand Nexus expose un Knowledge Graph du repository via MCP, SDK ou API.

Sources de connaissance :

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

### `SR_INBOX.yaml`

Capture a chaud :

- bug utilisateur ;
- idee ;
- decision ;
- retour test ;
- dette ;
- point design ;
- point a reouvrir.

Il peut contenir du bruit temporaire.

### `SR_LOTS.yaml`

Backlog vivant structure.

Il contient uniquement des lots cadrees ou validables, avec statut, perimetre, criteres d'acceptation, commandes de verification et stop conditions.

Pour les fonctions structurantes, il peut aussi declarer les relations entre lots :

- `depends_on` : lots qui doivent etre termines avant celui-ci ;
- `blocked_by` : lots ou decisions qui bloquent l'execution ;
- `impacts` : lots, surfaces ou contrats que ce lot modifie potentiellement ;
- `impacted_by` : origine d'une modification ou d'une reouverture ;
- `supersedes` / `superseded_by` : remplacement explicite d'un lot ou d'une approche ;
- `global_impact` : trace courte de l'analyse d'impact transverse quand elle est requise.

### `SR_CONTEXT_PACK.md`

Contexte court pour la session ou le lot courant.

Il doit reduire les tokens en evitant de relire toutes les specs, tasks et fichiers.

### `SR_PASSES.yaml`

Orchestration optionnelle des lots en passes.

Une passe ne remplace pas un lot. Le lot reste l'unite atomique de scope, criteres d'acceptation, chemins autorises, stop conditions et statut. La passe est une unite d'acceleration bornee qui regroupe plusieurs lots quand ils partagent un socle, un preflight ou un E2E coherent.

Une passe doit declarer :

- `pass_id`, titre, statut et priorite ;
- lots inclus et ordre d'execution ;
- rationale de sequencing ;
- preflight commun : validations humaines, secrets, actions externes, migrations, questions ouvertes ;
- sources partagees ;
- strategie E2E : par lot, groupee en fin de passe ou non requise ;
- gates et conditions d'arret.

Migration douce : un projet existant sans `SR_PASSES.yaml` reste valide. Lors d'une installation ou d'un upgrade, Codex ajoute d'abord un registre `passes: []`, que le validateur accepte explicitement. Il ne deduit aucune passe des anciens lots. Le prompt `08` peut ensuite proposer des passes `planned` ou `proposed` seulement apres lecture de `SR_LOTS.yaml` et validation humaine, sans convertir automatiquement l'historique ni modifier les statuts de lots sans preuve.

Note de migration : le validateur de passes reconnait les dependances inter-passes ordonnees. Une passe `proposed` ou `planned` peut declarer une dependance vers un lot place dans une passe strictement anterieure. Une passe `validated`, `in_progress`, `repair` ou `reopened` reste executable seulement si ses dependances anterieures sont reellement satisfaites (`done` ou `user_testing`). Les dependances vers une passe posterieure, les dependances hors de toute passe non terminees et les lots presents dans plusieurs passes restent des erreurs.

Exemple valide de planification avant execution :

```yaml
passes:
  - pass_id: MIA-PASS-001
    status: proposed
    lots: [LOT-A]
  - pass_id: MIA-PASS-002
    status: proposed
    lots: [LOT-B]
```

avec `LOT-B.depends_on: [LOT-A]` dans `SR_LOTS.yaml`.

### Pass Runtime Goal

Le Pass Runtime Goal est une couche d'execution optionnelle pour Codex CLI `/goal`.

Il ne remplace jamais `SR_PASSES.yaml`, `SR_LOTS.yaml` ni les `sr_contract.json`. Il est genere depuis une passe SR et sert uniquement a maintenir Codex en execution jusqu'au statut final correct de la passe.

Politique :

- `SR_PASSES.yaml`, `SR_LOTS.yaml` et les contrats de lots restent la source de verite ;
- `pass_runtime_goal.md` est un artefact derive et peut etre regenere ;
- une commande `/goal` doit rester courte et pointer vers `pass_runtime_goal.md` ;
- `max_goal_command_chars` vaut `1000` par defaut ;
- `hard_limit` vaut `4000` et ne doit jamais etre depasse ;
- si la commande depasse `max_goal_command_chars`, Codex doit la regenerer en forme plus courte ;
- si elle depasse encore `max_goal_command_chars` ou `hard_limit`, le Goal Length Gate est rouge et le goal ne doit pas etre lance ;
- une passe `proposed` ne doit jamais etre executee par goal ;
- une passe `planned` peut servir a un dry-run de generation, mais pas a une execution sans validation utilisateur ;
- une passe `validated`, `in_progress`, `repair` ou `reopened` peut recevoir un goal d'execution ;
- le goal s'arrete a la fin de la passe et propose la suivante sans l'enchainer silencieusement.

Generation recommandee :

```bash
python3 scripts/codex/build_pass_runtime_goal.py --pass-id <PASS_ID> --output docs/codex/tasks/YYYY-MM-DD_<pass-id>/pass_runtime_goal.md
```

La commande `/goal` produite doit etre copiee telle quelle depuis la sortie du script. Pour preparer une passe `planned` sans l'executer, utiliser `--allow-planned` et conserver le statut `planned` tant que l'utilisateur n'a pas valide.

### Goal Length Gate

Avant de lancer `/goal`, Codex doit verifier :

```text
Goal Length Gate:
- pass_runtime_goal.md genere : oui/non
- max_goal_command_chars: 1000
- hard_limit: 4000
- goal_command_chars: ...
- decision: pass / fail
```

Si `decision = fail`, stopper avant execution et corriger le fichier ou le chemin de sortie. Le depassement du seuil n'est pas une alerte cosmetique : il bloque le lancement du goal.

### Nommage des lots

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

## Niveaux d'autonomie

### Niveau 0 - Assistance ponctuelle

Question, lecture, micro-fix.

SR_LOTS peut etre ignore si la tache est simple et sans modification durable.

### Niveau 1 - Lot unique

Codex execute un seul lot valide, puis stoppe.

### Niveau 2 - Multi-lot borne

Codex peut enchainer plusieurs lots si tous les gates restent verts.

Ce niveau est le comportement attendu quand l'utilisateur valide une roadmap, un gros brief ou une phase autonome bornee. L'utilisateur ne doit pas avoir a repeter "fais les 3 prochains lots" si `SR_LOTS.yaml` contient deja des lots `validated` ou `reopened`.

Politique recommandee :

```yaml
max_lots_per_session: 3
max_repair_attempts_per_lot: 2
stop_on_gate_failure: true
```

### Niveau 3 - PR autonome bornee

Codex prepare un ensemble coherent de lots dans une branche ou PR, avec verification complete.

Validation humaine obligatoire.

### Niveau 4 - Autonomie continue

Non recommande par defaut.

## Gates obligatoires

### Lot Completion Gate

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

### UI Test Readiness Gate

Le UI Test Readiness Gate precede l'execution Playwright complete.

But : repondre a la question suivante avant de produire des preuves visuelles :

```text
Sommes-nous reellement capables de tester l'interface demandee ?
```

Statuts autorises :

```text
pass, fail, blocked, not_applicable
```

Le gate verifie au minimum :

- application joignable et `base_url` resolue ;
- routes demandees connues pour le lot ;
- mode auth projet : `none`, `storage_state`, `setup_command` ou `manual` ;
- presence et validite pratique du `storageState` quand requis ;
- detection de redirection login ;
- donnees de test ou preflight humain explicitement bloques si necessaire.

Cas rouge obligatoire : si la route attendue redirige vers `/login`, `/signin`, `/auth`, `/oauth/`, `/oidc/`, `/if/flow/` ou un pattern configure, `login_redirect_detected = true`. Codex ne doit jamais utiliser le screenshot de cette page comme preuve UI valide de la route demandee.

### UI Visual Evidence Gate

Le UI Visual Evidence Gate suit l'execution du runner.

But : repondre a la question suivante :

```text
L'interface reellement demandee a-t-elle ete observee et verifiee avec suffisamment de preuves ?
```

Statuts autorises :

```text
pass, repair, blocked, not_applicable
```

Le gate consomme le rapport `output/playwright/ui-verification-report.json` ou le chemin configure et verifie :

- routes effectivement testees ;
- matrice viewports attendue ;
- screenshots produits ;
- `console.error` ;
- `pageerror` ;
- `requestfailed` ;
- overflow horizontal inattendu ;
- redirection login inattendue.

Par defaut, un lot UI non trivial teste les routes concernees sur quatre viewports :

```yaml
- name: desktop-xl
  width: 1440
  height: 900
- name: desktop
  width: 1280
  height: 800
- name: tablet
  width: 768
  height: 1024
- name: mobile
  width: 390
  height: 844
```

Ces viewports restent surchargeables par projet. Pour API-only, CLI, backend, worker ou migration, les gates UI doivent etre `not_applicable` avec justification.

### Evidence gate

Avant un plan, une faisabilite, une architecture ou un bugfix, Codex doit verifier les sources necessaires :

- RepoMap ;
- Nexus KG si le mode `nexus_kg` est actif ;
- fichiers candidats ;
- routes/API/schemas ;
- specs pertinentes ;
- logs si bug.

Ordre attendu :

```text
RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs
```

La reponse doit distinguer :

```text
Verifie
Hypotheses restantes
Questions bloquantes
```

Si la question porte sur l'existence d'un menu, endpoint, composant, schema, route, modele, migration, configuration ou comportement deja codable, Codex doit lire le code ou les fichiers de reference avant de recommander. Repondre au conditionnel sans verification locale est un gate rouge si les sources sont accessibles.

### Fact gate

Le Fact Gate s'applique a toute reponse non triviale, meme hors patch et hors lot.

But : empecher une conclusion factuelle non prouvee quand les sources peuvent trancher.

Classification :

- `opinion/methode` : conseil general, preference ou explication methodologique ;
- `fait_verifiable` : fait sur un repo, produit, code, API, migration, flux UI, donnee, configuration, etat projet ou comportement existant ;
- `hypothese_non_verifiee` : piste utile non encore prouvee.

Regles :

- un `fait_verifiable` doit etre appuye par une source locale ou officielle lue avant la reponse ;
- si la source est accessible mais non lue, le gate est rouge et Codex doit repondre `Fact Gate non satisfait` avec la source a verifier ;
- si la verification n'est pas possible ou serait disproportionnee, la conclusion reste interdite : Codex peut seulement formuler une hypothese non verifiee avec la verification minimale ;
- les mots de probabilite ne doivent jamais remplacer une preuve disponible.

### Backlog Mutation Gate

Le Backlog Mutation Gate empeche les lots oublies.

Il est obligatoire quand une demande, une decouverte ou une reparation :

- introduit une fonction structurante ou une capacite transversale ;
- change durablement le comportement produit ;
- modifie ou questionne donnees, permissions, navigation, API/services, integrations, agents runtime, tests, migration ou configuration ;
- revele une dette ou un oubli qui depasse le lot courant ;
- cree une dependance nouvelle entre lots ;
- rend un lot existant incomplet, bloque, obsolete ou trop large.

Sorties autorisees :

- ajouter une entree dans `SR_INBOX.yaml` pour capture rapide ;
- creer un lot `proposed` ou `planned` dans `SR_LOTS.yaml` ;
- rouvrir un lot en `reopened` ;
- bloquer un lot via `blocked` ou `blocked_by` ;
- ajouter `depends_on`, `blocked_by`, `impacts`, `impacted_by`, `supersedes` ou `superseded_by` ;
- marquer un lot `deferred` ou `superseded` ;
- documenter `no_backlog_mutation_required` avec justification courte si aucune mutation n'est necessaire.

Avant toute creation de lot, classifier le retour parmi :

```text
existing_requirement_repair
existing_requirement_clarification
existing_requirement_acceptance
new_requirement
scope_change
cancelled_requirement
```

La recherche doit verifier objectifs, criteres d'acceptation, `validated_requests`, lots `user_testing` et passes deja validees. Si une correspondance existe, la decision par defaut est `reopen_or_amend_existing_lot` : rattacher le retour au `requirement_id`, rouvrir le lot d'origine et recharger toutes ses exigences encore ouvertes. `new_requirement` avec nouveau lot exige `new_lot_justification.outside_existing_validated_scope: true`, les lots verifies, une raison et une decision utilisateur. Plusieurs changements du meme perimetre produit et du meme niveau de risque sont repris dans une seule passe coherente ; les gates code, runtime, deploiement ou actions externes restent separes mais rattaches au meme registre.

Pour une tache non triviale, la cloture doit declarer :

```text
Backlog Mutation Gate:
- structural_change_detected: oui/non
- mutation_required: oui/non
- sr_inbox_updated: oui/non
- sr_lots_updated: oui/non
- affected_lots: [...]
- decision: ...
```

Un changement significatif ne doit pas etre code comme extension silencieuse du lot courant. Si le perimetre change, Codex doit enregistrer la decision dans la memoire de tache et proposer ou appliquer le delta backlog selon le niveau de risque.

### Lot Design Evidence Gate

Le Lot Design Evidence Gate empeche qu'un lot pret a executer soit defini sur une supposition non verifiee.

Il est obligatoire avant de creer ou promouvoir un lot en `planned`, `validated`, `in_progress`, `repair` ou `reopened`.

Un lot peut rester `proposed` sans preuve complete s'il sert a capturer une intention, une piste exploratoire ou une question a investiguer. Dans ce cas, il doit garder ses hypotheses et ne doit pas etre mis dans une passe executable.

Sortie attendue dans `SR_LOTS.yaml` :

```text
design_evidence:
- status: pending / pass / fail / not_applicable
- code_read_required: oui/non
- candidate_files: [...]
- confirmed_files_read: [...]
- symbols_or_routes_checked: [...]
- tests_or_logs_checked: [...]
- assumptions_remaining: [...]
- open_questions: [...]
- not_applicable_reason: ...
- status_ceiling_if_not_pass: proposed
```

Regles :

- `planned`, `validated`, `in_progress`, `repair` et `reopened` exigent `design_evidence.status: pass` ou `not_applicable` avec raison ;
- si `code_read_required: true`, `confirmed_files_read` ne doit pas etre vide ;
- si des fichiers existent et peuvent trancher le cadrage, Codex doit les lire avant de proposer un plan engageant ;
- pour un lot greenfield, Codex doit lire les patterns adjacents quand ils existent ou justifier l'absence de surface code.

### Global Impact Gate

Le Global Impact Gate force le recul produit et technique avant de cadrer ou coder une fonction structurante.

Il est obligatoire pour toute fonction qui peut affecter plusieurs surfaces du projet, meme si l'utilisateur ne demande qu'une partie de la fonction. La methode reste agnostique : les surfaces a verifier dependent du projet reel, pas d'un domaine predefini.

Surfaces minimales a evaluer quand elles existent :

- objectifs produit et parcours utilisateur ;
- roles, droits, validation humaine et politiques d'acces ;
- modele de donnees, migrations, retention, import/export ;
- routes, API, services, jobs, agents runtime et integrations ;
- navigation, ecrans, composants UI et design system ;
- tests, fixtures, donnees de demo, observabilite et logs ;
- lots SR existants, task memories, decisions actives et stop conditions ;
- risques de complexite, dette, compatibilite et sequence de livraison.

Sortie attendue :

```text
Global Impact Gate:
- required: oui/non
- surfaces_reviewed: [...]
- impacted_lots: [...]
- new_lots_to_create: [...]
- lots_to_reopen_or_block: [...]
- assumptions: [...]
- open_questions: [...]
- sequencing_recommendation: ...
```

Si l'analyse revele un impact large, Codex doit stopper avant codage significatif et demander validation du delta backlog, sauf si une regle projet autorise explicitement l'autonomie sur ce type de mutation.

### Lot Dependency Reconciliation

Apres un Global Impact Gate requis, Codex doit relire les lots existants pertinents et les classer.

Classes autorisees :

```text
unaffected      aucun impact identifie apres verification raisonnable
impacted        le lot doit etre ajuste mais reste executable
blocked_by      le lot ne doit pas etre execute avant une decision ou un autre lot
reopened        le lot deja traite doit etre repris
superseded      le lot ou son approche est remplace
split_required  le lot doit etre decoupe avant execution sure
depends_on      le lot doit declarer une dependance nouvelle
```

La reconciliation doit rester proportionnee : relire le backlog et les sources pertinentes, pas tout le repository si RepoMap/KG suffit a identifier les surfaces a risque. Les conclusions factuelles restent soumises au Fact Gate.

### Propagation Gate

Le Propagation Gate, alias Reference Integrity Gate, empeche les regressions dues a une propagation incomplete d'un changement de symbole ou de contrat.

Il est obligatoire quand le diff prevu ou observe change un element partage :

- nom de fonction, methode, classe, hook, composant exporte ou helper reutilise ;
- signature, parametre, type, interface ou schema partage ;
- champ API, payload JSON, endpoint, route, evenement ou message ;
- champ DB, migration, cle de configuration ou variable d'environnement ;
- contrat d'agent runtime, prompt, tool/action, output schema ou binding controle ;
- import/export public, barrel file, package boundary ou service commun.

Il n'est pas obligatoire pour une variable purement locale dans une fonction privee si la lecture du fichier confirme qu'aucun consommateur externe n'existe. Cette exception doit rester proportionnee et verifiable.

Niveaux de risque :

```text
low       variable locale ou helper prive dans un fichier
medium    fonction, type ou helper utilise dans plusieurs fichiers d'un module
high      contrat cross-module, API, frontend/backend, composant central, service partage
critical  DB, auth, permissions, secrets, agent runtime, action externe, migration
```

Preflight obligatoire avant mutation quand le gate est requis :

```text
Propagation Gate preflight:
- changed_symbols: ancien nom / nouveau nom / type de symbole
- old_contract: comportement ou signature actuelle
- new_contract: comportement ou signature cible
- expected_scope: local/module/cross_module/api/db/runtime
- consumers_detected: fichiers, routes, tests ou lots consommateurs connus
- affected_surfaces: [...]
- risk_level: low/medium/high/critical
- compatibility_strategy: full_propagation/compatibility_shim/two_step_migration/not_required
- planned_reference_searches: commandes ou outils prevus
- planned_verification: tests, build, typecheck, smoke, E2E
- human_validation_required: oui/non
- human_validation_received: oui/non
```

Validation humaine :

- en mode validation humaine stricte, tout risque `medium`, `high` ou `critical` exige validation avant mutation ;
- hors mode strict, tout risque `high` ou `critical` exige validation avant mutation ;
- une migration, action externe, changement auth/permissions/secrets, contrat runtime agent ou schema DB reste soumis aux validations humaines existantes, meme si le Propagation Gate est vert.

Postcheck obligatoire apres mutation :

```text
Propagation Gate postcheck:
- reference_searches: commandes executees, par exemple `rg ancienNom`, `rg nouveauNom`
- remaining_references: references restantes
- ignored_references: references historiques ou non applicables avec justification
- consumers_checked: appels, imports/exports, tests, routes, schemas ou composants verifies
- verification: commandes executees ou raison d'impossibilite
- decision: pass/repair/blocked/not_applicable
```

Regles de cloture :

- si `propagation.required` ou `propagation_gate.required` vaut `true`, un lot ne peut pas etre `done` tant que le gate n'est pas `pass` ;
- les references restantes a l'ancien symbole doivent etre videes ou justifiees dans `ignored_references` ;
- un risque `high` ou `critical` doit declarer des `affected_surfaces`, des `consumers_checked` et une verification proportionnee ;
- `rg` seul ne suffit pas pour un contrat partage : il doit etre combine avec typecheck/build/tests/smoke/E2E selon la stack et le risque ;
- si la propagation reste incomplete, la decision de lot doit rester `repair` ou `blocked`.

Politique d'upgrade : les contrats historiques sans Propagation Gate restent valides comme historique legacy. Les audits doivent les signaler en warning, pas bloquer l'installation. Les nouveaux templates et contrats crees apres upgrade doivent renseigner le gate.

### Pass Planning Gate

Le Pass Planning Gate est obligatoire avant toute execution multi-lots.

But : eviter qu'une passe commence avec un ordre incomplet, un prerequis cache ou une validation E2E trop precoce.

Codex doit verifier :

- les lots candidats et leur statut ;
- le Lot Design Evidence Gate des lots candidats executables ;
- les dependances directes et indirectes ;
- les lots requis mais places plus tard ;
- les questions bloquantes communes ;
- les secrets, identifiants, comptes de test, assets, URLs et services requis ;
- les validations humaines, migrations et actions externes ;
- les surfaces partagees : DB, API, UI, auth, integrations, tests, agents runtime ;
- la strategie E2E groupee ou par lot ;
- le budget contexte estime.

Sortie attendue :

```text
Pass Planning Gate:
- required: oui/non
- pass_id: ...
- lots_included: [...]
- execution_order: [...]
- dependencies_satisfied: oui/non
- preflight_required: [...]
- human_validation_required: [...]
- grouped_e2e: oui/non
- stop_conditions: [...]
- decision: pass / fail / requires_user_validation
```

Une passe executable doit etre validee avec :

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

Si `pass_runtime_goal.enabled` est actif dans `PROJECT_PROFILE.yaml`, Codex doit ensuite generer `pass_runtime_goal.md`, verifier le Goal Length Gate, puis lancer ou proposer la commande `/goal` selon le niveau de validation humaine.

Stopper avant codage si :

- un lot inclus dans une passe executable n'a pas de Lot Design Evidence Gate `pass` ou `not_applicable` justifie ;
- un lot depend d'un lot non termine et non inclus plus tot dans la passe ;
- une passe `validated`, `in_progress`, `repair` ou `reopened` depend d'un lot place dans une passe anterieure mais non `done` ou `user_testing` ;
- un lot depend d'un lot place dans une passe posterieure ;
- un lot apparait dans plusieurs passes ;
- un secret, identifiant, asset ou acces requis est absent ;
- une migration ou action sensible exige validation humaine non obtenue ;
- le regroupement masque un E2E utilisateur bloquant ;
- la passe depasse le budget contexte ou melange trop de surfaces a risque.

`sequencing.dependency_overrides` est une liste d'exceptions precises pour l'ordre interne d'une passe. Chaque entree doit nommer le lot et sa dependance concernes. Elle ne doit pas servir de contournement global pour ignorer les dependances inter-passes, les doublons ou les dependances hors passe non satisfaites.

### Knowledge gate

Le knowledge gate precise comment Codex a construit sa carte du changement.

En mode `core` :

- lire `CODEBASE_MAP.md` avant toute tache multi-fichiers ou reprise ;
- consulter `CODEBASE_MAP.generated.md` si la carte courte ne suffit pas ;
- documenter les fichiers candidats puis les fichiers vraiment lus.

En mode `nexus_kg` :

- interroger Nexus KG avant de choisir les fichiers candidats ;
- verifier la fraicheur du KG si l'outil le permet ;
- produire ou demander un context pack court ;
- apres le lot, indiquer si le KG doit etre mis a jour.

### Scope gate

Le diff doit rester dans `allowed_paths` et hors `forbidden_paths` du lot.

### Spec gate

Les criteres d'acceptation doivent etre couverts ou explicitement marques incomplets.

Le Spec gate ne remplace pas le Lot Completion Gate : il verifie les criteres, tandis que le Lot Completion Gate verifie toutes les exigences validees, y compris produit, UI/UX, E2E, documentation, i18n, rebuild ou integrations.

### Verification gate

Les commandes du lot doivent etre executees ou l'impossibilite documentee.

Quand le Propagation Gate est requis, le Verification Gate doit inclure les recherches de references et les tests consommateurs proportionnes au risque, ou documenter pourquoi une verification equivalente a ete choisie.

### Design gate

Obligatoire pour toute tache UI non triviale.

Codex doit lire la direction design du projet et les ressources UI/design locales si presentes, eviter les patterns interdits et verifier par screenshot quand possible.

Le Design Gate reste distinct du UI Visual Evidence Gate. Il verifie les regles de coherence design, composants, patterns et references visuelles. Le UI Visual Evidence Gate verifie que la bonne interface a ete executee et observee via le runner.

Pour une exigence "UI alignee sur X", la preuve attendue doit couvrir le parcours ou l'ecran demande : capture Playwright, comparaison de composants/patterns, checklist visuelle ciblee ou E2E. Sans cette preuve, le Lot Completion Gate doit rester `fail` ou la decision doit etre `user_testing`/`repair`.

### Context budget gate

Avant gros lot, apres 2 lots, 20 tours utilisateur, un changement de macro-fonction ou si la session devient longue :

- mettre a jour `CURRENT_STATE.md` selon la regle plein regime si un upgrade/realignement SR, changement de version, `NEXT_SESSION_PROMPT.md`, changement structurant de backlog, lot applicatif significatif ou fin de session significative vient d'avoir lieu ;
- produire ou mettre a jour `NEXT_SESSION_PROMPT.md` ;
- recommander un handoff si le contexte devient risque.

Si `scripts/codex/context_budget_report.py` est present, l'executer avant d'enchainer un nouveau lot apres une longue passe.

Seuils recommandes pour une fenetre de contexte de 258400 tokens :

```text
green  : aucun signal hybride significatif
yellow : contexte >= 70%, ou tokens non caches >= 12k, ou cache faible sur contexte significatif, ou 2 lots traites
orange : contexte >= 82%, ou tokens non caches >= 24k, ou 20 tours utilisateur, ou 3 lots traites
red    : contexte >= 92%, ou tokens non caches >= 48k
unknown/stale/ambiguous : ne pas faire confiance au budget, creer ou rafraichir NEXT_SESSION_PROMPT avant nouveau lot long
```

Le rapport doit indiquer la session utilisee, son `cwd`, `input_tokens`, `cached_input_tokens`, `uncached_input_tokens`, `cache_ratio` et `hybrid_budget.signals`. `input_tokens` et `raw_context_percent` mesurent une pression brute de diagnostic ; ils ne declenchent pas seuls une coupure orange/rouge quand la majorite est cachee. La decision repose sur `effective_context_percent`, `uncached_input_tokens`, `cache_ratio`, les tours utilisateur et les lots traites. `uncached_input_tokens` mesure le volume nouveau non cache, et `cache_ratio` evite les coupures trop precoces sans autoriser des conversations infinies. Un rapport non fiable ne doit jamais etre assimile a `green`.

Le gate doit etre visible dans `gate_report.md`. Si aucun handoff n'est cree, indiquer pourquoi le contexte reste sain.

### Self evaluation gate

Apres implementation et avant cloture, Codex doit auto-evaluer son propre travail avec des preuves falsifiables :

- objectif initial ;
- ce que le code fait maintenant ;
- preuves : tests, logs, routes, screenshots, diff ;
- risques restants ;
- ce qui aurait pu etre oublie ;
- fichiers relus apres patch ;
- decision : `done`, `user_testing`, `repair` ou `blocked`.

### Loop Contract

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

### SR Contract 3.1.0

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

Regles critiques :

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

Validation :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Transition : les contrats 3.0.0 et les fichiers legacy restent historiques. Un contrat multi-lots reduit a une seule exigence generique produit un warning et doit etre normalise apres lecture de ses sources avant reprise ou cloture, sans reecriture massive.

### Nexus context gate

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

## Execution multi-lots par defaut

Quand le backlog contient plusieurs lots executables :

1. verifier ou proposer une passe dans `SR_PASSES.yaml` ;
2. appliquer le Pass Planning Gate ;
3. generer un Pass Runtime Goal si la passe est validee et que la fonctionnalite est activee ;
4. traiter d'abord les lots `repair`/`reopened`, puis `validated`, dans l'ordre valide de la passe ;
5. executer jusqu'a `max_lots_per_session` ou `max_lots_per_pass` si les gates restent verts ;
6. mettre a jour `SR_LOTS.yaml` apres chaque decision de statut ;
7. mettre a jour `SR_PASSES.yaml` apres chaque decision de statut de passe ;
8. produire un `gate_report.md` par lot significatif ou une section par lot dans un gate report de passe ;
9. stopper si une validation humaine, migration, dependance, regle metier absente, test bloquant ou contexte a risque apparait.

Si aucun `SR_PASSES.yaml` n'existe dans un projet ancien, Codex peut executer la politique multi-lots historique uniquement pour terminer la tache courante, puis doit proposer l'ajout d'une passe avant nouvelle execution longue.

Quand l'utilisateur valide une roadmap ou un pack de specs, Codex doit soit :

- marquer explicitement les prochains lots executables en `validated` ;
- soit creer une entree `autonomy_run` bornee dans `SR_LOTS.yaml`.

## Relation avec les task memories

`SR_LOTS.yaml` est le backlog.

`docs/codex/tasks/...` est le journal d'execution.

Un lot peut avoir plusieurs task memories si plusieurs sessions ou reprises sont necessaires.

## Relation avec handoff

Le handoff sert a passer d'une conversation a l'autre.

SR-Harness impose que le handoff reference :

- lots ouverts ;
- lots en test utilisateur ;
- exigences validees, faites, partielles et non faites avec leurs identifiants stables ;
- preuves manquantes et tests restant a executer ;
- retours utilisateur rattaches et lots rouverts ;
- decisions actives ;
- stop conditions ;
- prochain ensemble coherent a traiter.

Un handoff ou un compact ne peut jamais retirer silencieusement une exigence ouverte. La reprise commence par le registre herite et non par la proposition d'un nouveau gate cible.

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
