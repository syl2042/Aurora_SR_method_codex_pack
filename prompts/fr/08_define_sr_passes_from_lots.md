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
3. Verifier le Lot Design Evidence Gate : exclure d'une passe executable tout lot `planned`, `validated`, `in_progress` ou `reopened` sans `design_evidence.status: pass` ou `not_applicable` justifie. Un lot `proposed` peut rester exploratoire.
4. Construire le graphe `depends_on`, `blocked_by`, `impacts`, `impacted_by`.
5. Proposer des passes avec ordre, rationale, preflight, validations humaines, migrations/actions externes, sources partagees, E2E groupe et stop conditions.
6. Preparer la suite d'execution sans la lancer : si une passe est proposee pour Codex CLI `/goal`, indiquer que `pass_runtime_goal.md` devra etre genere apres validation, avec Goal Length Gate (`max_goal_command_chars: 1000`, `hard_limit: 4000`) et sans enchainement silencieux de la passe suivante.
7. Creer ou mettre a jour `SR_PASSES.yaml` uniquement apres validation si le projet impose la validation stricte.
8. Valider avec `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml`.

Sortie attendue :

- passes proposees ;
- lots exclus et raison ;
- lots exclus pour Lot Design Evidence Gate manquant ou incomplet ;
- questions bloquantes ;
- preflight par passe ;
- E2E groupe recommande ;
- Pass Runtime Goal a generer apres validation, si applicable ;
- fichiers SR modifies ;
- resultat de validation ;
- prochaine passe recommandee.
