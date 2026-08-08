# Upgrade a project to the latest SR Method

You are working in an application repository that already contains an existing Aurora SR Method installation, possibly old, partial, or locally adapted.

Verifiable objective: upgrade the SR Method to the latest official version without regression, without changing application code, without overwriting project-owned adaptations, and leave the project in a realigned SR state before any development resumes.

Official SR Method source:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Local pack source:

```text
SR_PACK_SOURCE
```

`SR_PACK_SOURCE` means the local path to the official clone on the current server. Never assume a machine-specific absolute path. If the user did not provide this path, detect it or propose a suitable local path for the current server, for example `./.sr-method-pack`, `/opt/aurora/SR_Method`, or another user-approved working directory.

If the local source does not exist or is not a clone of the official repository, propose creating or updating it from the official GitHub repository before applying the upgrade. Do not download from another source without user validation.

Strict rules:

- Do not modify application code.
- Do not create migrations.
- Do not change application dependencies.
- Do not touch secrets, environment variables, or sensitive configuration files.
- Do not blindly replace `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `PROJECT_PROFILE.yaml`, `SKILL_MAP.md`, `docs/codex/SR_LOTS.yaml`, `docs/codex/SR_PASSES.yaml`, task memories, handoffs, decisions, or project skills.
- Preserve local project adaptations.
- Preserve legacy task memory files; do not create retroactive contracts in batch without explicit validation.
- Preserve `SR_LOTS.yaml`. Add `SR_PASSES.yaml` additively when missing, but do not automatically convert old lots or task memories into validated passes.
- Do not mass-convert old lots to add `design_evidence`; add the Lot Design Evidence Gate only to lots created, promoted, or resumed after upgrade.
- Add Pass Runtime Goal tooling additively (`build_pass_runtime_goal.py`, `pass_runtime_goal.md` template, `sr_passes.pass_runtime_goal` options) without generating a goal until a pass is validated.
- Never launch `/goal` during upgrade. The upgrade prepares the method; goal execution comes only after realignment, pass planning, and user validation.
- Do not close, promote, or reclassify any application lot or pass as an implicit side effect of the upgrade. If the user explicitly asks to close a lot or pass in the same work, treat that closure as a separate sub-phase after the upgrade, with validated scope, its own SR contract, evidence, and a distinct report.
- Preserve historical task memories without `propagation_gate`: report them as legacy warnings, not blocking errors. New templates and contracts created after upgrade must include the Propagation Gate.
- In full SR regime, every SR version change must update `docs/CURRENT_STATE.md` with installed version, review date, checks run, latest `NEXT_SESSION_PROMPT.md`, significant lots, and next step.
- An `upgrade` `loop_contract.json` cannot close as `done` with `memory_updates.current_state_updated=false`.
- Before any file mutation, present the upgrade plan and wait for explicit user validation.

Step 1 - Version diagnosis:

1. Read existing SR files:
   - `docs/codex/SR_PACK_VERSION.json` when present;
   - `docs/codex/SR_LOTS.yaml` when present;
   - `docs/codex/SR_PASSES.yaml` when present;
   - `docs/CURRENT_STATE.md` when present;
   - `AGENTS.md` when present;
   - `docs/codex/tasks/` when present.
2. Run available audits without modifying files:
   - `python3 scripts/codex/audit_codex_pack.py --json` when available;
   - `python3 scripts/codex/verify_codex_pack.py` when available;
   - `python3 scripts/codex/sr_post_install_check.py --root .` when available.
3. If these scripts do not exist or fail because the version is too old, classify the version as `unknown` or `legacy`.

Step 2 - Classification:

Classify the project into one flow:

- `upgrade_minor_3x` when the installed version is already `3.x`;
- `upgrade_standard_235_plus` when the version is `2.3.5+`;
- `upgrade_legacy_unknown` when the version is missing, unreadable, lower than `2.3.5`, or the SR installation is partial.

Step 3 - Official source:

1. Check whether a local clone of the official pack already exists.
2. If it exists, verify its remote and git state.
3. If it does not exist, propose cloning:
   `git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git ./.sr-method-pack`
4. Use only the official source or a verified local clone.
5. Record the source commit in the final report.

Step 4 - Analysis before mutation:

Compare the current installation with the latest pack version and identify:

- missing SR files;
- old SR files;
- project-owned files to preserve;
- files requiring careful merge;
- presence or absence of `SR_PASSES.yaml`;
- presence or absence of Pass Runtime Goal tooling;
- presence or absence of the Lot Design Evidence Gate;
- overwrite risks;
- application lots or passes that may need resumption or closure, to be handled only as a separate sub-phase when explicitly requested by the user;
- old contracts or task memories to keep as legacy warnings.

Important: old lots without `design_evidence` must not be modified in batch. `design_evidence` must be added only to lots created, promoted, or resumed after upgrade.

Step 5 - Plan to validate:

Before any modification, present a short plan with:

- detected version;
- selected upgrade flow;
- files to add;
- files to update;
- files to preserve;
- identified risks;
- planned verification commands;
- expected impact on `SR_LOTS.yaml`, `SR_PASSES.yaml`, `AGENTS.md`, `CURRENT_STATE.md`, and `docs/codex/tasks/`.
- confirmation that no application lot or pass will be closed implicitly by the upgrade; any requested closure must be isolated as a validated sub-phase.

Wait for explicit user validation before modifying.

Step 6 - Upgrade after validation:

After validation only:

1. Apply the SR upgrade additively.
2. Preserve project files and history.
3. Update required SR scripts, templates, prompts, and docs.
4. Add `SR_PASSES.yaml` if absent, without declaring an executable pass automatically.
5. Add Pass Runtime Goal tooling if absent:
   - `build_pass_runtime_goal.py`
   - `pass_runtime_goal.md` template
   - `sr_passes.pass_runtime_goal` options
6. Verify that the Goal Length Gate is present:
   - `max_goal_command_chars: 1000`
   - `hard_limit: 4000`
7. Verify that the Lot Design Evidence Gate is documented and active for new or resumed lots.

Step 7 - Verification:

Run the available and applicable checks:

- `python3 scripts/codex/audit_codex_pack.py`
- `python3 scripts/codex/verify_codex_pack.py`
- `python3 scripts/codex/sr_post_install_check.py --root .`
- `python3 scripts/codex/find_next_session_prompt.py --root .`
- `python3 scripts/codex/audit_sr_project.py --root .`
- `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` if the file exists
- `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` if `SR_PASSES.yaml` exists
- `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json` if present
- `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json` if present
- `python3 scripts/codex/audit_sr_task_contracts.py --root .`
- `python3 scripts/codex/context_budget_report.py --root . --compact`
- `python3 scripts/codex/validate_skills.py --path ~/.codex/skills` if method skills are installed

If some scripts are missing before upgrade, report that as normal for an old version, then rerun after upgrade.

Step 8 - Mandatory realignment:

After the upgrade, update or propose updating `docs/CURRENT_STATE.md` with:

- SR version before;
- SR version after;
- update date;
- source commit used;
- files added or updated;
- files preserved;
- legacy warnings;
- `SR_LOTS.yaml` status;
- `SR_PASSES.yaml` status;
- Pass Runtime Goal status;
- Lot Design Evidence Gate status;
- recommended next step.

Step 9 - Recommended continuation:

At the end, do not resume application development directly.

Propose the following sequence according to the project state:

1. use `07_realign_sr_state_after_upgrade.md` to realign SR state;
2. use `09_define_sr_lots_from_scope.md` to create or promote lots with prior analysis of impacted files;
3. use `08_define_sr_passes_from_lots.md` to automatically propose lot groupings into passes;
4. generate a `pass_runtime_goal.md` only after human validation of a pass;
5. launch `/goal` only for a validated pass, never during upgrade.

Expected final report:

- version before/after;
- selected upgrade flow;
- SR Method source commit used;
- modified files;
- preserved files;
- successful validations;
- failed or non-applicable validations;
- legacy warnings;
- application lots or passes detected as candidates for closure or resumption, and status of any explicitly requested closure sub-phase;
- proposed next action.

Mandatory end: wait for validation before any application modification or pass execution.
