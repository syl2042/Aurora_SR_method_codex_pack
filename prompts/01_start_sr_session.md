# Demarrer une session SR

Tu travailles dans un repo Auroramind equipe de la SR Method.

Objectif : reprendre proprement le projet sans perdre le backlog, les decisions et les lots ouverts.

Ne code pas avant d'avoir fait ce bootstrap.

Fast path obligatoire : Reprise SR stricte
si la demande utilisateur est seulement `reprends`, `resume`, `continue`, `on reprend` ou une formule vague equivalente, ne lis pas tout le projet. Execute `find_next_session_prompt.py`, lis uniquement le dernier `NEXT_SESSION_PROMPT.md`, son `sr_contract.json` SR 3.0.0 et son `loop_contract.json` associes si indiques, puis resume l'etat et attends validation. Ne code pas et ne lance pas le prochain lot.

Etapes :

1. Lire `AGENTS.md`.
2. Lire `docs/codex/SR_BOOTSTRAP.md`.
3. Lire `docs/codex/SR_METHOD.md`, `docs/codex/SR_DEVELOPMENT_METHOD.md` et `docs/codex/SR_AGENT_METHOD.md` si presents.
4. Lire `docs/codex/SR_HARNESS_METHOD.md` si present.
5. Lire `docs/CURRENT_STATE.md`.
6. Lire `docs/codex/SR_LOTS.yaml` et `docs/codex/SR_INBOX.yaml` si presents.
7. Lire `docs/codex/SR_CONTEXT_PACK.md` si present.
8. Lire `docs/codex/SKILL_MAP.md`.
9. Lire `docs/codex/CODEBASE_MAP.md` et `docs/codex/CODEBASE_MAP.generated.md` si presents.
10. Si le profil indique `knowledge.mode: nexus_kg`, lire le context pack Nexus/KG disponible avant toute proposition technique.
11. Chercher automatiquement le dernier prompt de reprise avec `python3 scripts/codex/find_next_session_prompt.py --root . --json` si le script existe.
12. Si un `NEXT_SESSION_PROMPT.md` est detecte, le lire avant de proposer la suite.
13. Verifier rapidement la version SR avec `python3 scripts/codex/audit_codex_pack.py` si le script existe.
14. Verifier le contrat projet avec `python3 scripts/codex/audit_sr_project.py --root .` si le script existe.
15. Verifier la disponibilite du Loop Contract avec `test -f docs/codex/tasks/_TEMPLATE/loop_contract.json && test -f scripts/codex/validate_loop_contract.py`.
16. Verifier la disponibilite du SR Contract 3.0.0 avec `test -f docs/codex/tasks/_TEMPLATE/sr_contract.json && test -f scripts/codex/validate_sr_contract.py`.
17. Verifier le budget contexte avec `python3 scripts/codex/context_budget_report.py --root . --compact` si le script existe. Si le statut est `green`, ne pas l'afficher sauf demande explicite ; sinon appliquer le Context budget gate.
18. Pour toute tache non triviale reprise dans cette conversation, prevoir `sr_contract.json` avec `validated_requests` et une decision finale `conversation_transition` dans `loop_contract.json`.
19. Si une nouvelle conversation est recommandee ou imposee, verifier que `resume_protocol.next_user_prompt` existe dans le contrat de boucle.

Puis repondre avec :

- objectif courant detecte ;
- lots ouverts/reopened/user_testing ;
- decisions actives ;
- `NEXT_SESSION_PROMPT.md` detecte ou absent ;
- mode connaissance detecte : `core` ou `nexus_kg` ;
- etat court du budget contexte seulement s'il n'est pas `green` ou si l'utilisateur le demande ;
- etat court du SR Contract 3.0.0 si une task memory active existe ;
- regle de transition conversationnelle applicable : continuer ici / recommander nouvelle conversation / stopper si contexte orange ou rouge ;
- protocole de reprise applicable : strict_resume / resume_and_continue / non requis ;
- risques ou blockers ;
- prochaine action recommandee ;
- skills a utiliser.

Si ma demande modifie le backlog, classer la demande et proposer la mise a jour `SR_INBOX.yaml` ou `SR_LOTS.yaml` avant de coder.

Si tu codes ensuite, applique la boucle SR : knowledge gate, evidence gate, patch, tests, self evaluation gate, gate report, tests E2E utilisateur a faire.

Pour toute tache non triviale, cree ou mets a jour `sr_contract.json` et `loop_contract.json` dans la memoire de tache, puis valide-les avec `validate_sr_contract.py` et `validate_loop_contract.py`.

Avant toute reponse de cloture ou d'avancement significatif, relancer `context_budget_report.py --root . --compact`. En cas de statut `orange`, `red`, `unknown`, `stale` ou `ambiguous`, mettre a jour le `NEXT_SESSION_PROMPT.md` du lot courant et donner un prompt court avec son chemin explicite.
