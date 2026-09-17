# Install SR 4.0.0 in a new target project

## SR 4.0.0 — published release

Target source: explicitly select `SR_PACK_SOURCE`, either an identified published release or the authorized local SR 4.0.0 candidate. Read `core/SR_PACK_VERSION.json` (`version`, `release_status`); record `source_commit`, Git state and, for a modified clone, a content fingerprint including the untracked source files used. Do not present an `unreleased` candidate as a release. Do not substitute a clone of the latest published release for the candidate; if the requested source is unavailable, stop and clarify before installing.

For this SR 4.0.0 target, the source must declare `version: 4.0.0`. If no 4.0.0 release is published, use only the authorized local candidate or report its absence; never silently install another version.

Preview with the command below before approval; after `je valide`, choose only the mode matching the path. `--plan-out` writes a local plan and requires authorization; `--apply-plan` rejects stale diagnostics. `--restore` is a separate operation using the exact transaction journal and rejects later edits. Never delete a file to bypass a conflict.

Saved plans contain file contents: keep them local. Set `SR_TARGET` to the target repository path.

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

You are working in a software repository that must receive Aurora SR Method for the first time.

Verifiable objective: install SR pack 4.0.0 and its target contracts (`sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4, `SR_PASSES` 0.2), verify the installation, then stop before application development.

Install `SR_PASSES.yaml` with `passes: []`. This empty registry is valid: a fresh install must not invent a product pass. Prompt `08` proposes passes later, after reading the lots and obtaining human validation.

Use only the official source: `https://github.com/syl2042/Aurora_SR_method_codex_pack`.

Strict rules:

- Do not change application code, migrations, dependencies, secrets, configuration, or business rules.
- Inspect the target repository and the nearest `AGENTS.md` before writing.
- If `docs/codex/SR_PACK_VERSION.json`, `docs/codex/SR_METHOD.md`, or `docs/codex/SR_LOTS.yaml` already exists, this is not a fresh install. Stop and use `05_upgrade_codex_environment.md`.
- Before mutation, report files to create, existing files to preserve, and planned checks; wait for the human validation required by the project.
- Do not invent `validated_requests`, validated lots, or executable passes. Templates are not validated product scope.
- Never use `--write` to update an existing SR project; use `--upgrade` only after a per-project audit.

After validation:

1. Identify a verified local clone of the official pack and record its source commit.
2. Classify the target as `fresh_install` by checking the SR markers above.
3. Run the installer with `--profile default --write`.
4. Verify `SR_PACK_VERSION.json`, `CHANGELOG.md`, `SR_LOTS.yaml`, `SR_PASSES.yaml`, task-memory templates, validators, and localized public prompts `01`, `05`, `06`, `07`, `08`, `09`, and `15`.
5. Confirm that `sr_contract.json` separates `implementation_status` from `evidence_status`, and includes granular `validated_requests`, lineage, closure, and a derived Completion Gate.
6. Run `audit_codex_pack.py`, `sr_post_install_check.py`, `validate_release_docs.py`, lot/pass validators, and the loop/SR template validators.
7. Verify Pass Runtime Goal and UI Verification Harness tooling. Keep `.playwright/.auth/` out of Git and request no credentials during installation.
8. Do not generate `/goal`. Recommend `09_define_sr_lots_from_scope.md`, then `08_define_sr_passes_from_lots.md`, and generate a goal only for a user-validated pass.
9. Report the `fresh_install` classification, target version, source commit, added/preserved files, passed/failed checks, warnings, and confirm that no application file changed.

Mandatory end: installing the method validates no product scope. Wait for an explicit user request before defining or executing application lots.

Paths: fresh installation `00 -> 06`; existing installation `05 -> 06 -> 07`. Prompt `06` only checks; `07` proposes realignment and waits for `je valide` before changing memory. Neither path authorizes application development.
