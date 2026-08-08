# Definir les passes SR a partir des lots existants

Tu travailles dans un repo deja equipe de la SR Method.

Objectif : proposer ou mettre a jour `docs/codex/SR_PASSES.yaml` a partir de `docs/codex/SR_LOTS.yaml`, sans modifier le code applicatif.

Ce n'est pas une passe de developpement.
Ce n'est pas une migration applicative.

Regles :

- Ne modifie aucun code applicatif.
- Ne change aucun statut de lot sans preuve et validation.
- Ne marque pas une passe `validated` sans validation utilisateur explicite.
- Ne cree pas de contrats retroactifs pour les anciennes task memories.
- Une passe regroupe des lots ; elle ne remplace jamais les criteres et gates des lots.

Sources a lire :

1. `AGENTS.md`
2. `docs/codex/SR_BOOTSTRAP.md`
3. `docs/codex/SR_HARNESS_METHOD.md`
4. `docs/codex/LOT_EXECUTION_METHOD.md`
5. `docs/CURRENT_STATE.md`
6. `docs/codex/SR_LOTS.yaml`
7. `docs/codex/SR_PASSES.yaml` si present
8. `docs/codex/CODEBASE_MAP.md`
9. Les dernieres task memories pertinentes

Methode :

1. Lancer si possible :
   - `python3 scripts/codex/audit_sr_project.py --root .`
   - `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml`
   - `python3 scripts/codex/context_budget_report.py --root . --compact`
2. Classer les lots :
   - `done` ou `user_testing` : prerequis possibles ;
   - `validated` ou `reopened` : candidats executables ;
   - `planned` ou `proposed` : a cadrer avant execution ;
   - `blocked`, `deferred`, `superseded` : non executables.
3. Construire le graphe :
   - `depends_on` ;
   - `blocked_by` ;
   - `impacts` et `impacted_by` ;
   - stop conditions et validations humaines.
4. Proposer des passes :
   - un socle par passe quand DB/API/UI/auth sont fortement lies ;
   - pas plus de `max_lots_per_pass` sauf validation ;
   - remonter dans la passe tout lot prerequis place plus tard ;
   - sortir de la passe tout lot qui exige une validation E2E bloquante avant le reste.
5. Pour chaque passe, declarer :
   - lots inclus et ordre ;
   - rationale ;
   - preflight : secrets, identifiants, assets, services, validations humaines, migrations, actions externes ;
   - sources partagees ;
   - E2E groupe ou par lot ;
   - stop conditions.
6. Preparer la suite d'execution sans la lancer :
   - si une passe est proposee pour execution avec Codex CLI `/goal`, indiquer que `pass_runtime_goal.md` devra etre genere apres validation ;
   - rappeler le Goal Length Gate : `max_goal_command_chars: 1000`, `hard_limit: 4000` ;
   - rappeler qu'une passe suivante ne doit pas etre enchainee sans validation utilisateur.
7. Creer ou mettre a jour `docs/codex/SR_PASSES.yaml` uniquement apres validation utilisateur si le projet impose la validation stricte.
8. Valider :
   - `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml`

Sortie attendue :

- passes proposees ;
- lots exclus et raison ;
- questions bloquantes ;
- preflight a regler avant chaque passe ;
- E2E groupe recommande ;
- Pass Runtime Goal a generer apres validation, si applicable ;
- fichiers SR modifies ;
- resultat de validation ;
- prochain lot ou prochaine passe recommande.
