# propagation — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Propagation Gate

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

## 3f. Propagation Gate preflight

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


## Regle distribuee par ancien installateur

- Propagation Gate : si un changement touche un symbole ou contrat partage, annoncer avant mutation les consommateurs et surfaces a risque, demander validation humaine si le risque depasse le local, puis verifier apres mutation les references, appels, imports/exports, signatures, tests et smokes proportionnes avant toute cloture `done`.
