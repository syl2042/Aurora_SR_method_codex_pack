# Findings

- `validate_pass()` ne recoit actuellement que la passe courante et `lots_by_id`.
- Une dependance absente de `item["lots"]` est traitee comme externe sans savoir si elle appartient a une passe anterieure.
- Les `dependency_overrides` actuels ne s'appliquent qu'a l'ordre interne de la passe; ils ne doivent pas devenir un contournement global.
- `audit_sr_project.py` reconstruit lui aussi la validation passe par passe et doit utiliser le meme contexte global que le CLI.
