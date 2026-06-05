# Aurora SR Method Codex Pack

[![GitHub stars](https://img.shields.io/github/stars/syl2042/Aurora_SR_method_codex_pack?style=social)](https://github.com/syl2042/Aurora_SR_method_codex_pack/stargazers)
[![Forks](https://img.shields.io/github/forks/syl2042/Aurora_SR_method_codex_pack?style=social)](https://github.com/syl2042/Aurora_SR_method_codex_pack/forks)
[![Issues](https://img.shields.io/github/issues/syl2042/Aurora_SR_method_codex_pack)](https://github.com/syl2042/Aurora_SR_method_codex_pack/issues)
[![Last commit](https://img.shields.io/github/last-commit/syl2042/Aurora_SR_method_codex_pack)](https://github.com/syl2042/Aurora_SR_method_codex_pack/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Star this repository](https://github.com/syl2042/Aurora_SR_method_codex_pack/stargazers) |
[Documentation](https://docs.auroramind.fr/docs/SR_Method) |
[Install with Codex](INSTALLATION.md) |
[Upgrade a project](prompts/en/05_upgrade_codex_environment.md) |
[Verify installation](prompts/en/06_verify_sr_installation.md)

## Languages

[English](README.md) |
[Francais](README.fr.md) |
[Deutsch](README.de.md) |
[Portugues](README.pt.md) |
[Espanol](README.es.md)

## What It Is

Aurora SR Method Codex Pack is a public source package for installing a governed Codex operating method inside software projects.

SR means **Specification Runtime**. The method gives Codex a project-local operating frame: bootstrap rules, task memory templates, evidence gates, repo maps, controlled prompts, validation scripts, and reusable method skills.

The goal is simple: help a developer clone this pack, ask Codex to install it in a target project, verify the installation, then work with Codex through explicit scope, evidence, validation, and handoff rules.

It is especially useful when Codex must work across several sessions, several developers, or larger codebases where uncontrolled context loss quickly becomes expensive.

```text
Clone pack -> Paste Codex prompt -> Install SR Method -> Verify -> Start governed development
```

## Why Developers Use It

The SR Method is designed for developers who want Codex to work like a disciplined project teammate, not like a one-off code generator.

It helps turn broad requests into controlled development sessions with explicit scope, written task memory, evidence-based decisions, validation gates, and clean handoffs.

Key gains for developers:

- **Faster project onboarding**: Codex reads the repository, detects the stack, and installs a project-local operating frame.
- **Less context loss**: task memory, current state, findings, decisions, and verification notes are written inside the project.
- **Safer autonomous work**: Codex works by bounded lots, checks evidence before changing code, and keeps human validation explicit.
- **Better continuity between sessions**: another Codex session or developer can resume from the written state instead of rediscovering everything.
- **Cleaner reviews**: changes are tied to scope, assumptions, files touched, verification commands, and remaining risks.
- **Reusable operating discipline**: the same method can be installed across projects while adapting to each repository.
- **Prompt-first workflow**: developers interact with Codex through copy-paste prompts; scripts remain implementation details handled by Codex when needed.

In practice, the pack reduces the cost of giving Codex real project work: fewer vague changes, fewer forgotten constraints, clearer validation, and better handoff quality.

## Language Policy

The SR Method core is maintained in English as the canonical technical language.

Developer entry points are available in multiple languages to make onboarding easier:

- README files
- installation guides
- copy-paste Codex prompts for install, upgrade, verification, session start, and runtime-agent definition

The installed project can still instruct Codex to speak with the user in French, German, Portuguese, Spanish, English, or another language. The technical method remains canonical in English.

## Quick Start With Codex

1. Clone this repository locally.
2. Open Codex in the target project.
3. Paste the install prompt for your language.
4. Let Codex inspect, install, and verify the SR Method.

Copy-paste prompts:

| Language | Install | Upgrade | Verify | Start session | Runtime agents |
| --- | --- | --- | --- | --- | --- |
| English | [00](prompts/en/00_install_codex_environment.md) | [05](prompts/en/05_upgrade_codex_environment.md) | [06](prompts/en/06_verify_sr_installation.md) | [01](prompts/en/01_start_sr_session.md) | [15](prompts/en/15_define_runtime_agents.md) |
| Francais | [00](prompts/fr/00_install_codex_environment.md) | [05](prompts/fr/05_upgrade_codex_environment.md) | [06](prompts/fr/06_verify_sr_installation.md) | [01](prompts/fr/01_start_sr_session.md) | [15](prompts/fr/15_define_runtime_agents.md) |
| Deutsch | [00](prompts/de/00_install_codex_environment.md) | [05](prompts/de/05_upgrade_codex_environment.md) | [06](prompts/de/06_verify_sr_installation.md) | [01](prompts/de/01_start_sr_session.md) | [15](prompts/de/15_define_runtime_agents.md) |
| Portugues | [00](prompts/pt/00_install_codex_environment.md) | [05](prompts/pt/05_upgrade_codex_environment.md) | [06](prompts/pt/06_verify_sr_installation.md) | [01](prompts/pt/01_start_sr_session.md) | [15](prompts/pt/15_define_runtime_agents.md) |
| Espanol | [00](prompts/es/00_install_codex_environment.md) | [05](prompts/es/05_upgrade_codex_environment.md) | [06](prompts/es/06_verify_sr_installation.md) | [01](prompts/es/01_start_sr_session.md) | [15](prompts/es/15_define_runtime_agents.md) |

Manual script commands are documented as fallback details in [INSTALLATION.md](INSTALLATION.md). The preferred workflow is prompt-first: Codex reads the prompt, checks the repository, runs the scripts when appropriate, and reports what changed.

## What This Repository Contains

This repository is a clean Public source package. It is intended to be cloned by a developer, then installed into a target project.

Published source folders:

```text
core/             SR Method templates and reference docs, English canonical core
prompts/          root prompts plus multilingual developer entry prompts
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

Use [INSTALLATION.md](INSTALLATION.md) or paste [the English install prompt](prompts/en/00_install_codex_environment.md) into Codex from your target project.

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

## Verify The Pack Source

From this repository:

```bash
python3 scripts/codex/verify_codex_pack.py
python3 scripts/codex/audit_codex_pack.py --root . --json
git diff --check
```

## Public Hygiene

Before making a fork or release public, verify that the repository only contains source package files and no target-project state:

```bash
git ls-tree -r --name-only HEAD | grep -E '(^docs/codex/|^tasks/|\.docx$|^AGENTS.md$|^DESIGN.md$|CURRENT_STATE)'
git grep -n -I -E 'absolute_path|customer_project|client_project|internal_project' HEAD -- .
```

Both commands should return no project-specific publication blockers.

## License

MIT License. See [LICENSE](LICENSE).
