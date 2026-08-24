# Start a governed SR session

Do not code.

Objective: reconstruct the complete validated scope and propose the next coherent action before any mutation.

1. Read `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md`, and `docs/CURRENT_STATE.md` when present.
2. Run `python3 scripts/codex/find_next_session_prompt.py --root . --json` and read the latest `NEXT_SESSION_PROMPT.md` when found.
3. Read the linked `sr_contract.json` (SR Contract 3.1.0 or legacy 3.0.0), `loop_contract.json`, task memory, lots, and passes needed to understand open work.
4. Reload every inherited open entry in `validated_requests`; never resume from only the most recent feedback item.
5. Separate requirements that are done, partial, not done, defective, blocked, or awaiting evidence.
6. Apply the status semantics: incomplete implementation means `repair`; `user_testing` requires complete technical implementation and only real E2E or human acceptance remaining.
7. If feedback concerns an existing requirement, reopen the original lot by default and present its consolidated checklist. Do not create a new micro-lot.
8. Run available contract and context-budget checks without mutating project state.

Report:

- SR version and memory used;
- validated requests and their implementation/evidence state;
- reopened lots, blockers, and missing evidence;
- the next coherent scope;
- the exact human validation required before coding.

Stop and wait for validation.
