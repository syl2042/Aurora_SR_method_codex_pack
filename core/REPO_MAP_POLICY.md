# REPO_MAP_POLICY.md

Le RepoMap aide Codex a naviguer dans le code sans relire tout le repo.

- `CODEBASE_MAP.md` : carte courte, humaine, stable, 200-400 lignes.
- `CODEBASE_MAP.generated.md` : carte generee automatiquement.

## SR Core et SR Nexus

En mode `core`, RepoMap est la carte principale du codebase.

En mode `nexus_kg`, RepoMap reste obligatoire comme synthese humaine courte, mais Nexus KG devient la carte technique profonde et requetable.

Ordre de connaissance attendu :

```text
RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs
```

Mettre a jour si route, endpoint, modele, migration, service, composant central, integration ou script build/test change.
Si Nexus KG est actif, indiquer en cloture si le KG doit etre mis a jour ou a ete mis a jour.

Le code reel confirme toujours la carte.
