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
5. Ajouter l'outillage Pass Runtime Goal de facon additive (`build_pass_runtime_goal.py`, template `pass_runtime_goal.md`, options `sr_passes.pass_runtime_goal`) sans generer ni lancer de `/goal` pendant l'upgrade.
6. Expliquer le plan d'upgrade et attendre validation explicite avant mutation.
7. Appliquer l'upgrade avec l'installateur seulement apres validation.
8. Lancer les scripts d'audit et de validation, dont `validate_pass_contract.py` si `SR_PASSES.yaml` existe.
9. Verifier le Goal Length Gate dans la methode installee : `max_goal_command_chars: 1000`, `hard_limit: 4000`.
10. Mettre a jour ou recommander la mise a jour de `docs/CURRENT_STATE.md` avec version avant/apres, commit source, warnings, statut passes et prochaine action.
11. Rapporter le commit source, les fichiers mis a jour, fichiers preserves, backups, warnings, statut `SR_PASSES.yaml`, statut Pass Runtime Goal et prochaines etapes.
12. Recommander `prompts/fr/07_realign_sr_state_after_upgrade.md` si disponible, sinon `prompts/07_realign_sr_state_after_upgrade.md`, avant toute reprise de developpement applicatif.
13. Recommander `prompts/fr/08_define_sr_passes_from_lots.md` si le projet contient plusieurs lots et aucune passe valide.
14. Recommander `build_pass_runtime_goal.py` seulement apres realignement et validation d'une passe `validated` ou `in_progress`.

Ne modifie pas le code applicatif, les dependances, les migrations ou les secrets.
