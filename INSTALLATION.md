# Installation

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

## Install In A Target Project

1. Clone this repository locally.
2. Open Codex in the target project.
3. Paste this prompt: [prompts/en/00_install_codex_environment.md](prompts/en/00_install_codex_environment.md).
4. Let Codex inspect, install, verify, and report.

Technical fallback:

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"

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

Open Codex in the target project and paste:

```text
prompts/en/05_upgrade_codex_environment.md
```

Codex should audit the installed SR version, preserve project-owned files and task memories, then use the installer only after reporting the upgrade plan.

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
python3 scripts/codex/audit_codex_pack.py --root . --json
python3 scripts/codex/sr_post_install_check.py --root . --json
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json
```

## Start A Governed Codex Session

After installation or upgrade, paste:

```text
prompts/en/01_start_sr_session.md
```

For application runtime agents, paste:

```text
prompts/en/15_define_runtime_agents.md
```
