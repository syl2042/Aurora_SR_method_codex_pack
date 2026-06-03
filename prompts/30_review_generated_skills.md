# Revue des skills generees

Verifier :
- noms ;
- `description` frontmatter sous 1024 caracteres, assez explicite pour declencher la skill ;
- `agents/openai.yaml` avec `short_description` de 25 a 64 caracteres ;
- declencheurs ;
- regles critiques ;
- references ;
- absence d'hallucination metier ;
- distinction skills Codex metier vs skills runtime agents ;
- stockage local dans `docs/codex/project-skills/` par defaut ;
- coherence avec `docs/codex/SKILL_DIGEST.md` sans dupliquer tout le contenu des skills ;
- sortie de `validate_skills.py`.
