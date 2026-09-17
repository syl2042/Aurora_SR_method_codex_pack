# ui — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## UI Test Readiness Gate

Le UI Test Readiness Gate precede l'execution Playwright complete.

But : repondre a la question suivante avant de produire des preuves visuelles :

```text
Sommes-nous reellement capables de tester l'interface demandee ?
```

Statuts autorises :

```text
pass, fail, blocked, not_applicable
```

Le gate verifie au minimum :

- application joignable et `base_url` resolue ;
- routes demandees connues pour le lot ;
- mode auth projet : `none`, `storage_state`, `setup_command` ou `manual` ;
- presence et validite pratique du `storageState` quand requis ;
- detection de redirection login ;
- donnees de test ou preflight humain explicitement bloques si necessaire.

Cas rouge obligatoire : si la route attendue redirige vers `/login`, `/signin`, `/auth`, `/oauth/`, `/oidc/`, `/if/flow/` ou un pattern configure, `login_redirect_detected = true`. Codex ne doit jamais utiliser le screenshot de cette page comme preuve UI valide de la route demandee.

## UI Visual Evidence Gate

Le UI Visual Evidence Gate suit l'execution du runner.

But : repondre a la question suivante :

```text
L'interface reellement demandee a-t-elle ete observee et verifiee avec suffisamment de preuves ?
```

```text
pass, repair, blocked, not_applicable
```

Le gate consomme le rapport `output/playwright/ui-verification-report.json` ou le chemin configure et verifie :

- routes effectivement testees ;
- matrice viewports attendue ;
- screenshots produits ;
- `console.error` ;
- `pageerror` ;
- `requestfailed` ;
- overflow horizontal inattendu ;
- redirection login inattendue.

Par defaut, un lot UI non trivial teste les routes concernees sur quatre viewports :

```yaml
- name: desktop-xl
  width: 1440
  height: 900
- name: desktop
  width: 1280
  height: 800
- name: tablet
  width: 768
  height: 1024
- name: mobile
  width: 390
  height: 844
```

Ces viewports restent surchargeables par projet. Pour API-only, CLI, backend, worker ou migration, les gates UI doivent etre `not_applicable` avec justification.

## Design gate

Obligatoire pour toute tache UI non triviale.

Codex doit lire la direction design du projet et les ressources UI/design locales si presentes, eviter les patterns interdits et verifier par screenshot quand possible.

Le Design Gate reste distinct du UI Visual Evidence Gate. Il verifie les regles de coherence design, composants, patterns et references visuelles. Le UI Visual Evidence Gate verifie que la bonne interface a ete executee et observee via le runner.

Pour une exigence "UI alignee sur X", la preuve attendue doit couvrir le parcours ou l'ecran demande : capture Playwright, comparaison de composants/patterns, checklist visuelle ciblee ou E2E. Sans cette preuve, le Lot Completion Gate doit rester `fail` ou la decision doit etre `user_testing`/`repair`.

## Design gate minimal

Pour une tache UI :

1. Identifier les composants/patterns existants.
2. Eviter les composants locaux one-shot si un wrapper existe.
3. Eviter l'empilement de cartes et sections sans hierarchy.
4. Respecter tokens/theme existants.
5. Produire screenshot Playwright si l'application peut tourner.
6. Documenter toute exception.
