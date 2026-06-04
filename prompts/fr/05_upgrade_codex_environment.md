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
4. Expliquer le plan d'upgrade et attendre validation explicite avant mutation.
5. Appliquer l'upgrade avec l'installateur seulement apres validation.
6. Lancer les scripts d'audit et de validation.
7. Rapporter le commit source, les fichiers mis a jour, fichiers preserves, backups, warnings et prochaines etapes.

Ne modifie pas le code applicatif, les dependances, les migrations ou les secrets.
