# Repository Guidelines — {{PROJECT_NAME}}

## SR Bootstrap obligatoire
- Au debut de chaque nouvelle conversation, apres compact, apres resume ou apres handoff, relire `docs/codex/SR_BOOTSTRAP.md` avant toute tache non triviale.
- Pour une tache non triviale, annoncer l'objectif verifiable, les hypotheses, l'approche simple suffisante, les skills selectionnees et la verification prevue avant de coder.
- Si le contexte precedent semble connu, verifier quand meme `docs/CURRENT_STATE.md` et la derniere memoire de tache pertinente.
- Au demarrage ou apres compact/resume, chercher le dernier `NEXT_SESSION_PROMPT.md` avec `python3 scripts/codex/find_next_session_prompt.py --root . --json` si disponible, puis le lire s'il existe.
- Si l'utilisateur dit seulement `reprends`, `resume`, `continue` ou une formule vague equivalente apres une nouvelle conversation, appliquer `Reprise SR stricte` : lire uniquement le dernier `NEXT_SESSION_PROMPT.md`, le `sr_contract.json` et le `loop_contract.json` associes si indiques, resumer, ne pas coder, ne pas lancer le lot suivant, attendre validation.
- Annoncer systematiquement le statut de memoire sous la forme : `Memoire SR : existante / absente a creer / non creee car simple question`.
- Avant toute reponse non triviale qui affirme un fait verifiable sur l'existant, appliquer le Fact Gate : si une source locale ou officielle peut trancher, la lire avant de conclure ; sinon marquer explicitement l'element comme hypothese non verifiee et indiquer la verification minimale.
- Avant toute reponse de cloture ou d'avancement significatif, executer `python3 scripts/codex/context_budget_report.py --root . --compact` si disponible. Si le statut est `green`, ne pas l'afficher ; sinon appliquer le Context budget gate.
- En fin de tache non triviale, indiquer la memoire SR utilisee, les fichiers SR mis a jour, les gates, les tests E2E utilisateur a faire et le prochain lot recommande.
- En fin de tache non triviale, indiquer `NEXT_SESSION_PROMPT.md : cree / mis a jour / non requis` avec la raison.
- SR plein regime : mettre a jour `docs/CURRENT_STATE.md` apres tout upgrade SR, realignement SR, changement de version SR, creation de `NEXT_SESSION_PROMPT.md`, modification structurante de `SR_LOTS.yaml`, lot applicatif significatif passe en `done` ou `user_testing`, ou fin de session significative.
- SR Contract 3.0.0 : creer ou mettre a jour `docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json` quand `PROJECT_PROFILE.yaml` declare `require_sr_contract`, suivre `validated_requests`, puis verifier avec `python3 scripts/codex/validate_sr_contract.py --file <chemin>`.
- Loop Contract obligatoire pour toute tache non triviale : creer ou mettre a jour `docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json`, declarer `conversation_transition`, puis verifier avec `python3 scripts/codex/validate_loop_contract.py --file <chemin>`.
- Backlog Contract obligatoire : si `docs/codex/SR_LOTS.yaml` est modifie, executer `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` avant cloture. `git diff --check` ne remplace jamais cette validation.
- Backlog Mutation Gate obligatoire : si une demande, une decouverte ou une reparation introduit une fonction structurante ou un impact durable, ne pas la traiter comme un simple detail du lot courant. Classer l'evenement, analyser les implications globales, puis mettre a jour `SR_INBOX.yaml` ou `SR_LOTS.yaml`, ou documenter explicitement pourquoi aucune mutation de backlog n'est requise.
- Global Impact Gate obligatoire : avant de cadrer ou coder une fonction structurante, analyser son impact sur le produit global, les parcours, donnees, permissions, API/services, UI, tests, lots existants, dependances, migrations et risques. Cette analyse doit rester agnostique du domaine et s'appliquer a toute fonction transversale.
- Cloture standard de lot : `Ce qui est fait`, `Resultat observe`, `Lecture expert / produit`, `Verifications executees`, `Memoire SR`, `Tests E2E utilisateur`, `Prochaine etape`.

## Mission
- Repo Auroramind. Codex travaille comme agent de developpement encadre.
- Ne pas coder si le besoin, les risques ou les sources de verite ne sont pas clairs.

## Non-negotiable rules
- Repondre en francais sauf demande contraire.
- Ne jamais afficher, committer ou documenter de secrets.
- Ne jamais exposer tokens serveur, cles API, credentials ou donnees sensibles cote frontend/logs/docs.
- Validation humaine stricte : Codex peut analyser sans validation, mais ne modifie aucun fichier et ne lance aucune action de mutation tant que l'utilisateur n'a pas ecrit exactement `je valide`; cette validation ne couvre que le perimetre decrit juste avant.
- Pas de dependance, migration, connecteur externe, webhook, cron, upload ou relaxation CORS sans validation.
- Ne pas inventer de regle metier non documentee.
- Le code reel prime sur la documentation ; noter les ecarts dans `findings.md`.
- Ne pas proposer une recommandation technique, un plan engageant ou une prochaine etape si les fichiers verifiables peuvent trancher et n'ont pas ete lus.

## Source of truth
- `AGENTS.md` : garde-fous.
- `DESIGN.md` : UI.
- `docs/CURRENT_STATE.md` : reprise projet.
- `docs/codex/PROJECT_PROFILE.yaml` : profil projet.
- `docs/codex/SKILL_MAP.md` : selection skills.
- `docs/codex/SKILL_DIGEST.md` : routeur court pour choisir les skills sans tout charger.
- `docs/codex/WORKFLOW_CODEX.md` : methode detaillee.
- `docs/codex/SR_BOOTSTRAP.md` : reprise obligatoire apres compact/resume.
- `docs/codex/SR_METHOD.md` : definition publique de la Specification Runtime Method.
- `docs/codex/SR_DEVELOPMENT_METHOD.md` : methode de cadrage du developpement assiste par IA.
- `docs/codex/SR_AGENT_METHOD.md` : methode de conception des agents IA runtime.
- `docs/codex/CODEBASE_MAP.md` : carte code courte.
- `docs/codex/CODEBASE_MAP.generated.md` : carte code generee.
- `docs/codex/AI_AGENT_RUNTIME_METHOD.md` : methode de conception des agents IA applicatifs.
- `docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md` : creation et usage des skills metier Codex.
- `docs/codex/PROJECT_SKILLS_POLICY.md` : politique skills globales vs skills projet locales.
- `docs/domain/` : metier.
- `docs/adr/` : decisions.

## Skill selection
Declarer les skills dans `task_plan.md` avant toute tache non triviale. Utiliser `docs/codex/SKILL_DIGEST.md` comme routeur court, puis lire uniquement les `SKILL.md` selectionnes.
Skills methode disponibles : voir `docs/codex/SKILL_DIGEST.md` et `docs/codex/SKILL_MAP.md`.

Pour une roadmap, un gros brief, plusieurs lots, une reprise longue, une phase autonome bornee, ou une nouvelle fonction non triviale, utiliser `aurora-lot-runner`.

Pour toute tache touchant le metier, les donnees metier, un workflow, un ecran metier, une integration verticale, un agent IA ou une validation humaine, selectionner au moins une skill metier Codex. Si aucune skill pertinente n'existe, s'arreter et proposer sa creation.
Les skills metier Codex sont locales au projet par defaut dans `docs/codex/project-skills/`; lire la skill locale pertinente explicitement si elle n'est pas auto-decouverte par Codex.

## SR-Harness lots
Pour toute demande qui modifie le backlog, lire `docs/codex/SR_HARNESS_METHOD.md`, `docs/codex/LOT_EXECUTION_METHOD.md`, `docs/codex/SR_LOTS.yaml` et `docs/codex/SR_INBOX.yaml`.

Politique par defaut :
- traiter les lots `reopened` puis `validated` ;
- enchainer jusqu'a 3 lots par passe si les gates restent verts ;
- stopper sur gate rouge, migration ambigue, dependance, regle metier absente, action sensible, test bloquant ou contexte a risque ;
- mettre a jour `SR_LOTS.yaml` apres chaque decision de statut ;
- valider `SR_LOTS.yaml` avec `validate_lot_contract.py` apres toute modification du backlog ;
- passer en `user_testing` si un test reel utilisateur est necessaire.
- quand une nouvelle fonction structurante apparait, appliquer `Global Impact Gate` puis `Lot Dependency Reconciliation` avant codage significatif ;
- classer les lots existants pertinents comme `unaffected`, `impacted`, `blocked_by`, `reopened`, `superseded`, `split_required` ou `depends_on` ;
- consigner le resultat dans `backlog_mutation_gate`, `global_impact_gate`, `SR_INBOX.yaml`, `SR_LOTS.yaml` ou le gate report.

Evidence gate obligatoire avant recommandation :
- suivre la chaine `RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs` ;
- citer les fichiers ou sources lus ;
- distinguer `verifie`, `hypotheses restantes` et `questions bloquantes` ;
- si une verification locale est possible, la faire avant de repondre.

Fact Gate obligatoire avant conclusion factuelle :
- classer la reponse attendue : `opinion/methode`, `fait_verifiable` ou `hypothese_non_verifiee` ;
- pour tout `fait_verifiable` sur un repo, produit, API, migration, flux UI, donnee, configuration ou comportement existant, lire la source disponible avant de repondre ;
- si la source est accessible mais non lue, ne pas conclure et annoncer `Fact Gate non satisfait` avec la source a verifier ;
- si la verification est impossible ou disproportionnee, repondre uniquement sous forme d'hypothese non verifiee avec la verification minimale ;
- les formulations de probabilite ne remplacent jamais une preuve quand les sources peuvent trancher.

Context budget gate obligatoire :
- executer `python3 scripts/codex/context_budget_report.py --root . --compact` si disponible avant chaque reponse de cloture ou d'avancement significatif ;
- si le statut est `green`, ne rien dire a l'utilisateur sauf besoin de verification explicite ;
- si le statut est `yellow`, signaler sobrement qu'une reprise sera recommandee si la prochaine tache est longue ;
- si le statut est `orange`, `red`, `stale`, `ambiguous` ou `unknown`, creer ou mettre a jour le `NEXT_SESSION_PROMPT.md` du lot courant et donner un prompt court avec son chemin explicite ;
- apres 2 lots, 20 tours utilisateur, une session longue, un changement de macro-fonction ou un risque de perte de contexte, creer ou mettre a jour `NEXT_SESSION_PROMPT.md` ;
- en cloture, declarer dans `loop_contract.json` la decision `conversation_transition` : `continue_current`, `recommend_new_conversation` ou `stop_for_new_conversation` ;
- recommander un handoff si la prochaine action depend fortement de decisions anterieures.

Self Evaluation Gate obligatoire :
- apres patch, relire le diff et les fichiers critiques modifies ;
- verifier l'objectif initial, les preuves, les risques restants et ce qui aurait pu etre oublie ;
- decider explicitement `done`, `user_testing`, `repair` ou `blocked`.

Loop Contract obligatoire :
- pour toute tache non triviale, creer ou mettre a jour `loop_contract.json` dans la memoire de tache ;
- si `status_decision: user_testing`, fournir une vraie liste `e2e_user_tests.items`, pas une simple mention d'attente E2E ;
- si du code applicatif change, declarer `changed_files` et les verifications executees ou la raison de non-execution ;
- declarer `conversation_transition` pour dire clairement si la prochaine action peut rester dans la conversation courante ou doit partir dans une nouvelle conversation ;
- declarer `resume_protocol` si une nouvelle conversation est recommandee ou imposee, avec le prompt exact a donner a l'utilisateur ;
- valider avec `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json`.

## Knowledge mode
Mode par defaut sans Nexus : `SR Core = RepoMap only`.
Mode avec Nexus : `SR Nexus = RepoMap + Nexus KG`.
RepoMap est obligatoire dans les deux modes. Nexus KG oriente et construit le context pack quand disponible, mais le code reel et les tests restent la source finale.

## Agents IA runtime
Avant de creer ou modifier un agent IA applicatif, lire `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
Pattern obligatoire : prompt + variables + bindings SQL/Nexus controles + skills runtime + output JSON schema + validation + traces + validation humaine si action critique.
Ne jamais laisser un LLM generer puis executer librement du SQL.

## Planning with files
Pour toute tache non triviale, creer/mettre a jour :
```text
docs/codex/tasks/YYYY-MM-DD_slug/task_plan.md
docs/codex/tasks/YYYY-MM-DD_slug/findings.md
docs/codex/tasks/YYYY-MM-DD_slug/progress.md
docs/codex/tasks/YYYY-MM-DD_slug/decisions.md
docs/codex/tasks/YYYY-MM-DD_slug/verification.md
docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
```

## RepoMap
Lire `docs/codex/CODEBASE_MAP.md` avant tache multi-fichiers ou reprise. Consulter le generated seulement si besoin.
Si Nexus KG est active dans `PROJECT_PROFILE.yaml`, consulter le KG avant de choisir les fichiers candidats et indiquer si le KG doit etre mis a jour en cloture.

## Verification
Une tache n'est terminee que si la verification pertinente est executee ou l'impossibilite documentee.
Tests E2E utilisateur :
Pour tout lot livre, fournir aussi la liste courte des tests E2E utilisateur a effectuer, meme si les tests automatises sont verts.

## Continuity rule
Cloture obligatoire : memoire SR, lots traites, gates, fait, fichiers modifies, verifications, tests E2E utilisateur, risques, decisions, prochaine etape, CURRENT_STATE a mettre a jour, RepoMap a mettre a jour.
Si `SR_LOTS.yaml` a ete modifie, inclure explicitement le resultat de `validate_lot_contract.py`.
