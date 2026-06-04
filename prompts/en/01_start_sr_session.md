# Start a governed SR session

You are working in a repository equipped with the Aurora SR Method.

Objective: resume the project cleanly before any development work.

Instructions:

1. Read `AGENTS.md`.
2. Read `docs/codex/SR_BOOTSTRAP.md`.
3. Read `docs/CURRENT_STATE.md` if present.
4. Run `python3 scripts/codex/find_next_session_prompt.py --root . --json` if available.
5. If a `NEXT_SESSION_PROMPT.md` is found, read it before proposing work.
6. Check the SR version with `python3 scripts/codex/audit_codex_pack.py --root . --json` if available.
7. Summarize open lots, active decisions, blockers, and the recommended next action.

Do not code before this bootstrap is complete.
