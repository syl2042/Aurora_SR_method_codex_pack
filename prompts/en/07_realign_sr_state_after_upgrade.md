# Realign SR state after an upgrade

## SR 4.0.0 — published release

Start read-only. Reopening lots and updating memory below are proposals until exact `je valide` approval of the realignment scope; apply them only within that scope afterwards. Installation approval does not authorize application repairs.

Do not modify application code.

Objective: reconcile SR memory with the code and the complete previously validated scope before development resumes.

Read `AGENTS.md`, then `docs/codex/SR_BOOTSTRAP.md`. Run `python3 scripts/codex/find_next_session_prompt.py --root . --json`: use `selected`; if `ambiguous`, ask for the path and use `--prompt`. Never choose `latest` by date alone. Read the selected `NEXT_SESSION_PROMPT.md` and associated `sr_contract.json`/`loop_contract.json`, retaining all inherited open `validated_requests`. Without a handoff, inventory open lots and propose the scope. This post-upgrade realignment also requires `docs/CURRENT_STATE.md` and lot/pass registries to identify global discrepancies. Then load only detailed memories, procedures, RepoMap/KG and code/tests needed for the relevant lots; expand when evidence, a gate or a dependency requires it.

1. Run the pack, release-documentation, post-install, project, and task-contract audits.
2. Inventory every entry in `validated_requests` and retain its stable requirement ID, original lot/pass, `implementation_status`, `evidence_status`, missing tests, and feedback history.
3. Reopen the original lot when a validated requirement is missing, partial, defective, regressed, or contradicted by user feedback.
4. Reload the entire open checklist of that lot and pass; do not isolate only the latest defect.
5. Apply strict states:
   - `done`: implementation and required evidence are complete;
   - `user_testing`: technical implementation is complete and only real E2E or human acceptance remains;
   - `repair`: at least one implementation is absent, partial, defective, or failed;
   - `blocked`: a real unavailable authority, access, secret, decision, or external change prevents execution.
6. Keep code/build/runtime/E2E/deployment evidence separate but attached to the same persistent requirement.
7. Update `CURRENT_STATE.md` and the active task memory only after evidence supports the new state.

Start the report with `User request | State | Evidence | Remaining work`, list reopened lots and missing evidence, then propose one consolidated repair scope. Do not create a new lot unless the request is truly outside existing validated scope.

Stop and request exact human validation before mutation.

Paths: fresh installation `00 -> 06`; existing installation `05 -> 06 -> 07`. Prompt `06` only checks; `07` proposes realignment and waits for `je valide` before changing memory. Neither path authorizes application development.
