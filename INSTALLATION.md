# Installation

## SR 4.0.0 — published release

Target source: explicitly select `SR_PACK_SOURCE`, either an identified published release or the authorized local SR 4.0.0 candidate. Read `core/SR_PACK_VERSION.json` (`version`, `release_status`); record `source_commit`, Git state and, for a modified clone, a content fingerprint including the untracked source files used. Do not present an `unreleased` candidate as a release. Do not substitute a clone of the latest published release for the candidate; if the requested source is unavailable, stop and clarify before installing.

For this SR 4.0.0 target, the source must declare `version: 4.0.0`. If no 4.0.0 release is published, use only the authorized local candidate or report its absence; never silently install another version.

Paths: fresh installation `00 -> 06`; existing installation `05 -> 06 -> 07`. Prompt `06` only checks; `07` proposes realignment and waits for `je valide` before changing memory. Neither path authorizes application development.

SR 4 loads procedures on demand through `SR_BOOTSTRAP.md` and `SR_ROUTES.json`. Gates, HITL, open requirements and contract schemas remain preserved. The pack version does not force conversion of old contracts.

### First installation
Inspect local rules; obtain `je valide` for the scope; preview, apply `--write`, then verify. Existing project files are preserved or explicitly merged. Application code is outside this operation.

### Version-agnostic upgrade
Use `--upgrade` after inspecting actual files. The previous release number is informational, never a prerequisite. Old, unversioned, partial and mixed installations are classified by content. Unknown/customized pack files block replacement: do not delete them to bypass the conflict. Review and authorize reconciliation. Preserve old contracts, open lots, task memories, handoffs and domain skills.

Preview is read-only unless `--plan-out` is explicitly requested. Saved plans contain file contents; keep them local. `--apply-plan` rejects changes made after preview. Transactions back up changed files; `--restore` refuses to overwrite later edits. Never force an upgrade with `--write`. Writing the target version is not installation success: the postcheck must pass.

Preview with the command below before approval; after `je valide`, choose only the mode matching the path. `--plan-out` writes a local plan and requires authorization; `--apply-plan` rejects stale diagnostics. `--restore` is a separate operation using the exact transaction journal and rejects later edits. Never delete a file to bypass a conflict.

Preview only:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Fresh installation after approval:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --write
```

Existing installation after approval:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

Verification only:

```bash
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Optional local plan after authorization:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --plan-out "$SR_PLAN_FILE"
```

Apply the approved plan, an alternative to direct commands:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --apply-plan "$SR_PLAN_FILE"
```

Separate restoration, only when needed and authorized:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --restore "$SR_JOURNAL_FILE"
```


[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

Official repository:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

The preferred workflow is **Codex prompt first**. The Python scripts are implementation and validation tools that Codex can run after reading the prompt and inspecting the target project.

## Choose The Correct Path First

| Target state | Prompt | Installer mode | Required behavior |
|---|---|---|---|
| No SR marker | `00_install_codex_environment` | `--write` | Install SR 4.0.0 directly |
| Any existing or partial SR marker | `05_upgrade_codex_environment` | `--upgrade` | Audit and merge additively |
| Several repositories, possibly different versions | `05_upgrade_codex_environment` | one `--upgrade` per repository | Produce a per-repository version matrix |

Do not infer that sibling folders use the same SR version. Read `SR_PACK_VERSION.json` and the actual method, schema, task-memory, lot, and pass markers in every target. The installer refuses fresh-install `--write` when it detects an existing SR installation.

## Install In A Target Project

1. Select the verified local source as described in Target source.
2. Open Codex in the target project.
3. Paste this prompt: [prompts/en/00_install_codex_environment.md](prompts/en/00_install_codex_environment.md).
4. Let Codex inspect, install, verify, and report.

For a blank or never-SR project, Codex must treat this as a method installation only:

- inspect the target repository before writing;
- explain which SR files will be added;
- wait for validation if the target project enforces strict human validation;
- install SR method files and scripts;
- avoid all application code, migrations, dependencies, secrets, and business rules;
- run verification scripts;
- stop with a report and recommended next prompts.

The fresh-install target is SR pack 4.0.0: `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4, and `SR_PASSES` 0.2. The SR contract separates `implementation_status` from `evidence_status`. Installation must not invent validated product requirements, lots, or passes.

Technical fallback:

Without a mutation option and without `--plan-out`, the installer performs a read-only preview. `--write`, `--upgrade`, `--apply-plan` and `--restore` are mutually exclusive.

Use the previously selected and verified `SR_PACK_SOURCE` clone. For a published release, clone the official source if needed and select the approved published reference; cloning alone does not select the SR 4 candidate. The candidate requires the explicitly approved local content. Set `SR_TARGET` to the intended project path before running commands.

The installer copies the source package into the target project as:

```text
AGENTS.md
DESIGN.md
docs/CURRENT_STATE.md
docs/codex/*
docs/codex/prompts/*
docs/codex/tasks/_TEMPLATE/*
scripts/codex/*
docs/codex/skills-method/*
```

These generated target-project files are intentionally not stored in this source repository.

New installations include `docs/codex/SR_PASSES.yaml`. SR Passes group several SR lots into a bounded execution pass with dependency ordering, shared preflight, human validations, and grouped E2E checks. Lots remain the atomic delivery unit in `SR_LOTS.yaml`.

The installed registry starts as `passes: []`. This is a valid state, not a missing configuration: installation does not invent a product pass. Use prompt `08` after the lots are known and validated.

New installations also include Pass Runtime Goal tooling:

```text
scripts/codex/build_pass_runtime_goal.py
docs/codex/tasks/_TEMPLATE/pass_runtime_goal.md
```

Do not generate a pass goal immediately on a blank project. First define lots, then propose and validate passes. Generate `pass_runtime_goal.md` only for a real `validated` or `in_progress` pass.

New installations also include the UI Verification Harness:

```text
scripts/codex/sr_ui_verify.mjs
scripts/codex/playwright_auth_smoke.mjs  # legacy wrapper
docs/codex/skills-method/aurora-ui-visual-qa/
PROJECT_PROFILE.yaml ui_validation
```

For a public app, keep `ui_validation.auth.mode = none`. For an authenticated app, configure `auth.mode = storage_state` and keep `.playwright/.auth/` out of Git.

## Upgrade A Target Project

Open Codex in the target project and paste:

```text
prompts/en/05_upgrade_codex_environment.md
```

Codex should audit the installed SR version, preserve project-owned files and task memories, then use the installer only after reporting the upgrade plan.

For a project already using an older SR Method, the upgrade must be non-regressive:

- preserve `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `PROJECT_PROFILE.yaml`, `SKILL_MAP.md`, local domain docs, handoffs, task memories, and project skills;
- preserve `SR_LOTS.yaml` and existing lot statuses unless evidence and validation justify a change;
- add or refresh `SR_PASSES.yaml` additively if absent/stale, without marking passes `validated` silently;
- preserve historical task memories and do not batch-convert them to `sr_contract.json` without explicit validation;
- keep legacy contracts without new gates as warnings, not blocking errors;
- add `ui_validation` additively when possible; if absent, keep the project usable for non-UI tasks but block significant UI lot closure until configured;
- preserve legacy `playwright_auth_smoke.mjs` behavior through the wrapper and prefer `sr_ui_verify.mjs` for new UI validation;
- never commit or print Playwright storageState, cookies or tokens;
- update `docs/CURRENT_STATE.md` with the SR version change, source commit, checks, warnings, and next prompt;
- run `07_realign_sr_state_after_upgrade` before resuming application development.
- keep reading historical `sr_contract` 3.0.0 contracts, while new task memories and reopened lots use 3.1.0;
- warn when a multi-lot historical contract has only one generic `validated_request`;
- do not rewrite historical memories in bulk; normalize only active or reopened scope after reviewing its source and obtaining the required validation;
- preserve every open requirement ID and reopen its original lot by default instead of creating migration micro-lots.

Representative official layouts from SR 2.2.0, 2.3.0, 2.3.5, 2.4.1, and 3.0.0 are covered by upgrade regressions. If an older target has no `SR_PASSES.yaml`, the upgrade creates a valid `passes: []` registry and does not infer a pass from existing lots. Unknown, partial, or locally adapted layouts still require the per-file audit in prompt `05`; the regression fixture does not claim universal compatibility with arbitrary local structures.

An installer exit code of 0 is only implementation evidence. The upgrade is successful only when `sr_post_install_check.py` also passes; otherwise report the target as `repair` and keep its errors explicit.

When upgrading several repositories, audit and report each repository separately. A green result in one folder cannot hide an old, partial, failed, or locally adapted installation in another folder.

Technical fallback:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" \
  --target /path/to/project \
  --profile default \
  --upgrade
```

Upgrade backups are written under:

```text
docs/codex/upgrade_backups/
```

## Verify

Open Codex in the target project and paste:

```text
prompts/en/06_verify_sr_installation.md
```

Technical checks Codex may run:

```bash
python3 scripts/codex/verify_codex_pack.py
python3 scripts/codex/validate_release_docs.py --root . --json
python3 scripts/codex/audit_codex_pack.py --root . --json
python3 scripts/codex/sr_post_install_check.py --root . --json
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json
```

## Define SR Lots

After framing a feature or collecting inbox items, ask Codex to define or promote lots with code evidence:

```text
prompts/en/09_define_sr_lots_from_scope.md
```

This step updates SR memory only. It must not modify application code.

## Define SR Passes

After lots have been created or after upgrading an existing project, ask Codex to propose passes:

```text
prompts/en/08_define_sr_passes_from_lots.md
```

This step updates only SR memory. It must not modify application code.

## Generate A Pass Runtime Goal

After a pass is validated, Codex may generate a runtime goal:

```bash
python3 scripts/codex/build_pass_runtime_goal.py \
  --pass-id <PASS_ID> \
  --output docs/codex/tasks/YYYY-MM-DD_<pass-id>/pass_runtime_goal.md
```

The generated `/goal` command is intentionally short. The script enforces:

```yaml
max_goal_command_chars: 1000
hard_limit: 4000
```

If user E2E is required, Codex should finish the pass in `user_testing`, not `done`. The next pass must be proposed, never started silently.

## Start A Governed Codex Session

After installation or upgrade, paste:

```text
prompts/en/01_start_sr_session.md
```

For application runtime agents, paste:

```text
prompts/en/15_define_runtime_agents.md
```
