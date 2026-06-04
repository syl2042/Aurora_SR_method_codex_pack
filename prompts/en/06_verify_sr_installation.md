# Verify an SR Method installation

You are working in a repository equipped with the Aurora SR Method.

Objective: verify that the installation or upgrade is complete, coherent, and usable before development resumes.

Instructions:

1. Run `python3 scripts/codex/verify_codex_pack.py`.
2. Run `python3 scripts/codex/audit_codex_pack.py --root . --json`.
3. Run `python3 scripts/codex/sr_post_install_check.py --root . --json` if available.
4. Validate lot, loop, and SR contracts when the scripts are present.
5. Classify remaining warnings as acceptable, to document, to fix with validation, or blocking.
6. Report version, checks, errors, warnings, and recommended next action.

This is not an application development pass.
