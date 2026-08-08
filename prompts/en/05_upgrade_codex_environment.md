# Upgrade a project to the latest SR Method

You are working in a repository already equipped with an older Aurora SR Method version.

Objective: audit and upgrade the SR pack without changing application code or overwriting project-owned adaptations.

Use the official source package:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Instructions:

1. Detect the installed SR version.
2. Verify or clone the official source package.
3. Identify project-owned files to preserve: `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `docs/codex/tasks/`, project skills, and local decisions.
4. Preserve `SR_LOTS.yaml` and add `SR_PASSES.yaml` additively when missing, without automatically converting old lots or task memories.
5. Do not mass-convert old lots to add `design_evidence`; add the Lot Design Evidence Gate only to lots created, promoted, or resumed after upgrade.
6. Add Pass Runtime Goal tooling additively (`build_pass_runtime_goal.py`, `pass_runtime_goal.md` template, `sr_passes.pass_runtime_goal` options) without generating or launching `/goal` during upgrade.
7. Explain the upgrade plan and wait for explicit validation before mutation.
8. Apply the upgrade with the installer only after validation.
9. Run audit and validation scripts, including `validate_pass_contract.py` when `SR_PASSES.yaml` exists.
10. Verify the installed Goal Length Gate: `max_goal_command_chars: 1000`, `hard_limit: 4000`.
11. Update or recommend updating `docs/CURRENT_STATE.md` with before/after version, source commit, warnings, pass status, and next action.
12. Report source commit, files upgraded, files preserved, backups, warnings, `SR_PASSES.yaml` status, Pass Runtime Goal status, and next steps.
13. Recommend `prompts/07_realign_sr_state_after_upgrade.md` before any application development resumes.
14. Recommend `prompts/en/09_define_sr_lots_from_scope.md` to create or promote lots with the Lot Design Evidence Gate before execution.
15. Recommend `prompts/en/08_define_sr_passes_from_lots.md` when the project has multiple lots and no valid passes.
16. Recommend `build_pass_runtime_goal.py` only after realignment and validation of a `validated` or `in_progress` pass.

Do not modify application code, dependencies, migrations, or secrets.
