---
name: aurora-domain-skill-factory
description: >-
  utiliser au lancement d’un nouveau projet, apres export domaine ou avant une tache metier sans skill locale pertinente. Analyse le domaine, propose des skills Codex metier locales au projet dans docs/codex/project-skills, distingue les skills runtime agents, prepare skill_map, docs/domain, validations humaines et descriptions sous 1024 caracteres.
---

# Role
Transformer specs/export domaine en skills metier. Ne pas inventer le metier. Une skill par domaine recurrent, risque ou non evident.

## Declenchement

Utiliser :
- au lancement d'un nouveau projet ;
- apres export domaine ;
- avant une tache metier si aucune skill Codex metier pertinente n'existe ;
- lorsqu'un agent IA runtime, un workflow, une validation humaine ou une integration verticale est cree ou modifie.

## Sources minimales

Lire selon disponibilite :
- `docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md`
- `docs/codex/AI_AGENT_RUNTIME_METHOD.md` si agents IA
- PRD, brief, docs/domain
- modeles DB, schemas, migrations, OpenAPI
- routes backend et ecrans frontend metier
- exports domaine, AIP, Knowledge Graph, RAG/KG
- decisions, ADR, tickets, commentaires humains

## Sortie attendue

Avant generation, produire une proposition avec :
- cartographie des objets metier ;
- workflows ;
- actions sensibles ;
- regles critiques ;
- validations humaines ;
- risques ;
- questions ouvertes ;
- skills Codex metier proposees ;
- skills runtime agents distinctes ;
- documents `docs/domain/` a creer ou mettre a jour.

## Regles

- Ne pas coder pendant la phase de proposition.
- Ne pas inventer une regle metier absente des sources.
- Si une tache touche le metier sans skill pertinente, recommander la creation d'une skill et attendre validation.
- Distinguer explicitement skills Codex et skills runtime.
- Stocker les skills Codex metier dans `docs/codex/project-skills/` par defaut.
- Ne pas copier les skills metier dans `~/.codex/skills` sauf demande explicite.
- Une skill Codex doit avoir des declencheurs concrets et des regles non negociables.
- Une skill runtime doit rester dans l'application ou son stockage runtime, sauf si elle sert aussi Codex.

## Generation apres validation

Generer des `SKILL.md` valides :
- frontmatter limite a `name` et `description` ;
- description courte et orientee declenchement ;
- details longs dans `references/` si necessaire ;
- `agents/openai.yaml` si le projet utilise cette convention ;
- mise a jour de `docs/codex/SKILL_MAP.md`.

Executer `validate_skills.py` apres generation.
