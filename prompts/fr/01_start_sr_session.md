# Demarrer une session SR gouvernee

Tu travailles dans un repository equipe de la Aurora SR Method.

Objectif : reprendre proprement le projet avant tout developpement.

Instructions :

1. Lire `AGENTS.md`.
2. Lire `docs/codex/SR_BOOTSTRAP.md`.
3. Lire `docs/CURRENT_STATE.md` si present.
4. Lancer `python3 scripts/codex/find_next_session_prompt.py --root . --json` si disponible.
5. Si un `NEXT_SESSION_PROMPT.md` est trouve, le lire avant de proposer du travail.
6. Verifier la version SR avec `python3 scripts/codex/audit_codex_pack.py --root . --json` si disponible.
7. Resumer les lots ouverts, decisions actives, blockers et prochaine action recommandee.

Ne code pas avant la fin de ce bootstrap.
