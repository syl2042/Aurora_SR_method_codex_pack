# Mettre a jour un projet vers la derniere SR Method

Tu travailles dans un repository deja equipe d'une ancienne version de Aurora SR Method.

Objectif : auditer et mettre a jour le pack SR sans modifier le code applicatif ni ecraser les adaptations projet.

Utilise le package source officiel :

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Instructions :

1. Detecter la version SR installee.
2. Verifier ou cloner le package source officiel.
3. Identifier les fichiers projet a preserver : `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `docs/codex/tasks/`, skills projet et decisions locales.
4. Preserver `SR_LOTS.yaml` et ajouter `SR_PASSES.yaml` de facon additive si absent, sans convertir automatiquement les anciens lots ou task memories.
5. Expliquer le plan d'upgrade et attendre validation explicite avant mutation.
6. Appliquer l'upgrade avec l'installateur seulement apres validation.
7. Lancer les scripts d'audit et de validation, dont `validate_pass_contract.py` si `SR_PASSES.yaml` existe.
8. Rapporter le commit source, les fichiers mis a jour, fichiers preserves, backups, warnings, statut `SR_PASSES.yaml` et prochaines etapes.
9. Recommander `prompts/fr/08_define_sr_passes_from_lots.md` si le projet contient plusieurs lots et aucune passe valide.

Ne modifie pas le code applicatif, les dependances, les migrations ou les secrets.
