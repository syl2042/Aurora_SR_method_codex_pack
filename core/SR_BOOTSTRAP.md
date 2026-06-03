# SR_BOOTSTRAP.md

## Objectif
Garantir que Codex reprend systematiquement la methode SR apres nouvelle conversation, compact, resume, handoff ou changement de contexte.

## Declenchement obligatoire
Executer ce bootstrap mentalement et explicitement avant toute tache non triviale :
- debut de conversation dans un repo installe ;
- reprise apres compact ;
- reprise apres `resume` ou handoff ;
- demande multi-fichiers, metier, architecture, securite, agents IA, DB ou integration ;
- doute sur l'etat courant du projet.

## Sources a relire en premier
1. `AGENTS.md`
2. `docs/codex/PROJECT_PROFILE.yaml`
3. `docs/CURRENT_STATE.md`
4. `docs/codex/WORKFLOW_CODEX.md`
5. `docs/codex/SR_METHOD.md` si present
6. `docs/codex/SR_DEVELOPMENT_METHOD.md` si present
7. `docs/codex/SR_AGENT_METHOD.md` si present
8. `docs/codex/SKILL_MAP.md`
9. `docs/codex/SKILL_DIGEST.md` pour choisir les skills sans charger tous les `SKILL.md`
10. `docs/codex/CODEBASE_MAP.md`
11. `docs/codex/CODEBASE_MAP.generated.md` si present
12. `docs/codex/NEXUS_CONTEXT_PACK.md` ou context pack KG si `knowledge.mode: nexus_kg`
13. `docs/codex/AI_AGENT_RUNTIME_METHOD.md` si agents IA, LLM, prompts, tools ou orchestration
14. `docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md` si metier, donnees metier, workflow ou verticale
15. `docs/codex/SR_HARNESS_METHOD.md` et `docs/codex/LOT_EXECUTION_METHOD.md` si gros brief, roadmap, lots, reprise longue ou autonomie bornee

## Auto-reprise obligatoire

Au debut d'une conversation ou apres compact/resume, chercher automatiquement le dernier `NEXT_SESSION_PROMPT.md` :

```bash
python3 scripts/codex/find_next_session_prompt.py --root . --json
```

Si un prompt est detecte, le lire avant de proposer la suite et annoncer :

```text
NEXT_SESSION_PROMPT detecte : <chemin>
```

Si plusieurs prompts existent, lire le plus recent et signaler les autres comme candidats secondaires. Si aucun prompt n'existe, continuer avec les sources SR standard.

## Reprise SR stricte

Si l'utilisateur ouvre une nouvelle conversation et dit seulement `reprends`, `resume`, `continue`, `on reprend` ou une formule vague equivalente, Codex doit appliquer la reprise stricte :

1. executer `python3 scripts/codex/find_next_session_prompt.py --root . --json` ;
2. lire uniquement le dernier `NEXT_SESSION_PROMPT.md` detecte ;
3. lire le `loop_contract.json` associe si le prompt ou la task memory l'indique ;
   si un `sr_contract.json` SR 3.0.0 est indique ou present dans la meme memoire, le lire aussi avant les fichiers legacy ;
4. repondre avec l'etat precedent, les tests E2E utilisateur, le prochain lot recommande, les blockers et la decision attendue ;
5. ne pas coder ;
6. ne pas lancer le prochain lot ;
7. attendre une validation explicite.

Ne lire `SR_LOTS.yaml`, `CODEBASE_MAP.md`, les docs methode completes ou le code reel qu'apres validation utilisateur ou demande explicite de continuer. Cette regle reduit les tokens et evite de transformer une reprise vague en execution de lot.

## Rituel minimal avant action
Pour toute tache non triviale, Codex doit annoncer :
- objectif verifiable ;
- hypotheses retenues ;
- approche simple suffisante ;
- skills methode selectionnees ;
- skills metier Codex selectionnees ou raison de leur absence ;
- digest skills consulte ou raison de non-consultation ;
- mode connaissance detecte (`core` ou `nexus_kg`) ;
- methode de verification prevue.

## Validation humaine stricte

Quand un `AGENTS.md`, un lot, une reprise ou l'utilisateur active le mode strict, Codex peut analyser, lire et recommander sans validation, mais ne doit modifier aucun fichier ni lancer d'action de mutation tant que l'utilisateur n'a pas ecrit exactement `je valide`.

Cette validation ne couvre que l'action ou le plan decrit juste avant. Toute extension de perimetre, dependance, migration, configuration, donnees, agent IA runtime, backlog, publication Git, action destructive ou changement metier exige une nouvelle validation explicite.

Si la demande modifie un backlog de lots, Codex doit classer la demande et proposer la mise a jour de `SR_INBOX.yaml` ou `SR_LOTS.yaml` avant de coder.

Avant une recommandation technique engageante, appliquer le knowledge gate :

```text
RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs
```

## Fact Gate

Avant toute reponse non triviale, appliquer un gate deterministe sur les faits utilises dans la reponse.

Classification obligatoire :

- `opinion/methode` : conseil general, preference ou explication methodologique ; source locale non obligatoire ;
- `fait_verifiable` : affirmation sur un repo, produit, code, API, migration, flux UI, donnee, configuration, etat projet ou comportement existant ;
- `hypothese_non_verifiee` : piste utile mais non encore prouvee.

Regle :

- si une source locale ou officielle peut trancher un `fait_verifiable`, la lire avant de repondre ;
- si la source est accessible mais non lue, ne pas conclure et repondre `Fact Gate non satisfait : je dois verifier <source> avant de conclure.` ;
- si la verification est impossible ou disproportionnee, garder le statut `hypothese_non_verifiee` et indiquer la verification minimale ;
- les termes probabilistes ne remplacent jamais une preuve quand le repo, les logs, les fichiers SR ou la documentation officielle peuvent trancher.

Sources attendues :

- comportement applicatif : code reel, tests, logs, diff ;
- methode SR ou etat projet : fichiers SR, task memory, contrats, backlog, `CURRENT_STATE.md` ;
- API ou outil externe : documentation officielle ou source primaire ;
- donnees metier : source metier documentee ou validation humaine.

## Memoire de tache
Creer ou reprendre :

```text
docs/codex/tasks/YYYY-MM-DD_slug/
  sr_contract.json
  task_plan.md
  findings.md
  progress.md
  decisions.md
  verification.md
  loop_contract.json
```

En SR 3.0.0, `sr_contract.json` est la cible machine du lot. Il doit lister les intentions utilisateur validees dans `validated_requests` et etre valide avec :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Pendant la transition, les fichiers legacy restent crees ou maintenus si le projet les exige. Ne pas les supprimer sans lot de migration explicite.

Le `task_plan.md` doit contenir au minimum :
- objectif verifiable ;
- hypotheses ;
- sources lues ;
- skills utilisees ;
- fichiers candidats puis fichiers confirmes apres lecture ;
- risques ;
- plan court ;
- verification prevue.

## Budget contexte par iteration

Si `scripts/codex/context_budget_report.py` existe, l'executer avant chaque reponse de cloture ou d'avancement significatif :

```bash
python3 scripts/codex/context_budget_report.py --root . --compact
```

Cette commande exploite les evenements `token_count` Codex/OpenAI de la session locale : `last_token_usage`, `total_token_usage`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`, `model_context_window` et `rate_limits` quand ils sont disponibles. Ne jamais afficher le JSON complet sauf diagnostic.

Regle de sortie :
- `green` : ne rien afficher a l'utilisateur sauf s'il demande explicitement le statut contexte ;
- `yellow` : signaler sobrement qu'une reprise sera recommandee si la prochaine tache est longue ;
- `orange`, `red`, `unknown`, `stale` ou `ambiguous` : creer ou mettre a jour le `NEXT_SESSION_PROMPT.md` du lot courant avant de conclure et donner un prompt court avec le chemin explicite.

Prompt court recommande quand le chemin est connu :

```text
Reprise SR stricte. Projet : <chemin absolu du projet>. Lis docs/codex/tasks/YYYY-MM-DD_slug/NEXT_SESSION_PROMPT.md et les contrats associes. Resume l'etat, ne code pas avant validation.
```

## Regle compact/resume
Apres compact ou resume, ne pas supposer que le contexte precedent suffit.
Relire les sources SR ci-dessus et reprendre la derniere memoire de tache pertinente avant de modifier des fichiers.

Le statut hybride tient compte de `effective_context_percent`, `uncached_input_tokens`, `cache_ratio`, tours utilisateur et lots traites ; ne pas couper une conversation uniquement sur `input_total` ou `raw_context_percent` quand la majorite est cachee. `raw_context_percent` est un signal de diagnostic, pas un seuil de coupure autonome. Un statut `unknown`, `stale` ou `ambiguous` ne doit jamais etre traite comme `green`.

`NEXT_SESSION_PROMPT.md` n'est pas systematique. Il est obligatoire si :
- contexte `orange` ou `red` ;
- contexte `stale` ou `ambiguous` ;
- fin de batch multi-lots ou apres 2-3 lots dans la session ;
- pause longue ou arret annonce par l'utilisateur ;
- changement de macro-fonction ;
- upgrade SR ou realignement SR ;
- decision structurante importante ;
- prochain lot fortement dependant des decisions courantes.

Il est recommande si le contexte est `yellow` et que la prochaine tache est longue. Il n'est pas necessaire pour une question simple, une micro-correction ou une session courte en contexte `green`.

En cloture d'une tache non triviale, la decision doit etre visible dans `loop_contract.json` :

- `continue_current` : conversation saine, prochain lot court ou contexte green ;
- `recommend_new_conversation` : contexte yellow, fin de lot significatif, pause probable ou prochaine action longue ;
- `stop_for_new_conversation` : contexte orange/red, changement de macro-fonction risque, decisions nombreuses ou reprise fragile.

Si la decision est `recommend_new_conversation` ou `stop_for_new_conversation`, creer ou mettre a jour `NEXT_SESSION_PROMPT.md` et indiquer son chemin.
Le `loop_contract.json` doit aussi renseigner `resume_protocol` avec le prompt utilisateur exact a copier dans la prochaine conversation.

## Exceptions
Pour une question simple ou une commande ponctuelle sans modification, la memoire de tache peut etre omise. Si la demande devient multi-etapes, revenir au bootstrap complet.

## Cloture obligatoire
Avant de conclure une tache non triviale :
- completer `verification.md` ;
- creer ou mettre a jour `loop_contract.json` ;
- creer ou mettre a jour `sr_contract.json` si le projet declare SR 3.0.0 ;
- executer `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json` si le contrat existe ;
- executer `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json` si le script existe ;
- executer ou documenter la verification impossible ;
- appliquer le Self Evaluation Gate : objectif atteint, preuves suffisantes, risques, oublis possibles, statut `done/user_testing/repair/blocked` ;
- utiliser `aurora-review-diff` ;
- mettre a jour `docs/CURRENT_STATE.md` pour tout upgrade SR, realignement SR, changement de version SR, creation de `NEXT_SESSION_PROMPT.md`, modification structurante de `SR_LOTS.yaml`, lot applicatif significatif passe en `done` ou `user_testing`, ou fin de session significative ;
- indiquer si `docs/CURRENT_STATE.md` a ete mis a jour et pourquoi ;
- indiquer si `docs/codex/CODEBASE_MAP.md` doit etre mis a jour.
- indiquer `NEXT_SESSION_PROMPT.md : cree / mis a jour / non requis` avec la raison ;
- indiquer `Conversation : continuer ici / recommander nouvelle conversation / stopper pour nouvelle conversation`.
