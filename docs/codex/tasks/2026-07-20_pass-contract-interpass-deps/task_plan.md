# Task plan - pass contract inter-pass dependencies

## Objectif
Corriger `validate_pass_contract.py` pour accepter les dependances declarees vers une passe strictement anterieure quand la passe courante est encore `proposed` ou `planned`, tout en conservant l'exigence de statut termine pour les passes executables `validated` et `in_progress`.

## Classification
- Type: bug/regression methode.
- Backlog actif: non applicable dans le repo source du pack, qui expose des templates.
- Scope: validateur, audit SR projet, tests, documentation/migration minimale.

## Skills
- `aurora-lot-runner`
- `aurora-diagnose`
- `aurora-planning-with-files`
- `aurora-tdd`
- `aurora-review-diff`

## Hypotheses
- L'ordre global des passes est l'ordre de la liste `passes`.
- Un lot ne peut apparaitre que dans une seule passe; aucun mecanisme officiel de duplication n'est documente.
- `dependency_overrides` ne doit pas desactiver globalement les controles.
- Les projets sans `SR_PASSES.yaml` restent compatibles car l'audit ignore l'absence du fichier.

## Approche
1. Ajouter un index global `lot_id -> pass_id/index -> position lot` et signaler les duplications.
2. Adapter la validation des dependances externes a la passe courante avec distinction `proposed/planned` vs `validated/in_progress`.
3. Faire utiliser ce contexte global par le CLI et par `audit_sr_project.py`.
4. Ajouter les tests unitaires et un smoke audit temporaire.
5. Documenter la regle de migration dans le template/methode.

## Verification prevue
- `python3 -m unittest scripts.codex.test_validate_pass_contract`
- `python3 scripts/codex/validate_pass_contract.py --file <scenario>/SR_PASSES.yaml --lots-file <scenario>/SR_LOTS.yaml`
- `python3 scripts/codex/audit_sr_project.py --root <scenario>`
- `git diff --check`
