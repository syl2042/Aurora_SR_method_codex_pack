# impact — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Backlog Mutation Gate

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

## Global Impact Gate

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

## Lot Dependency Reconciliation

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

## 3c. Backlog Mutation Gate

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

## 3d. Global Impact Gate

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

## 3e. Lot Dependency Reconciliation

Apres un Global Impact Gate requis, relire les lots existants pertinents et les classer :

```text
unaffected, impacted, blocked_by, reopened, superseded, split_required, depends_on
```

Mettre a jour `depends_on`, `blocked_by`, `impacts`, `impacted_by`, `supersedes`, `superseded_by` ou le statut du lot si necessaire. Les lots non verifies ne doivent pas etre declares `unaffected` sans source.


## Regle distribuee par ancien installateur

- Backlog Mutation Gate : si une demande, une decouverte ou une reparation introduit une fonction structurante ou un impact durable, classer l'evenement, analyser les implications globales, puis mettre a jour `SR_INBOX.yaml` ou `SR_LOTS.yaml`, ou documenter pourquoi aucune mutation n'est requise.

## Regle distribuee par ancien installateur

- Global Impact Gate : avant de cadrer ou coder une fonction structurante, analyser son impact sur le produit global, les parcours, donnees, permissions, API/services, UI, tests, lots existants, dependances, migrations et risques, de facon agnostique au domaine.

## Regle distribuee par ancien installateur

- Lot Dependency Reconciliation : classer les lots existants pertinents comme `unaffected`, `impacted`, `blocked_by`, `reopened`, `superseded`, `split_required` ou `depends_on` avant codage significatif.

## Regle distribuee par ancien installateur

- Backlog Contract : apres modification de `SR_LOTS.yaml`, executer `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` avant cloture.
