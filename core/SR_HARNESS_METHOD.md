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
→ verifier les preuves avant plan avec RepoMap/KG puis code reel
→ executer un lot borne
→ auto-evaluer le resultat
→ produire gate report
→ mettre a jour memoire
```

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

### `SR_CONTEXT_PACK.md`

Contexte court pour la session ou le lot courant.

Il doit reduire les tokens en evitant de relire toutes les specs, tasks et fichiers.

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
done          code/verifications techniques termines
user_testing  attente test reel utilisateur
reopened      lot rouvert apres bug, oubli ou regression
blocked       attente decision, acces, source, spec ou architecture
deferred      reporte volontairement
superseded    remplace par une decision ou un autre lot
```

`done` ne signifie pas "valide produit".

Si un test reel utilisateur est requis, utiliser `user_testing`.

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

### Verification gate

Les commandes du lot doivent etre executees ou l'impossibilite documentee.

### Design gate

Obligatoire pour toute tache UI non triviale.

Codex doit lire la direction design du projet et les ressources UI/design locales si presentes, eviter les patterns interdits et verifier par screenshot quand possible.

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

- sources lues pour l'evidence gate ;
- fichiers modifies ;
- commandes executees ou raison de non-execution ;
- liste E2E utilisateur concrete ;
- mises a jour memoire ;
- statut context budget et `NEXT_SESSION_PROMPT.md` ;
- decision de transition conversationnelle ;
- protocole de reprise a donner a l'utilisateur.

Regles critiques :

- si `status_decision` vaut `user_testing`, `e2e_user_tests.items` doit contenir une vraie liste de tests ;
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

### SR Contract 3.0.0

A partir de SR 3.0.0, le contrat vivant cible d'un lot est :

```text
docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Il fusionne la partie machine de `task_plan.md`, `findings.md`, `decisions.md`, `verification.md`, `gate_report.md` et `loop_contract.json` autour d'une question principale : toutes les intentions utilisateur validees dans le lot sont-elles couvertes ?

Champs structurants :

- `validated_requests` : intentions validees, statut, couverture, fichiers et verification ;
- `scope` : inclus, exclus, chemins autorises/interdits ;
- `product_truth` : verites produit/metier a preserver ;
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
- un lot `done` est invalide si une requete reste `todo`, `doing`, `requires_e2e` ou `blocked` ;
- `product_truth.items` est obligatoire si `product_truth.required` vaut `true` ;
- `e2e.items` est obligatoire si `e2e.required` vaut `true` ;
- contexte `orange` impose `recommend_new_conversation` ou `stop_for_new_conversation` ;
- contexte `red`, `stale` ou `ambiguous` impose `stop_for_new_conversation`.

Validation :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Transition : tant que le lot de migration SR 3.0.0 n'a pas ete execute, `loop_contract.json` reste requis par les projets SR 2.x et les fichiers legacy restent historiques.

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

1. traiter d'abord les lots `reopened`, puis `validated` ;
2. executer jusqu'a `max_lots_per_session` si les gates restent verts ;
3. mettre a jour `SR_LOTS.yaml` apres chaque decision de statut ;
4. produire un `gate_report.md` par lot significatif ou une section par lot dans un gate report groupe ;
5. stopper si une validation humaine, migration, dependance, regle metier absente, test bloquant ou contexte a risque apparait.

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
- decisions actives ;
- stop conditions ;
- prochaine action recommandee.

## Regle de cloture

Avant de clore une tache SR-Harness :

- mettre a jour `progress.md` ;
- completer `verification.md` ;
- produire `gate_report.md` pour un lot execute ;
- produire et valider `loop_contract.json` pour une tache non triviale ;
- mettre a jour `SR_LOTS.yaml` si le statut change ;
- si `SR_LOTS.yaml` a ete modifie, executer `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` et noter le resultat dans `verification.md` ;
- mettre a jour `CURRENT_STATE.md` selon la regle plein regime ;
- utiliser `aurora-review-diff`.

Format de cloture utilisateur recommande :

```text
Ce qui est fait
Resultat observe
Lecture expert / produit
Verifications executees
Memoire SR mise a jour
Tests E2E utilisateur a faire
Prochaine etape recommandee
```
