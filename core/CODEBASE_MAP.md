# CODEBASE_MAP

Carte de navigation courte, a adapter au projet. Ne documenter que les entrees durables : applications, services, donnees, integrations, build et zones sensibles. Le code reel reste la source finale.

Utiliser `CODEBASE_MAP.generated.md` pour reperer des candidats, puis lire les fichiers cibles. Regenerer uniquement si la structure a change :

```bash
python3 scripts/codex/generate_repo_map.py --root . --write
```
