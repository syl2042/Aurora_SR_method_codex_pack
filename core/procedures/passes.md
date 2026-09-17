# passes — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## `SR_PASSES.yaml`

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

## Niveau 2 - Multi-lot borne

Codex peut enchainer plusieurs lots si tous les gates restent verts.

Ce niveau est le comportement attendu quand l'utilisateur valide une roadmap, un gros brief ou une phase autonome bornee. L'utilisateur ne doit pas avoir a repeter "fais les 3 prochains lots" si `SR_LOTS.yaml` contient deja des lots `validated` ou `reopened`.

Politique recommandee :

```yaml
max_lots_per_session: 3
max_repair_attempts_per_lot: 2
stop_on_gate_failure: true
```

## Pass Planning Gate

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

## 1b. Pass Planning Gate

Avant toute execution multi-lots, verifier la passe :

- les lots inclus existent dans `SR_LOTS.yaml` ;
- les dependances sont terminees, incluses plus tot dans la passe, ou placees dans une passe strictement anterieure quand la passe courante est encore `proposed` ou `planned` ;
- les passes `validated`, `in_progress`, `repair` et `reopened` n'ont que des dependances anterieures reellement satisfaites (`done` ou `user_testing`) ;
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


## Regle distribuee par ancien installateur

- Pour une execution multi-lots, creer ou verifier une passe dans `docs/codex/SR_PASSES.yaml` avant codage : lots inclus, ordre, preflight, validations humaines, secrets/actions externes, criteres d'arret et E2E groupe.

## Regle distribuee par ancien installateur

- Politique multi-lots par defaut : traiter les lots `repair`/`reopened` puis `validated`, jusqu'a 3 lots si les gates restent verts; stopper sur gate rouge, validation humaine requise ou contexte a risque.

## Regle distribuee par ancien installateur

- Pass Planning Gate : avant toute passe, verifier que les dependances directes sont terminees ou incluses plus tot dans la passe; utiliser `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` si disponible.
