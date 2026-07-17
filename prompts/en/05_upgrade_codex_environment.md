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
5. Explain the upgrade plan and wait for explicit validation before mutation.
6. Apply the upgrade with the installer only after validation.
7. Run audit and validation scripts, including `validate_pass_contract.py` when `SR_PASSES.yaml` exists.
8. Report source commit, files upgraded, files preserved, backups, warnings, `SR_PASSES.yaml` status, and next steps.
9. Recommend `prompts/en/08_define_sr_passes_from_lots.md` when the project has multiple lots and no valid passes.

Do not modify application code, dependencies, migrations, or secrets.
