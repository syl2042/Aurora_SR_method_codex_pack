# Aurora SR Method Codex Pack

SR Method 4.1 is a lean execution harness for Codex: a short permanent kernel, conditional procedures, exact skill triggers, compact state and proportionate final verification.

Status: **4.1.0 (`released`)**, published on 2026-09-24.

**EN** · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md)

[Installation](INSTALLATION.md) · [Changelog](CHANGELOG.md) · [Install prompt](prompts/en/00_install_codex_environment.md) · [Upgrade prompt](prompts/en/05_upgrade_codex_environment.md) · [Verify](prompts/en/06_verify_sr_installation.md) · [Realign](prompts/en/07_realign_sr_state_after_upgrade.md)

## What changes in 4.1

- `AGENTS.md` is reconciled and reduced instead of receiving another appended manual.
- The default cognitive catalog is limited to lot running, diagnosis, architecture and UI visual QA.
- TDD, planning files, terminal compaction, final diff review and RepoMap maintenance are not skills.
- No intentionally failing test, artificial red gate or source-development rollback loop.
- Scope, Verification and Activation are the only execution boundaries.
- New tasks may use one compact `task_state.yaml`; legacy SR and loop contracts remain readable.
- `core` mode performs no MCP call. `nexus_kg` follows an explicit `MCP_POLICY.yaml` with deferred capabilities, allowlists, approvals and result budgets.
- Input, cached input/write, context occupancy, output and tool-result volume are measured separately.
- Pack qualification tests and fixtures remain source-only; target projects receive only runtime tools.

## Operating model

```text
AGENTS.md kernel
  -> SR_ROUTES.json
  -> triggered procedure only
  -> zero to two specialized skills
  -> real source and bounded tools
  -> proportionate final verification
```

Simple questions and local edits stay on the fast path. Multi-lot execution uses the harness. Build or deployment rules load only after an explicit activation request.

## Install or upgrade

Select an explicit `SR_PACK_SOURCE` and target repository. A fresh target uses prompt `00`; any target with SR markers uses prompt `05`.

The updater is version-agnostic: the declared previous version is provenance only. It classifies actual files as absent, managed, locally modified, unmanaged, obsolete, conflicting or already aligned. It preserves project-owned state and removes an obsolete managed artifact only when its content is recognized.

```bash
# read-only preview
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json

# fresh target, after validation
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --write

# existing or partial target, after validation
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

Then run:

```bash
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

An installer exit code alone is not acceptance. Review preservation, conflicts, post-install checks and remaining product realignment. See [INSTALLATION.md](INSTALLATION.md).

## Compatibility

- Old, partial, unversioned and locally adapted installations are evaluated by content.
- Historical lots, passes, task memories, open requirements and local skills remain project-owned.
- Legacy contracts stay readable; V4.1 does not mass-rewrite them.
- Unknown modified pack files are preserved or reported, never silently overwritten.
- Application code, secrets, dependencies, migrations and deployments are outside a method-only upgrade.

## Repository map

- `core/`: method, routes, procedures, profiles and policies.
- `skills-method/`: the small distributed method-skill catalog.
- `scripts/install_codex_pack.py`: preview and transactional convergence.
- `scripts/codex/`: validation, audit and bounded tooling.
- `prompts/`: public entry prompts and localized variants.
- `tasks/_TEMPLATE/`: compact state and legacy-readable templates.
- `tools/sr-cockpit/`: optional read-only operator UI; not installed in target projects.

Release history and migration notes live only in [CHANGELOG.md](CHANGELOG.md).
