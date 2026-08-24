# Verify an SR Method installation

Do not modify files.

Objective: prove that each installation or upgrade is complete, coherent, and usable before application development resumes.

For every target repository independently:

1. Read its actual `AGENTS.md`, `docs/codex/SR_PACK_VERSION.json`, method, contracts, lots, passes, and task-memory markers. Do not infer one folder's version from another.
2. Run `python3 scripts/codex/verify_codex_pack.py`.
3. Run `python3 scripts/codex/validate_release_docs.py --root . --json`.
4. Run `python3 scripts/codex/audit_codex_pack.py --root . --json`.
5. Run `python3 scripts/codex/sr_post_install_check.py --root . --json`.
6. Run `python3 scripts/codex/audit_sr_task_contracts.py --root . --json`.
7. Validate `SR_LOTS.yaml`, `SR_PASSES.yaml`, active loop contracts, and the SR Contract 3.1.0 (or explicitly identified legacy 3.0.0 contracts).
8. Verify `docs/codex/CHANGELOG.md`, the target version, localized public prompts, and additive preservation of project-owned files.

Classify every warning as compatible legacy state, documentation debt, `repair`, or a real external blocker. Installer exit code `0` alone is not sufficient.

Report a per-repository table with version, checks, errors, warnings, contract status, open `validated_requests`, missing evidence, and next action. `user_testing` is allowed only for technically complete work; missing implementation remains `repair`.

Stop without applying fixes. Ask for exact validation for any repair scope.
