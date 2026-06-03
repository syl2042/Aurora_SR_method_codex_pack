# PROJECT_SKILLS_POLICY.md

## Objectif
Eviter que le Codex global du serveur accumule toutes les skills metier de tous les projets.

La politique SR distingue trois familles :

1. Skills methode SR globales.
2. Skills metier Codex locales au projet.
3. Skills runtime applicatives injectees dans les agents IA.

## Politique recommandee

### Skills methode SR globales

Installer dans `~/.codex/skills` :
- `aurora-planning-with-files`
- `aurora-diagnose`
- `aurora-tdd`
- `aurora-review-diff`
- `aurora-to-prd`
- `aurora-architecture-check`
- `aurora-repomap-maintainer`
- `aurora-domain-skill-factory`
- `aurora-terminal-token-optimizer`
- `aurora-lot-runner`

Ces skills sont transverses, stables et utiles dans tous les projets.

### Skills metier Codex locales

Stocker par defaut dans le repo projet :

```text
docs/codex/project-skills/
  codex-{project}-core/
    SKILL.md
    references/
  codex-{project}-ui/
    SKILL.md
    references/
  codex-{project}-agent-runtime/
    SKILL.md
    references/
```

Ces skills ne doivent pas etre copiees automatiquement dans `~/.codex/skills`, sauf decision explicite pour une session ou un projet pilote.

## Limite pratique
Si l'environnement Codex ne decouvre automatiquement que `~/.codex/skills`, les skills locales projet doivent etre chargees par la methode SR :
- `AGENTS.md` pointe vers `docs/codex/SKILL_MAP.md`.
- `SKILL_MAP.md` liste les skills locales, leurs chemins et leurs declencheurs.
- Pour une tache metier, Codex lit explicitement la skill locale pertinente avant de coder.

Ce comportement est moins automatique qu'une skill globale, mais il evite la pollution du Codex racine.

## Option d'export temporaire
Si une skill metier doit etre auto-decouverte par Codex pour une session :
1. copier explicitement la skill locale vers `~/.codex/skills/` ;
2. prefixer le nom par le projet pour eviter les collisions ;
3. supprimer ou archiver l'export quand le projet n'est plus actif.

Ne pas utiliser cet export comme mecanisme par defaut.

## Descriptions de skills
Deux champs sont a distinguer :

- `SKILL.md` frontmatter `description` : description de declenchement lue par Codex.
- `agents/openai.yaml` `interface.short_description` : libelle court d'interface.

Contraintes :
- `description` : maximum 1024 caracteres ; viser 300 a 800 caracteres pour une skill metier ; decrire le role, les declencheurs, les objets couverts, les risques et les moments ou demander validation.
- `short_description` : 25 a 64 caracteres ; rester humainement lisible pour les listes et chips UI.
- Ne pas mettre les regles longues dans la description : les placer dans le corps ou `references/`.

## Regle de blocage
Si une tache touche le metier et que la skill locale pertinente n'existe pas :
- ne pas coder silencieusement ;
- utiliser `aurora-domain-skill-factory` ;
- proposer la skill locale a creer ;
- attendre validation humaine.
