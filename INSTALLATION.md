# Installation — SR Method 4.1

Status: released `4.1.0`. Select an explicit `SR_PACK_SOURCE`; record its `release_status`, `source_commit` and Git state.

[Français](INSTALLATION.fr.md) · [Deutsch](INSTALLATION.de.md) · [Español](INSTALLATION.es.md) · [Português](INSTALLATION.pt.md)

## Choose the path

| Observed target | Prompt | Installer mode |
|---|---|---|
| No SR marker | `prompts/en/00_install_codex_environment.md` | `--write` |
| Any SR marker, partial or unknown state | `prompts/en/05_upgrade_codex_environment.md` | `--upgrade` |

Never choose the algorithm from the previous version number. The updater uses actual content, managed fingerprints and local modifications.

## Preview

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Review every conflict and preserved file. `--plan-out` is optional and writes file contents locally; protect that plan.

## Apply after validation

```bash
# fresh
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --write

# existing, partial, unversioned or locally adapted
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

The transaction guards the preview against concurrent edits, backs up changed files and supports exact `--restore`. It refuses to overwrite later edits.

## File convergence

| State | Action |
|---|---|
| absent | Create target content. |
| managed exact | Update safely. |
| managed block with local surrounding rules | Replace the managed block and preserve local rules. |
| project-owned | Preserve and add missing safe defaults only where defined. |
| unknown customized pack file | Report a conflict; do not overwrite. |
| recognized obsolete managed file | Remove transactionally. |
| obsolete but locally modified | Preserve and report. |
| already target | No operation. |

The upgrade never closes application lots, rewrites historical memories, changes product code or performs a deployment.

## Verify

```bash
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" \
  --root "$SR_TARGET" --json
```

The post-check is read-only by default. Add `--write-report` only when a persisted audit artifact is wanted.

The result must prove version `4.1.0`, required files, short AGENTS kernel, active skill catalog, route integrity, documentation consistency and preservation. Then use `prompts/en/07_realign_sr_state_after_upgrade.md` only if project state needs realignment.

Fresh installations include `SR_LOTS.yaml`, `SR_PASSES.yaml` with `passes: []`, `MCP_POLICY.yaml`, `task_state.yaml`, the UI verifier and legacy contract readers. No product lot, pass or MCP capability is invented.
