---
name: aurora-review-diff
description: >-
  utiliser avant de cloturer une tache codex. verifie le diff, le scope, les fichiers modifies, la securite, les dependances, les tests, la memoire de tache, current_state et repomap.
---

# Role
Verifier demande, scope, securite, dependances, migrations, tests, memoire, CURRENT_STATE, RepoMap, Loop Contract et risques restants.

Pour une tache non triviale, verifier que `docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json` existe et que `python3 scripts/codex/validate_loop_contract.py --file <chemin>` passe, ou documenter pourquoi le contrat n'est pas applicable.
