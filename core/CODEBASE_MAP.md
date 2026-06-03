# CODEBASE_MAP.md

Carte courte du codebase pour aider Codex a choisir les bons fichiers. Le code reel reste la source de verite.

## Frontend
- `frontend/app/` : routes Next.js.
- `frontend/components/` : composants.
- `frontend/lib/` : clients/helpers.

## Backend
- `backend/app/main.py` : app FastAPI.
- `backend/app/api/` : routes API.
- `backend/app/models/` : modeles.
- `backend/app/schemas/` : schemas.
- `backend/app/services/` : services/integrations.
- `backend/alembic/` : migrations.

## Fichiers sensibles
`.env*`, Docker/Compose, config securite/auth, clients API, migrations, services integrations.

Regenerer : `python3 scripts/codex/generate_repo_map.py --write`.
