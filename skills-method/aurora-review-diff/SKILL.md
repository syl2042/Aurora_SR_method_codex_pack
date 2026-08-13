---
name: aurora-review-diff
description: >-
  utiliser avant de cloturer une tache codex. verifie le diff, le scope, les fichiers modifies, la securite, les dependances, les tests, la memoire de tache, current_state, repomap et, pour une UI significative, les preuves ui_validation, screenshots, rapport Playwright, erreurs navigateur et matrice responsive.
---

# Role
Verifier demande, scope, securite, dependances, migrations, tests, memoire, CURRENT_STATE, RepoMap, Loop Contract et risques restants.

Pour une tache non triviale, verifier que `docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json` existe et que `python3 scripts/codex/validate_loop_contract.py --file <chemin>` passe, ou documenter pourquoi le contrat n'est pas applicable.

Pour une tache UI/UX significative, verifier aussi :

- `sr_contract.json.ui_validation.required` ;
- `ui_validation.test_readiness.status` ;
- `ui_validation.visual_evidence.status` ;
- rapport `output/playwright/ui-verification-report.json` ou chemin configure ;
- screenshots attendus ;
- routes et viewports testes ;
- absence de redirection login inattendue ;
- `console.error`, `pageerror`, `requestfailed` et overflow horizontal ;
- coherence avec le Design Gate.
