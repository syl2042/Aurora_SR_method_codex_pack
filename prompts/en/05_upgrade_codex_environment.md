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
4. Explain the upgrade plan and wait for explicit validation before mutation.
5. Apply the upgrade with the installer only after validation.
6. Run audit and validation scripts.
7. Report source commit, files upgraded, files preserved, backups, warnings, and next steps.

Do not modify application code, dependencies, migrations, or secrets.
