---
name: codex-project-domain
description: >-
  utiliser pour toute tache Codex qui touche le domaine metier du projet: objets metier, workflows, ecrans, donnees, integrations, agents IA runtime, controles ou validations humaines. Cette skill rappelle les regles non negociables, les sources de verite, les actions sensibles, les limites connues et les cas ou Codex doit demander validation avant de coder. A charger avant toute modification metier, meme si le changement semble seulement UI ou technique.
---

# Role
Utiliser cette skill avant de modifier une fonctionnalite liee au domaine.

## Declencheurs
- Objets metier :
- Workflows :
- Ecrans metier :
- Integrations :
- Agents IA runtime :
- Validations humaines :

## Regles
- Ne pas inventer de regle metier.
- Signaler toute ambiguite.
- Demander validation si action engageante.
- Garder la description frontmatter sous 1024 caracteres.
- Viser une description assez explicite pour declencher la skill sans charger tout son contenu.

## Sources de verite
- docs/domain/DOMAIN_PROFILE.md
- docs/domain/GLOSSARY.md
- docs/domain/BUSINESS_RULES.md
- docs/domain/RISK_REGISTER.md
- docs/domain/HUMAN_VALIDATION_RULES.md

## Points de vigilance
- Donnees sensibles :
- Actions critiques :
- Regles a ne pas deduire :
- Tests ou controles attendus :
