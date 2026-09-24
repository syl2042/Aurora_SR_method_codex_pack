# Repository Guidelines — {{PROJECT_NAME}}

- Follow the nearest `AGENTS.md`; project-local rules override this file.
- Reply in French unless the user asks otherwise.
- Preserve secrets, user data, local changes, persistent storage and rollback capacity.
- Before a non-trivial mutation, state the verifiable objective, assumptions, smallest sufficient approach and planned verification.
- Do not invent business rules or silently choose between plausible interpretations.
- Keep changes surgical. No unrelated dependency, refactor, migration, publication or external action.
- A task is complete only after proportionate final verification. Distinguish source, built artifact, active runtime, smoke, authenticated E2E and human acceptance.

<!-- AURORA_SR_PACK_START -->
## SR Method 4.1

- Load `docs/codex/SR_BOOTSTRAP.md` only for a non-trivial mutation, a multi-lot run or a resume. Simple questions and local edits do not require the full method.
- Use `docs/codex/SR_ROUTES.json` to load only the procedure triggered by the task. Re-evaluate routes only when a new fact changes the scope.
- When the user explicitly requires validation before mutation, wait for that validation. One validation covers the bounded pass; do not add micro-gates while scope and safety remain unchanged.
- Do not create a failing test or red gate on purpose. Verify the final result with the least expensive evidence that covers the risk.
- Roll back only an activated runtime that is genuinely degraded and has a verified recovery candidate.
- In `core` knowledge mode, do not load or call MCP. In `nexus_kg` mode, follow `docs/codex/MCP_POLICY.yaml` and use only resolved, allowed capabilities.
- Store task state only when continuity is useful. Prefer one compact `task_state.yaml`; legacy contracts remain readable but are not required for new V4.1 tasks.
- Keep raw logs and large artifacts outside model context; inject bounded summaries and stable paths.
<!-- AURORA_SR_PACK_END -->

## Conditional sources

- `DESIGN.md`: significant UI work.
- `docs/domain/`: relevant business rule only.
- `docs/codex/CODEBASE_MAP.md`: structural exploration when target files are unknown.
- `docs/CURRENT_STATE.md`: cross-cutting state, significant resume or conflict.
- `docs/codex/SKILL_DIGEST.md`: only when a specialized skill may apply.
