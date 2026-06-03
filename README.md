# Aurora SR Method Codex Pack

Public source package for installing the **SR Method** in software projects that use Codex.

SR means **Specification Runtime**. The method gives Codex a project-local operating frame: bootstrap rules, task memory templates, evidence gates, repo maps, controlled prompts, validation scripts, and method skills.

Official source:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

## What This Repository Contains

This repository is a clean source package. It is intended to be cloned by a developer, then installed into a target project.

Published source folders:

```text
core/             SR Method templates and reference docs
prompts/          operational prompts copied into target projects
scripts/          install, audit and validation scripts
skills-method/    reusable Codex method skills
blueprints/       task, lot, inbox and domain-skill templates
profiles/         generic installation profiles
project-skills/   placeholder for project-local skills
adr/              ADR template
```

This public repository intentionally does not publish:

```text
AGENTS.md
DESIGN.md
docs/CURRENT_STATE.md
docs/codex/
docs/codex/tasks/
tasks/
*.docx
local handoffs or session memories
project/client-specific paths or data
```

Those files are generated or maintained inside each target project after installation.

## Install Into A Project

Clone or update the pack:

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"
cd "$SR_PACK_SOURCE"
git pull
```

Install into a target project:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" \
  --target /path/to/project \
  --profile default \
  --write
```

Upgrade an existing target project:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" \
  --target /path/to/project \
  --profile default \
  --upgrade
```

## Verify The Pack Source

From this repository:

```bash
python3 scripts/codex/verify_codex_pack.py
python3 scripts/codex/audit_codex_pack.py --root . --json
git diff --check
```

After installation, run the target-project checks from the target project root:

```bash
python3 scripts/codex/verify_codex_pack.py
python3 scripts/codex/audit_codex_pack.py --root . --json
python3 scripts/codex/sr_post_install_check.py --root . --json
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json
```

## Runtime Agent Method

The pack includes the SR Agent Method for application runtime agents. It requires controlled prompts, explicit variables, controlled SQL/RAG bindings, runtime skills, typed output contracts, validation, traces, and human validation for critical actions.

For Python backends, consumed agent output should be validated with Pydantic. Other stacks should use an equivalent strict typed validator.

## Public Hygiene

Before making a fork or release public, verify that the repository only contains source package files and no target-project state:

```bash
git ls-tree -r --name-only HEAD | grep -E '(^docs/codex/|^tasks/|\\.docx$|^AGENTS.md$|^DESIGN.md$|CURRENT_STATE)'
git grep -n -I -E 'absolute_path|customer_project|client_project|internal_project' HEAD -- .
```

Both commands should return no project-specific publication blockers.
