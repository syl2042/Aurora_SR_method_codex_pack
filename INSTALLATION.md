# Installation

Official repository:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

This repository contains only the SR Method source package: templates, prompts, scripts, method skills, profiles and blueprints.

## Prepare A Local Source

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"
cd "$SR_PACK_SOURCE"
git pull
```

## Install In A Target Project

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" \
  --target /path/to/project \
  --profile default \
  --write
```

The installer copies the source package into the target project as:

```text
AGENTS.md
DESIGN.md
docs/CURRENT_STATE.md
docs/codex/*
docs/codex/prompts/*
docs/codex/tasks/_TEMPLATE/*
scripts/codex/*
```

These generated target-project files are intentionally not stored in this source repository.

## Upgrade A Target Project

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" \
  --target /path/to/project \
  --profile default \
  --upgrade
```

The upgrade path preserves project-owned files when needed and writes backups under:

```text
docs/codex/upgrade_backups/
```

## Verify

From the source repository:

```bash
python3 scripts/codex/verify_codex_pack.py
python3 scripts/codex/audit_codex_pack.py --root . --json
git diff --check
```

From the target project after installation:

```bash
python3 scripts/codex/verify_codex_pack.py
python3 scripts/codex/audit_codex_pack.py --root . --json
python3 scripts/codex/sr_post_install_check.py --root . --json
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json
```

## First Codex Session In The Target Project

After installation, ask Codex to read:

```text
docs/codex/prompts/00_install_codex_environment.md
docs/codex/prompts/06_verify_sr_installation.md
docs/codex/prompts/01_start_sr_session.md
```

For application runtime agents, also read:

```text
docs/codex/prompts/15_define_runtime_agents.md
```
