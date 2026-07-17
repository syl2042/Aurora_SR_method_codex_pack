# Definir les passes SR a partir des lots existants

Tu travailles dans un repository deja equipe de la SR Method.

Objectif : proposer ou mettre a jour `docs/codex/SR_PASSES.yaml` a partir de `docs/codex/SR_LOTS.yaml`, sans modifier le code applicatif.

Regles :

- Ne modifie aucun code applicatif.
- Ne change aucun statut de lot sans preuve et validation.
- Ne marque pas une passe `validated` sans validation utilisateur explicite.
- Une passe regroupe des lots ; elle ne remplace jamais les criteres et gates des lots.

Sources a lire :

1. `AGENTS.md`
2. `docs/codex/SR_HARNESS_METHOD.md`
3. `docs/codex/LOT_EXECUTION_METHOD.md`
4. `docs/CURRENT_STATE.md`
5. `docs/codex/SR_LOTS.yaml`
6. `docs/codex/SR_PASSES.yaml` si present
7. `docs/codex/CODEBASE_MAP.md`

Methode :

1. Valider `SR_LOTS.yaml`.
2. Classer les lots par statut et dependances.
3. Construire le graphe `depends_on`, `blocked_by`, `impacts`, `impacted_by`.
4. Proposer des passes avec ordre, rationale, preflight, validations humaines, migrations/actions externes, sources partagees, E2E groupe et stop conditions.
5. Creer ou mettre a jour `SR_PASSES.yaml` uniquement apres validation si le projet impose la validation stricte.
6. Valider avec `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml`.

Sortie attendue :

- passes proposees ;
- lots exclus et raison ;
- questions bloquantes ;
- preflight par passe ;
- E2E groupe recommande ;
- fichiers SR modifies ;
- resultat de validation ;
- prochaine passe recommandee.
