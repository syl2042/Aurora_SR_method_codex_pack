# SKILL_MAP.md — {{PROJECT_NAME}}

## Objectif
Aider Codex a selectionner les skills utiles sans charger tout le contexte.

Pour une selection rapide, lire aussi `docs/codex/SKILL_DIGEST.md` : il resume les declencheurs des skills methode, la politique des skills metier locales et la distinction avec les skills runtime.

## Regle
Ne jamais charger toutes les skills par securite. Declarer les skills dans `task_plan.md`.
Utiliser `SKILL_DIGEST.md` comme routeur court, puis lire uniquement les `SKILL.md` selectionnes.
Pour toute tache metier, selectionner au moins une skill metier Codex. Si aucune skill pertinente n'existe, utiliser `aurora-domain-skill-factory` et proposer la skill avant de coder.
Lire `docs/codex/PROJECT_SKILLS_POLICY.md` pour distinguer skills globales et skills locales.
Une skill projet non declaree dans ce fichier ou dans `PROJECT_PROFILE.yaml` est interdite par defaut. Une exception cross-project doit etre explicite dans `task_plan.md`.

## Skills methode
- `aurora-planning-with-files` : taches non triviales et memoire de tache.
- `aurora-diagnose` : debug avant correction.
- `aurora-tdd` : test-first pragmatique.
- `aurora-review-diff` : revue avant cloture.
- `aurora-to-prd` : besoin vague vers PRD.
- `aurora-architecture-check` : changements structurants.
- `aurora-repomap-maintainer` : maj RepoMap.
- `aurora-domain-skill-factory` : creation skills metier.
- `aurora-terminal-token-optimizer` : sorties terminal longues.
- `aurora-lot-runner` : orchestration SR Development Method, backlog vivant, gates, execution multi-lots bornee et Loop Contract.

## Skills metier Codex
A definir par projet apres `DOMAIN_EXPERTISE_BOOTSTRAP` :
- `codex-{project}-core` : objets, workflows et regles coeur.
- `codex-{project}-ui` : conventions UI metier et parcours.
- `codex-{project}-data` : modele de donnees, mappings, qualite.
- `codex-{project}-integration` : connecteurs, API, synchronisations.
- `codex-{project}-security` : permissions, donnees sensibles, actions critiques.
- `codex-{project}-agent-runtime` : agents IA applicatifs et skills runtime.

Stockage recommande :

```text
docs/codex/project-skills/codex-{project}-core/SKILL.md
docs/codex/project-skills/codex-{project}-ui/SKILL.md
docs/codex/project-skills/codex-{project}-agent-runtime/SKILL.md
```

Ces skills sont locales au projet par defaut. Si Codex ne les auto-decouvre pas, lire explicitement le fichier `SKILL.md` local indique ici avant de modifier le domaine concerne.

## Skills runtime
A distinguer des skills Codex : elles sont injectees dans les agents IA embarques dans l'application.
Lire `docs/codex/AI_AGENT_RUNTIME_METHOD.md` avant toute creation ou modification d'agent runtime.

## SR Development Method
Pour gros brief, roadmap, reprise longue, phase autonome ou demande multi-lots :
- lire `docs/codex/SR_METHOD.md` et `docs/codex/SR_DEVELOPMENT_METHOD.md` si presents ;
- lire `docs/codex/SR_HARNESS_METHOD.md` ;
- lire `docs/codex/LOT_EXECUTION_METHOD.md` ;
- utiliser `aurora-lot-runner` ;
- maintenir `docs/codex/SR_INBOX.yaml` et `docs/codex/SR_LOTS.yaml`.
- produire et valider `docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json` pour toute tache non triviale.

## Knowledge mode

- `core` : utiliser RepoMap puis lecture ciblee du code.
- `nexus_kg` : utiliser RepoMap + Nexus KG, puis lecture ciblee du code.

Le KG et RepoMap orientent; ils ne remplacent pas le code reel ni les tests.
