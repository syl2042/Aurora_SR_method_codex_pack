# SR_BOOTSTRAP — entree canonique SR 4

## Activation et autorite
Appliquer avant toute tache non triviale et apres nouvelle conversation, compact, resume ou handoff. Les conditions d'activation SR et les garanties ne changent pas. Les regles projet et les autorisations explicites priment; aucune procedure ne permet de reduire le perimetre valide.
Validation humaine stricte : avant mutation, verifier l'autorisation `je valide` et sa portee. Une passe validee autorise tous ses lots annonces; seules une extension, un gate rouge ou une decision humaine manquante imposent un arret. Preserver les exceptions explicites autorisees, dont BUILD-CYCLE-V2.

## Auto-reprise obligatoire / Reprise SR stricte
Chercher `python3 scripts/codex/find_next_session_prompt.py --root . --json` si present. Un chemin fourni explicitement prime (`--prompt`). En cas de plusieurs candidats sans choix explicite, signaler l'ambiguite et demander lequel reprendre; ne pas confondre mtime et tache active.
Annoncer `NEXT_SESSION_PROMPT detecte : <chemin>` apres selection. Lire le NEXT_SESSION_PROMPT pertinent et les contrats associes (sr_contract.json avant legacy), retrouver objectif, perimetre autorise, exigences ouvertes, decisions, preuves manquantes et prochaine action. Un simple `reprends` exige resume puis validation avant mutation. Un prompt de reprise ne constitue pas une autorisation nouvelle.
Ne charger les details que pour resoudre une question de la prochaine action. Apres compact, reverifier ce point d'entree et l'etat courant pertinent; un resume n'est pas preuve du code ou du runtime. Lire CURRENT_STATE si etat global requis, absence de reprise fiable ou contradiction. Conserver toutes les exigences ouvertes du parent.

## Routage obligatoire et progressif
Lire PROJECT_PROFILE pour les politiques effectives. Lire SKILL_DIGEST puis les seules skills declarees et selectionnees. Declaration dans task_plan; lire SKILL_MAP si la declaration n'est pas resolue par profil/digest. Un manque de skill metier declenche DOMAIN_EXPERTISE_BOOTSTRAP, pas une invention metier.
Avant action annoncer objectif, hypotheses, approche couvrant le scope, skills methode/metier (ou absence justifiee), digest, mode core/nexus_kg et verification. Memoire SR : existante / absente a creer / non creee car simple question.
Les anciennes listes de documents citees dans les procedures sont des destinations conditionnelles selon ce routeur, jamais une seconde checklist universelle. Les routes ci-dessous sont cumulatives; reevaluer apres toute decouverte. Un document absent ou un declencheur incertain ne vaut jamais gate vert : charger la procedure, verifier ou signaler le blocage. SR_ROUTES.json fournit les memes destinations aux outils. `python3 scripts/codex/sr_route_check.py --root . --events fact recommendation` retourne les sources pour des evenements explicitement identifies; ce calcul ne declare aucun gate vert et ne remplace pas la classification fondee sur les preuves.

| Evenement | Source a charger |
|---|---|
| Avant mutation ou action sensible | procedures/authority.md ; autorisation et perimetre |
| Fait verifiable dans une reponse non triviale | procedures/fact.md, puis source locale/officielle qui tranche |
| Recommandation technique ou plan engageant | procedures/evidence.md ; RepoMap/KG si navigation necessaire puis code/tests/logs |
| Creation/reprise de memoire avant mutation non triviale | procedures/memory.md et procedures/contracts.md ; cinq fichiers detail seulement pour leur contenu requis |
| Nouvelle demande, retour utilisateur, lot executable | procedures/design-evidence.md et procedures/execution.md ; Lot Design Evidence Gate, intake, scope/spec/security/architecture et limites d'autonomie |
| Fonction structurante / mutation backlog / dependances | procedures/impact.md ; Global Impact Gate, Backlog Mutation Gate, Lot Dependency Reconciliation, lots pertinents puis elargissement selon impact |
| Symbole, schema, API, config ou composant partage change | procedures/propagation.md avant ET apres mutation |
| UI significative | DESIGN.md, procedures/ui.md et skill UI ; Design Gate, UI Test Readiness Gate, UI Visual Evidence Gate |
| Plusieurs lots / passe | procedures/passes.md ; Pass Planning Gate, SR_PASSES et dependances |
| Passe executee avec /goal | procedures/runtime-goal.md ; Pass Runtime Goal et Goal Length Gate |
| Agent IA / LLM / prompt / RAG / outil runtime | AI_AGENT_RUNTIME_METHOD.md et procedures/skills.md |
| Domaine, workflow, donnees ou validation metier | DOMAIN_EXPERTISE_BOOTSTRAP.md, skill et sources domaine concernees |
| Apres patch / verification | procedures/verification.md ; tests proportionnes, diff, preuves et consommateurs |
| Cloture / changement de statut | procedures/completion.md et procedures/contracts.md ; Lot Completion Gate, Self Evaluation Gate, validateurs, memoire et propagation |
| Avancement significatif / cloture / risque de contexte | procedures/context.md ; context_budget_report.py --root . --compact, seuils legacy inchanges |
| Pause, handoff, prochaine conversation | procedures/resume.md et procedures/context.md ; prompt court, exigences ouvertes, contrats associes |

Charger les sources plus larges si la preuve, le risque ou une dependance l'exige. Ne pas reread une source comprise et inchangee dans le contexte courant; apres compact, verifier la reprise. Ni le cache ni une ancienne preuve ne dispensent de verifier un runtime ayant change.

## Cloture et continuite
Toute tache non triviale garde ses contrats et sa memoire. Mettre a jour uniquement les informations changees, sans recopier logs et historique dans chaque document. Les vues derivees ne creent jamais de preuve ni d'acceptation. CURRENT_STATE est mis a jour aux evenements prescrits dans completion; RepoMap si structure changee. Aucun `done` si gate requis rouge, implementation partielle ou preuve obligatoire manquante.
Annoncer resultat, preuves/limites, memoire mise a jour, E2E restant, decision de conversation et NEXT_SESSION_PROMPT cree/mis a jour/non requis. Question simple sans mutation ni investigation significative : reponse directe, memoire omissible.
