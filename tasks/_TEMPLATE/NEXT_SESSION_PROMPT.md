# NEXT_SESSION_PROMPT

## Role

Ce fichier est un point de reprise court. Il peut etre colle dans une nouvelle conversation, mais la SR Method demande aussi a Codex de le detecter automatiquement au demarrage avec :

```bash
python3 scripts/codex/find_next_session_prompt.py --root . --json
```

Ne pas creer ce fichier pour chaque micro-tache. Le creer ou le rafraichir quand le risque de perte de contexte devient reel : contexte orange/rouge, pause utilisateur, fin de batch multi-lots, changement de macro-fonction, upgrade, realignement ou decision structurante.

## Prompt a copier dans la prochaine conversation

Utiliser ce prompt apres un stop contexte `orange`, `red`, `unknown`, `stale` ou `ambiguous`, sauf si l'utilisateur veut explicitement continuer le developpement. Le chemin du `NEXT_SESSION_PROMPT.md` est toujours connu : le preciser dans le prompt.

```text
Reprise SR stricte. Projet : <chemin absolu du projet>. Lis docs/codex/tasks/YYYY-MM-DD_slug/NEXT_SESSION_PROMPT.md et les contrats associes. Resume l'etat, ne code pas avant validation.
```

Si l'utilisateur ecrit seulement `reprends`, `resume`, `continue` ou une phrase vague apres une nouvelle conversation, appliquer ce mode `Reprise SR stricte` par defaut.

## A lire par Codex dans une nouvelle conversation

```text
Reprends cette session avec la methode SR-Harness.

Lis dans cet ordre :
1. AGENTS.md
2. docs/codex/SR_BOOTSTRAP.md
3. docs/codex/SR_HARNESS_METHOD.md
4. docs/CURRENT_STATE.md
5. docs/codex/SR_LOTS.yaml
6. docs/codex/CODEBASE_MAP.md
7. docs/codex/SR_CONTEXT_PACK.md si present
8. Nexus KG/context pack si le projet est en mode nexus_kg
9. La task memory indiquee ci-dessous

Task memory a reprendre :
- docs/codex/tasks/YYYY-MM-DD_slug/

Contexte court :
- objectif courant :
- lots ouverts :
- decisions actives :
- interdits :
- prochaine action recommandee :

Avant de coder :
- si la demande utilisateur est vague (`reprends`, `resume`, `continue`), appliquer `Reprise SR stricte` : lire ce fichier, resumer, puis attendre validation ;
- appliquer evidence_gate ;
- appliquer knowledge_gate : RepoMap/KG -> fichiers candidats -> lecture code reel ;
- mettre a jour SR_INBOX/SR_LOTS si ma demande modifie le backlog ;
- demander validation si le lot est seulement proposed/planned ou si une action sensible apparait.
- utiliser aurora-lot-runner si plusieurs lots sont ouverts ;
- traiter jusqu'a 3 lots reopened/validated si les gates restent verts ;
- executer `context_budget_report.py --root . --compact` avant toute reponse de cloture ou d'avancement significatif ; ne rien afficher si le statut est `green` ;
- appliquer self_evaluation_gate apres patch ;
- donner les tests E2E utilisateur apres chaque lot livre.
```

## Notes de reprise

-
