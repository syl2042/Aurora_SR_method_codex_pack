# Define SR Lots From Scope Or Inbox

Objective: turn a framing note, user request, or `docs/codex/SR_INBOX.yaml` into explicit SR lots in `docs/codex/SR_LOTS.yaml`, without modifying application code.

Rules:

- Do not modify application code.
- Do not create a `planned`, `validated`, `in_progress`, or `reopened` lot without the Lot Design Evidence Gate.
- A `proposed` lot may remain exploratory.
- Never mark a lot `validated` without explicit user validation.

Method:

1. Read `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md`, `docs/codex/SR_HARNESS_METHOD.md`, `docs/codex/LOT_EXECUTION_METHOD.md`, `docs/CURRENT_STATE.md`, `docs/codex/SR_INBOX.yaml`, `docs/codex/SR_LOTS.yaml`, and `docs/codex/CODEBASE_MAP.md` when present.
2. Identify candidate surfaces through `RepoMap/KG -> candidate files -> real code reading -> tests/logs`.
3. Fill `design_evidence` for each candidate lot.
4. Keep any lot whose framing still depends on a verifiable assumption in `proposed`.
5. Propose the lots for validation before execution.
6. Validate `SR_LOTS.yaml` with `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml`.
7. Recommend `docs/codex/prompts/08_define_sr_passes_from_lots.md` next when several lots are executable or close to executable.

Expected output: lots created or modified, Lot Design Evidence Gate status, files read, remaining assumptions, blocking questions, `SR_LOTS.yaml` validation, next step.
