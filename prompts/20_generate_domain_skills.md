# Generer les skills metier Codex

Generer les SKILL.md valides apres validation PM.

Regles :
- distinguer skills Codex metier et skills runtime agents ;
- frontmatter seulement `name` et `description` ;
- description sous 1024 caracteres ;
- viser 300 a 800 caracteres pour une skill metier Codex ;
- la description doit expliquer role, declencheurs, objets couverts, risques et cas ou demander validation ;
- eviter les descriptions generiques comme "utiliser pour le domaine du projet" ;
- `agents/openai.yaml` doit contenir un `short_description` distinct de 25 a 64 caracteres ;
- details longs dans `references/` ;
- ajouter `agents/openai.yaml` si le pack projet l'utilise ;
- mettre a jour `docs/codex/SKILL_MAP.md` ;
- verifier que `docs/codex/SKILL_DIGEST.md` reste vrai ou ajouter une note de declencheur si necessaire ;
- documenter les declencheurs, limites et validations humaines ;
- lancer `validate_skills.py`.

Stockage :
- generer les skills metier Codex dans `docs/codex/project-skills/` par defaut ;
- ne pas les copier dans `~/.codex/skills` sauf demande explicite ;
- ne pas generer de skill runtime agent dans `~/.codex/skills` sauf si elle sert explicitement Codex ;
- les skills runtime applicatives doivent rester dans le stockage ou les fichiers de l'application.
