# Definir les skills metier Codex depuis un export domaine

Ne code rien.

Lire :
- `docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md`
- `docs/codex/SKILL_DIGEST.md`
- codex_domain_pack ou export domaine
- PRD, OpenAPI, docs/domain
- PROJECT_PROFILE
- SKILL_MAP
- modele DB, routes, ecrans metier si disponibles

Produire :
- cartographie metier ;
- objets metier ;
- workflows ;
- actions sensibles ;
- regles critiques ;
- validations humaines ;
- risques ;
- skills Codex metier proposees ;
- skills runtime agents a distinguer ;
- docs/domain manquants ;
- questions PM.

Regle : si une future tache metier n'a pas de skill Codex pertinente, proposer la skill avant tout code.
Les skills metier Codex proposees doivent etre locales au projet par defaut dans `docs/codex/project-skills/`.
Chaque proposition doit contenir une description frontmatter de 300 a 800 caracteres, sous la limite 1024 caracteres, avec role, declencheurs, objets couverts, risques et validations humaines.

Stop apres proposition.
