# SR Method

## Definition

SR signifie **Specification Runtime**.

La SR Method est la doctrine generale Auroramind pour encadrer le travail avec des agents IA dans un projet logiciel. Elle transforme des specs, une memoire projet et des gates de verification en un cadre executable par Codex ou par des agents applicatifs.

Elle comporte deux branches complementaires :

- **SR Development Method** : cadrage du developpement assiste par IA, avec lots, evidence gate, knowledge gate, verification, auto-evaluation, memoire de tache et reprise de contexte.
- **SR Agent Method** : construction d'agents IA runtime embarques dans une application, avec action produit bornee, representation interne stable, contrat runtime type, prompt contract, message builder, bindings controles, tools/actions, schemas de sortie, routing/fallback, traces et validation humaine.

## Positionnement

La SR Method rejoint les principes du harness engineering : l'IA n'est pas seulement appelee par un prompt, elle est encadree par un environnement de travail, des outils, des contrats et des boucles de verification.

La difference est que la SR Method applique ce principe a l'echelle complete d'un projet :

- backlog vivant ;
- cartographie codebase ;
- lots atomiques et passes d'execution multi-lots ;
- skills Codex et skills runtime separees ;
- gates de preuve ;
- gate de propagation des changements de symboles et contrats partages ;
- memoire long terme ;
- budget contexte ;
- verification humaine et automatisee ;
- verification UI executable via UI Verification Harness ;
- agents runtime applicatifs.

## Validation humaine stricte

La SR Method supporte un mode de validation humaine stricte, activable par `AGENTS.md`, par un lot, par une reprise ou par l'utilisateur. Dans ce mode, Codex peut analyser, lire et recommander sans validation, mais ne modifie aucun fichier et ne lance aucune action de mutation tant que l'utilisateur n'a pas ecrit exactement `je valide`.

La validation ne couvre que l'action ou le plan decrit juste avant. Toute extension de perimetre, dependance, migration, configuration, donnees, agent IA runtime, backlog, publication Git, action destructive ou changement metier exige une nouvelle validation explicite.

Une validation utilisateur d'un lot ou d'une passe engage tout le perimetre decrit juste avant validation. Les principes de solution simple, changement chirurgical, scope minimal et respect du style local s'appliquent a la maniere d'implementer chaque exigence validee ; ils ne peuvent jamais reduire silencieusement le perimetre fonctionnel valide.

Si Codex estime que le lot valide est trop large, trop risque, ambigu ou doit etre decoupe, il doit le declarer avant mutation, proposer le decoupage et attendre une nouvelle validation utilisateur. Il est interdit de livrer un sous-ensemble comme si le lot complet etait couvert.

## SR 3.1.0 - Registre persistant des demandes

A partir de SR 3.0.0, la cible machine d'un lot non trivial est un contrat vivant :

```text
docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Ce contrat ne remplace pas instantanement l'historique existant. Les fichiers `task_plan.md`, `findings.md`, `progress.md`, `decisions.md`, `verification.md`, `gate_report.md` et `loop_contract.json` restent lisibles pendant la transition, mais la source machine cible devient `sr_contract.json`.

Le contrat 3.1.0 garde `validated_requests` comme registre canonique. Une ligne doit representer une intention utilisateur stable, pas un resume global tel que « couvrir les cinq lots ». Il faut distinguer au minimum chaque lot valide, chaque critere produit important, chaque demande UI/UX explicite, chaque exclusion et chaque E2E ou validation humaine attendue.

Chaque ligne separe obligatoirement :

- `implementation_status` : `not_started`, `partial`, `complete` ou `defective` ;
- `evidence_status`, calcule depuis les preuves attendues et obtenues ;
- `decision`, calculee pour l'exigence ;
- le lot et la passe d'origine, les surfaces touchees, le travail et les tests restants, l'historique et toute decision explicite de report, annulation ou deplacement.

Choix de schema : `unit_verified`, `build_verified`, `runtime_verified` et `e2e_verified` ne sont pas des etapes mutuellement exclusives et ne forment pas une progression lineaire. SR 3.1.0 les represente donc comme des entrees typees dans `expected_evidence` et `obtained_evidence`. L'`evidence_status` agrege mesure uniquement la completude (`missing`, `partial`, `failed`, `sufficient`, `awaiting_user_acceptance`, etc.). Cette normalisation evite qu'un build vert ecrase un E2E manquant ou qu'une preuve unitaire soit prise pour une preuve runtime.

Le contrat doit aussi porter explicitement :

- les intentions utilisateur validees dans `validated_requests` ;
- le scope inclus/exclu ;
- les verites produit/metier a ne pas perdre ;
- les sources lues et preuves ;
- les skills methode et metier ;
- le plan, les constats et decisions ;
- les fichiers modifies ;
- les commandes de verification ;
- les gates ;
- les tests E2E utilisateur ;
- le statut contexte ;
- la decision de transition conversationnelle.

Regle centrale : le statut du lot et le Completion Gate sont derives des exigences. Une implementation `partial`, `not_started` ou `defective` impose `repair` (ou `blocked` seulement si elle n'a pas commence et depend reellement d'une autorite externe). Une implementation `complete` dont il manque seulement un E2E, une preuve visuelle reelle ou une acceptation humaine autorise `user_testing`. Une verification technique unitaire, build ou runtime manquante reste `repair`. Une preuve rouge impose `repair`.

Regle de completude : la table de couverture est une vue derivee, ligne par ligne, du registre ; elle ne peut pas contredire celui-ci. Un gate rouge interdit les affirmations non qualifiees « termine », « complet », « livre » ou « implemente ». La cloture utilisateur commence par `Demande utilisateur | Etat | Preuve | Reste a faire`.

Regle de reprise : un retour sur une fonction deja validee est classe par defaut `existing_requirement_repair`. Il rouvre le lot d'origine, rattache le retour au `requirement_id`, recharge toutes les exigences ouvertes du lot et de la passe, puis organise une reprise consolidee. Un nouveau lot n'est autorise que pour une demande reellement hors scope avec `new_lot_justification` explicite.

Regle de propagation : quand un lot modifie un symbole ou contrat partage (fonction, signature, type, schema, endpoint, champ DB, config, import/export, composant ou agent runtime), Codex doit annoncer avant mutation les consommateurs et surfaces a risque, obtenir la validation humaine requise selon le risque, puis prouver apres mutation que les references, appels, imports/exports, signatures, tests et smokes proportionnes ont ete verifies. Un lot ne peut pas etre `done` si le Propagation Gate requis n'est pas `pass`.

Regle UI SR 3.6.0 : pour une exigence UI/UX significative, un build, un lint, des tests unitaires ou un HTTP 200 ne suffisent pas. Si `ui_validation.required` vaut `true`, `ui_validation.test_readiness.status` et `ui_validation.visual_evidence.status` doivent etre `pass` avant `done`. Une capture de page de login, un `pageerror` ou un overflow horizontal inattendu ne constituent pas une preuve UI valide.

Validation :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Les contrats 3.0.0 restent lisibles. Ils ne sont pas reecrits en masse. Un registre legacy generique doit toutefois produire un avertissement et etre normalise manuellement avant toute reprise ou cloture multi-lots ; il est interdit d'inventer retrospectivement des intentions utilisateur sans source.

La compatibilite d'upgrade concerne aussi le layout installe. Les distributions officielles SR 2.2.0 a 3.0.0 sont testees par fixtures representatives : les fichiers projet sont preserves, le bloc SR de `AGENTS.md` est realigne et une installation sans passes recoit un registre valide `passes: []`. Une installation unknown/partial ou adaptee localement reste auditee fichier par fichier. Le code retour de l'installateur ne prouve pas a lui seul la reussite : un postcheck rouge impose `repair`.

## Regle de compatibilite

Les anciens noms techniques restent acceptes :

- `SR_HARNESS_METHOD.md` est l'alias historique de la SR Development Method.
- `AI_AGENT_RUNTIME_METHOD.md` est l'alias historique de la SR Agent Method.

Ne pas casser les projets existants pour un renommage de fichiers. Preferer ajouter les nouveaux docs et garder les anciens chemins comme alias.
