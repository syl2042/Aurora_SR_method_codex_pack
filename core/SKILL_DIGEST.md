# SKILL_DIGEST.md

## Objectif
Servir de routeur court pour choisir les skills sans charger tous les `SKILL.md`.

Ce digest ne remplace pas :
- `docs/codex/SKILL_MAP.md`, source de declaration des skills du projet ;
- `docs/codex/PROJECT_PROFILE.yaml`, source de politique SR ;
- les `SKILL.md`, qui restent la source finale quand une skill est selectionnee ;
- les docs domaine et les validations humaines.

## Lecture minimale
1. Lire `PROJECT_PROFILE.yaml` pour le mode connaissance et les obligations SR.
2. Lire `SKILL_MAP.md` pour les skills declarees.
3. Lire ce digest pour choisir les skills candidates.
4. Lire uniquement les `SKILL.md` selectionnes avant de coder.

## Skills methode globales

| Skill | Declencheur |
|---|---|
| `aurora-planning-with-files` | Tache non triviale, multi-fichiers, reprise, memoire SR. |
| `aurora-lot-runner` | Roadmap, gros brief, lot SR, reprise longue, phase autonome bornee. |
| `aurora-diagnose` | Bug, erreur runtime, test rouge, integration ou UI a diagnostiquer. |
| `aurora-tdd` | Fonction ou correction verifiable par test automatise raisonnable. |
| `aurora-review-diff` | Revue obligatoire avant cloture d'une tache non triviale. |
| `aurora-architecture-check` | Migration, modele DB, integration, orchestration IA, dependance ou refactor structurant. |
| `aurora-repomap-maintainer` | Route, endpoint, modele, migration, service, composant central ou script modifie. |
| `aurora-domain-skill-factory` | Projet sans skill metier pertinente ou creation de skill locale. |
| `aurora-terminal-token-optimizer` | Commandes longues, logs, tests, build, docker, grep ou diff volumineux. |
| `aurora-to-prd` | Besoin produit trop vague pour coder directement. |

## Skills metier Codex locales
Les skills metier restent locales par defaut dans :

```text
docs/codex/project-skills/
```

Avant toute tache touchant objets metier, donnees metier, workflow, ecran metier, integration verticale, agent IA ou validation humaine :
- verifier `PROJECT_PROFILE.yaml` et `SKILL_MAP.md` ;
- lire la skill locale pertinente si elle existe ;
- si aucune skill pertinente n'existe, utiliser `aurora-domain-skill-factory`, proposer la skill et attendre validation avant de coder.

Une skill metier locale doit rester declaree dans `SKILL_MAP.md` ou `PROJECT_PROFILE.yaml`. Une skill non declaree est interdite par defaut.

## Skills runtime applicatives
Les skills runtime des agents applicatifs ne sont pas des skills Codex globales. Avant de creer ou modifier un agent IA runtime, lire `docs/codex/AI_AGENT_RUNTIME_METHOD.md` et appliquer le pattern :

```text
prompt + variables + bindings controles + skills runtime + schema JSON + validation + traces + validation humaine
```

Ne jamais laisser un LLM generer puis executer librement du SQL.

## Garde-fous de selection
- Ne pas charger toutes les skills par securite.
- Ne pas exporter une skill metier vers `~/.codex/skills` sans decision explicite.
- Ne pas inventer de regle metier absente des sources.
- Pour un lot SR, declarer les skills dans `task_plan.md`.
- Le code, les tests et les logs priment sur ce digest.
