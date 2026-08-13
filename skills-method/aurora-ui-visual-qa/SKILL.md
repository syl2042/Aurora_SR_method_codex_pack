---
name: aurora-ui-visual-qa
description: >-
  utiliser pour toute modification UI/UX non triviale necessitant une preuve visuelle, responsive ou E2E : ecran, layout, navigation, composant central, modal, formulaire, tableau, dashboard, responsive, design system ou alignement avec une reference visuelle. Applique Design Gate, UI Test Readiness Gate et UI Visual Evidence Gate, execute le runner Playwright SR sur les routes et viewports requis, controle erreurs navigateur et overflow, et empeche la cloture sans preuve suffisante.
---

# Role

Orchestrer la validation UI SR sans implementer Playwright dans la skill.

## Sources a lire

1. `docs/codex/PROJECT_PROFILE.yaml`
2. `docs/codex/SR_HARNESS_METHOD.md`
3. `docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json` du lot courant
4. `docs/codex/SKILL_MAP.md`
5. Skill UI locale du projet si declaree, par exemple `docs/codex/project-skills/codex-<project>-ui/SKILL.md`
6. Fichiers UI reels modifies ou a verifier

## Procedure

1. Determiner si l'exigence UI est significative.
2. Lire la direction design et la skill UI locale si disponible.
3. Identifier les routes concernees par le lot.
4. Verifier la configuration `ui_validation`.
5. Appliquer le UI Test Readiness Gate.
6. Executer le runner :

```bash
node scripts/codex/sr_ui_verify.mjs --route <route>
```

ou utiliser les routes declarees dans le contrat/profil.

7. Lire le rapport machine configure, par defaut :

```text
output/playwright/ui-verification-report.json
```

8. Alimenter `sr_contract.json.ui_validation`.
9. Appliquer le UI Visual Evidence Gate.
10. Decider `done`, `repair`, `blocked` ou `user_testing`.

## Regles de cloture

- `done` exige `ui_validation.test_readiness.status = pass`.
- `done` exige `ui_validation.visual_evidence.status = pass`.
- Une redirection login detectee ne constitue jamais une preuve UI valide.
- `pageerror` bloque `done`.
- Un overflow horizontal inattendu bloque `done`.
- Si l'authentification, MFA ou une session E2E empeche l'automatisation, utiliser `blocked` ou `user_testing` avec checklist humaine concrete.

## Limites

La skill ne contient aucune regle specifique a une application. Les tokens, patterns, navigation, composants privilegies, interdits UI et references design appartiennent aux skills UI locales du projet.
