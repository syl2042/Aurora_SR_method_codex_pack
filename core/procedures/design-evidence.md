# design-evidence — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Lot Design Evidence Gate

Le Lot Design Evidence Gate empeche qu'un lot pret a executer soit defini sur une supposition non verifiee.

Il est obligatoire avant de creer ou promouvoir un lot en `planned`, `validated`, `in_progress`, `repair` ou `reopened`.

Un lot peut rester `proposed` sans preuve complete s'il sert a capturer une intention, une piste exploratoire ou une question a investiguer. Dans ce cas, il doit garder ses hypotheses et ne doit pas etre mis dans une passe executable.

Sortie attendue dans `SR_LOTS.yaml` :

```text
design_evidence:
- status: pending / pass / fail / not_applicable
- code_read_required: oui/non
- candidate_files: [...]
- confirmed_files_read: [...]
- symbols_or_routes_checked: [...]
- tests_or_logs_checked: [...]
- assumptions_remaining: [...]
- open_questions: [...]
- not_applicable_reason: ...
- status_ceiling_if_not_pass: proposed
```

Regles :

- `planned`, `validated`, `in_progress`, `repair` et `reopened` exigent `design_evidence.status: pass` ou `not_applicable` avec raison ;
- si `code_read_required: true`, `confirmed_files_read` ne doit pas etre vide ;
- si des fichiers existent et peuvent trancher le cadrage, Codex doit les lire avant de proposer un plan engageant ;
- pour un lot greenfield, Codex doit lire les patterns adjacents quand ils existent ou justifier l'absence de surface code.

## 2c. Lot Design Evidence Gate

Avant de creer ou promouvoir un lot en `planned`, `validated`, `in_progress`, `repair` ou `reopened`, prouver que le cadrage repose sur le code reel :

- fichiers candidats identifies depuis RepoMap/KG, recherche locale ou sources SR ;
- fichiers reellement lus avant plan engageant ;
- routes, composants, services, schemas, contrats, tests ou logs verifies quand ils existent ;
- hypotheses restantes et questions bloquantes listees ;
- justification explicite si le lot est greenfield ou pure documentation et que la lecture code est `not_applicable`.

Sans gate `pass` ou `not_applicable` justifie, le statut maximal est `proposed`.
