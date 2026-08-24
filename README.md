# Aurora SR Method Codex Pack

[![GitHub stars](https://img.shields.io/github/stars/syl2042/Aurora_SR_method_codex_pack?style=social)](https://github.com/syl2042/Aurora_SR_method_codex_pack/stargazers)
[![Forks](https://img.shields.io/github/forks/syl2042/Aurora_SR_method_codex_pack?style=social)](https://github.com/syl2042/Aurora_SR_method_codex_pack/forks)
[![Issues](https://img.shields.io/github/issues/syl2042/Aurora_SR_method_codex_pack)](https://github.com/syl2042/Aurora_SR_method_codex_pack/issues)
[![Last commit](https://img.shields.io/github/last-commit/syl2042/Aurora_SR_method_codex_pack)](https://github.com/syl2042/Aurora_SR_method_codex_pack/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**EN** · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt.md) · [Español](README.es.md)

[⭐ Star this repository](https://github.com/syl2042/Aurora_SR_method_codex_pack/stargazers) ·
[Documentation](https://docs.auroramind.fr/docs/SR_Method) ·
[Installation](INSTALLATION.md) ·
[Changelog](CHANGELOG.md) ·
[Install with Codex](prompts/en/00_install_codex_environment.md) ·
[Upgrade](prompts/en/05_upgrade_codex_environment.md) ·
[Verify](prompts/en/06_verify_sr_installation.md)

---

## What it is

**Aurora SR Method Codex Pack** is a public pack for installing the **SR Method** into a software project so Codex works inside an explicit, verifiable, and transferable operating frame.

Public source package for the Aurora SR Method Codex operating pack.

**SR** means **Specification Runtime**.

The central idea is simple:

> **AI is free in exploration, but constrained in execution.**

Codex can analyze, diagnose, propose, and compare. But as soon as it needs to modify a file, change a dependency, create a migration, touch configuration, push to GitHub, or make a business decision, it must work inside a validated scope, with evidence, checks, and resumable memory.

```text
Clone the pack
-> Paste a prompt into Codex
-> Install the SR Method in the target project
-> Verify the installation
-> Work through governed lots
-> Test, document, hand off
```

---

## Why use this pack?

Codex is powerful, but on a real project it can quickly become risky when context is unclear:

- it codes before reading the sources;
- it confuses hypotheses with verified facts;
- it expands scope without validation;
- it forgets previous decisions;
- it closes a lot without real user testing;
- it becomes hard to resume in a new session.

The SR Method brings project-work discipline: **clear objective, sources read, short lots, validation gates, SR contracts, task memory, and clean handoff**.

It turns Codex into a more reliable development teammate: not a one-off code generator, but an agent that works inside the repository with method.

---

## Who is it for?

This pack is mainly for:

| Profile | Need covered |
|---|---|
| Solo developer | Keep control over Codex, even across several long sessions. |
| Tech lead | Standardize how Codex reads, modifies, verifies, and documents. |
| SaaS founder | Move a product forward quickly without losing vision, scope, and decisions. |
| AI trainer / consultant | Demonstrate a reproducible method for AI-assisted development. |
| Product-tech team | Make Codex work auditable, testable, and transferable. |

---

## What the SR Method changes in practice

### Without an SR frame

```text
Broad prompt
-> Codex interprets
-> Codex modifies
-> Final summary
-> Hard to know what is proven, tested, or still risky
```

### With an SR frame

```text
User intent
-> Source reading
-> Proposed scope
-> Human validation
-> Short lot
-> SR gates
-> Checks
-> User E2E tests
-> Resumable memory
-> Handoff
```

---

## Key principles

### 1. Prompt-first

The recommended path is not to run scripts manually.

You open Codex in the target project, paste the appropriate prompt, then Codex inspects the repository, proposes the scope, asks for validation, and runs useful scripts when needed.

### 2. Evidence before action

Before acting, Codex must read the available sources: SR files, real code, tests, logs, official documentation, RepoMap, or Knowledge Graph when available.

### 3. Short and verifiable lots

Development is split into named, bounded, traceable lots.

A lot is not `done` because Codex finished coding. It becomes `done` when the planned checks and, when needed, user E2E tests are validated.

### 4. Explicit human validation

Codex can analyze freely. But sensitive actions require validation: file modification, dependency change, migration, GitHub push, configuration, secret, business rule, or product decision.

### 5. Resumable memory

Every important session must leave usable traces: current state, decisions, sources read, files changed, checks, remaining risks, and the next resume prompt.

---

## Optional Tooling

### Aurora SR Cockpit

This repository includes a small read-only dashboard in [tools/sr-cockpit](tools/sr-cockpit) for supervising SR Method projects under `/home/ubuntu/apps`.

It shows the project list, active Codex sessions, SR version, lots, passes, inbox entries, task memories, gate status, and basic Git state. The cockpit is not installed into target projects by the SR installer; it is an operator tool kept in this pack so existing projects can update the SR Method without receiving unrelated UI files.

Quick local server start:

```bash
cd tools/sr-cockpit
npm install
npm run build
npm start -- --host 127.0.0.1 --port 18787
```

Windows/MobaXterm launcher scripts are available in [tools/sr-cockpit/scripts/windows](tools/sr-cockpit/scripts/windows).

---

## Target release 3.7.0

Target version `3.7.0` prevents validated requests from disappearing behind a global status. SR Contract 3.1.0 separates `implementation_status` from `evidence_status`, derives each requirement decision and the global Completion Gate, requires open-requirement inheritance on resume, and reserves `user_testing` for technically complete implementations.

User feedback about an existing function now reopens the original lot by default and reloads its complete checklist. Creating a new lot requires evidence that the request is outside the existing scope. Contracts 3.0.0 remain readable and are not mass-rewritten; overly generic legacy registries receive a manual-normalization warning.

Installation is now explicit about two paths: prompt `00` is only for a repository with no SR markers, while prompt `05` audits and upgrades every existing repository independently. When several folders use different SR versions, Codex must present a per-repository matrix and cannot derive a global green status from only some targets. The installer rejects fresh `--write` mode when it detects an existing SR installation.

Fresh installs and upgrades without product passes now start from a valid `passes: []` registry. No example pass is inferred from legacy lots. Upgrade regressions cover representative official layouts SR 2.2.0, 2.3.0, 2.3.5, 2.4.1, and 3.0.0; unknown or locally adapted layouts remain subject to per-file audit. Installer success alone is insufficient: the target stays in `repair` until `sr_post_install_check.py` passes.

## Release history

See [CHANGELOG.md](CHANGELOG.md) for the complete version-by-version history, migration notes, compatibility guarantees, and source release references.

### First install vs upgrade

For a first installation in a blank project, Codex should install SR files, verify the pack, then stop before application development. `SR_PASSES.yaml` starts with `passes: []`; the Pass Runtime Goal tooling is installed, but pass goals are generated only after lots and passes exist.

For an existing project with an older SR Method already used in real work, Codex must preserve project-owned files, task memories, `SR_LOTS.yaml`, decisions, handoffs, and local skills. The upgrade is additive: it adds or refreshes SR method files and scripts, then asks Codex to realign the project state before continuing development. Historical task memories are not converted in bulk without explicit validation.

Recommended upgrade sequence:

```text
05_upgrade_codex_environment
-> 06_verify_sr_installation
-> 07_realign_sr_state_after_upgrade
-> 08_define_sr_passes_from_lots if passes are absent/stale
-> build_pass_runtime_goal.py only for the next validated pass
```

This sequence is designed to avoid regressions after update: Codex must understand what changed, preserve existing project state, reorganize passes only when evidence supports it, and stop before any application code work.

---

## SR Passes and SR Agent Method

Version `3.2.0` introduced two distinct evolutions; version `3.2.1` then hardened ordered inter-pass dependencies:

### SR Passes: group lots into execution passes

SR Passes introduce an orchestration layer above lots. A lot remains the atomic unit for scope, acceptance criteria, authorized paths, stop conditions, status, and task memory. A pass groups several related lots when they share a foundation, a preflight, dependencies, or one coherent E2E validation.

SR 3.2.0 added:

- `docs/codex/SR_PASSES.yaml` for bounded multi-lot execution;
- `scripts/codex/validate_pass_contract.py` to verify lot references and dependency order;
- `prompts/09_define_sr_lots_from_scope.md` to create or promote lots with Lot Design Evidence Gate;
- `prompts/08_define_sr_passes_from_lots.md` and localized variants to propose passes from existing lots;
- installation and upgrade rules that preserve `SR_LOTS.yaml` and add passes without converting historical task memories;
- a Pass Planning Gate before any significant multi-lot execution.

3.2.x note: the validator now accepts dependencies to strictly earlier passes for `proposed` or `planned` passes, so a future pass plan can be audited before execution. `validated` or `in_progress` passes still require those earlier dependencies to be `done` or `user_testing`. Dependencies to later passes, lots duplicated across passes, and unfinished dependencies outside every pass remain rejected.

This evolution is useful when a roadmap, a large brief, or an autonomous phase cannot be represented cleanly as one isolated lot. The pass makes the execution order, shared preflight, human validations, external actions, migrations, stop conditions, and grouped E2E checks explicit before coding starts.

### SR Agent Method: runtime agents without framework lock-in

SR 3.2.0 also added:

- a runtime agent contract template based on bounded product actions, stable internal representations, prompt contracts, message builders, tools/actions, routing/fallback, validation and traces.

When a new function, repair, or discovery may affect more than the current lot, Codex must now:

- apply the **Backlog Mutation Gate** to decide whether `SR_INBOX.yaml` or `SR_LOTS.yaml` must be updated;
- apply the **Global Impact Gate** before coding, reviewing impact across product flows, data, permissions, APIs/services, UI, tests, migrations, risks, and existing lots;
- run **Lot Dependency Reconciliation** to classify affected lots as `impacted`, `blocked_by`, `reopened`, `superseded`, `split_required`, `depends_on`, or `unaffected`;
- document `no_backlog_mutation_required` when no backlog change is needed.

This keeps SR project-agnostic while preventing important cross-project implications from staying implicit.

---

## The full workflow

```mermaid
flowchart LR
    A[Product intent] --> B[Product Discovery]
    B --> C[Domain Expertise]
    C --> D[Codex Project Pack]
    D --> E[SR Development]
    E --> F[Delivery & Handoff]
```

| Step | Objective | Expected output |
|---|---|---|
| **1. Product Discovery** | Clarify the need before code. | Product vision, target users, V0, exclusions, risks. |
| **2. Domain Expertise** | Prevent Codex from treating the domain as generic CRUD. | Vocabulary, critical rules, sources of truth, LLM risks. |
| **3. Codex Project Pack** | Turn discovery into a Codex-ready dossier. | Brief, PRD, specs, architecture, data model, API, UX, tests, initial lots. |
| **4. SR Development** | Make Codex work by controlled lots inside the repository. | Executed, verified, documented, testable lot. |
| **5. Delivery & Handoff** | Deliver cleanly and enable resumption. | E2E tests, SR memory, contracts, risks, next step. |

---

## Quick start with Codex

Install Into A Project by opening Codex in the target repository and using the installation prompt below.

### 1. Clone this repository

```bash
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git
```

### 2. Open Codex in the target project

Move into the repository of the application where you want to install the SR Method.

### 3. Paste the installation prompt

Use the English prompt:

- [00_install_codex_environment.md](prompts/en/00_install_codex_environment.md)

Codex must:

1. inspect the project;
2. check whether SR is already installed;
3. install only the expected SR files;
4. avoid modifying application code;
5. run the checks;
6. produce a final report;
7. stop before any application development.

### 4. Verify the installation

Recommended prompt:

- [06_verify_sr_installation.md](prompts/en/06_verify_sr_installation.md)

### 5. Start an SR session

Recommended prompt:

- [01_start_sr_session.md](prompts/en/01_start_sr_session.md)

---

## Main prompts

| Action | Prompt |
|---|---|
| Install the SR Method | [00_install_codex_environment.md](prompts/en/00_install_codex_environment.md) |
| Start an SR session | [01_start_sr_session.md](prompts/en/01_start_sr_session.md) |
| Upgrade the SR Method | [05_upgrade_codex_environment.md](prompts/en/05_upgrade_codex_environment.md) |
| Verify the installation | [06_verify_sr_installation.md](prompts/en/06_verify_sr_installation.md) |
| Realign state after upgrade | [07_realign_sr_state_after_upgrade.md](prompts/en/07_realign_sr_state_after_upgrade.md) |
| Define SR lots from scope | [09_define_sr_lots_from_scope.md](prompts/en/09_define_sr_lots_from_scope.md) |
| Define runtime AI agents | [15_define_runtime_agents.md](prompts/en/15_define_runtime_agents.md) |

---

## Short prompt example to frame a lot

```text
Frame this need as an SR lot.

Do not code anything.

Give me:
- the verifiable objective;
- included scope;
- out of scope;
- assumptions;
- sources to read;
- candidate files;
- risks;
- planned checks;
- user E2E tests;
- recommended lot status.

Wait for my validation before any modification.
```

---

## Working by lots

The lot is the central work unit of the SR Method.

```text
proposed -> planned -> validated -> in_progress -> user_testing -> done
```

When there is a problem:

```text
user_testing -> reopened -> in_progress -> user_testing -> done
```

| Status | Meaning |
|---|---|
| `proposed` | Idea or feedback to frame. |
| `planned` | Structured lot, not yet validated. |
| `validated` | Lot validated by the user and executable. |
| `in_progress` | Codex is executing the lot. |
| `user_testing` | Code is delivered, but real user testing is expected. |
| `done` | Lot is checked and validated according to the planned criteria. |
| `reopened` | Lot reopened after bug, omission, or regression. |
| `blocked` | Lot blocked by a decision, access, or missing source. |
| `superseded` | Lot replaced by another lot or decision. |

---

## SR gates

A **gate** is a control that prevents Codex from moving forward on assumptions or delivering without evidence.

| Gate | Purpose |
|---|---|
| **Evidence Gate** | Check sources before planning. |
| **Fact Gate** | Prevent unproven conclusions. |
| **Knowledge Gate** | Build the change map from RepoMap, KG, or real code. |
| **Scope Gate** | Stay strictly inside the validated scope. |
| **Verification Gate** | Prove the change works or explain why verification is impossible. |
| **Design Gate** | Control UI/UX quality when the interface is involved. |
| **Context Budget Gate** | Prevent context loss and prepare resumption. |

Example of a good Fact Gate reflex:

```text
I cannot conclude without evidence.
I must read the relevant file, logs, tests, or official documentation before stating the cause.
```

---

## What the pack installs in a target project

After installation, the target project may contain:

```text
AGENTS.md
docs/CURRENT_STATE.md
docs/codex/SR_BOOTSTRAP.md
docs/codex/PROJECT_PROFILE.yaml
docs/codex/SKILL_DIGEST.md
docs/codex/SKILL_MAP.md
docs/codex/SR_LOTS.yaml
docs/codex/SR_INBOX.yaml
docs/codex/CODEBASE_MAP.md
docs/codex/tasks/
docs/codex/project-skills/
scripts/codex/
```

These files orient Codex, structure lots, preserve memory, validate contracts, and prepare resumptions.

They never replace reading the real code: **code, tests, and logs decide**.

---

## Public repository contents

This repository is a **public source pack**. It is meant to be cloned, then installed into target projects.

```text
core/             Canonical English method core and templates
prompts/          Root prompts and multilingual entry points
scripts/          Installation, audit, and validation scripts
skills-method/    Reusable Codex method skills
blueprints/       Templates for lots, inbox, tasks, and skills
profiles/         Generic installation profiles
project-skills/   Template location for project-local skills
adr/              ADR template
tasks/_TEMPLATE/  Task memory template
```

The public repository must not publish target-project state files:

```text
AGENTS.md
DESIGN.md
docs/CURRENT_STATE.md
docs/codex/
docs/codex/tasks/
tasks/
*.docx
local handoffs
client paths
project data
secrets
```

---

## SR contracts

The SR Method uses contracts to verify that the loop was followed.

| Contract | Question answered |
|---|---|
| `loop_contract.json` | Did Codex apply the SR loop correctly? |
| `sr_contract.json` | Are all validated user requests covered or explicitly out of scope? |

A lot must not move to `done` if a validated request remains open without clear treatment.

Typical validation commands:

```bash
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

---

## Codex skills

The method distinguishes three skill families.

### Method skills

They frame how work is done:

- diagnosis;
- planning;
- architecture;
- TDD;
- diff review;
- RepoMap maintenance;
- lot execution;
- terminal context optimization.

### Domain skills

They describe a specific domain so Codex does not invent the rules.

A good domain skill contains:

- domain vocabulary;
- non-negotiable rules;
- sources of truth;
- likely LLM mistakes;
- expected patterns;
- anti-patterns;
- checklist before closure.

### Runtime skills

They belong to application AI agents. They describe versionable behaviors loaded by a runtime: careful diagnosis, support writing, escalation, quality review, brand tone, and more.

---

## SR Agent Method

The **SR Agent Method** is an optional extension for designing AI agents embedded in business applications.

It is not a framework and does not replace LangChain, LangGraph, LlamaIndex, PydanticAI, CrewAI, or agent SDKs.

It is framework-, provider-, domain-, and UI-agnostic. It defines the agent's **runtime application contract** before implementation:

- bounded product action;
- runtime shape (`micro_agent`, `workflow_agent`, `delegation_agent`, or `mini_agent`);
- stable internal representation read or produced by the agent;
- typed inputs and outputs;
- prompt contract derived from the runtime contract;
- application-side user message builder;
- authorized data, tools, and committing actions;
- routing and fallback policy;
- validations, traces, risks, and activation status.

Core rule:

> A runtime agent is not defined by its model or prompt. It is defined by the bounded product action it serves, the stable internal representation it reads or writes, the typed contract that validates its output, and the runtime surface that consumes the validated result.

Strong principle:

> JSON produced by an LLM is not reliable application data until it has been validated on the backend side.

Recommended flow:

```text
Typed model
-> JSON Schema exposed to the LLM
-> prompt contract and controlled message builder
-> LLM JSON response
-> strict runtime validation
-> accepted application object or controlled error
```

In Python, validation must rely on **Pydantic** or an equivalent validator.

Prudence rules:

- no free SQL generated and executed by the LLM;
- structured and validated application outputs;
- critical actions subject to human validation;
- agent inactive by default until its contract is validated.

---

## SR Core mode and SR Nexus KG mode

The SR Method can operate at two levels.

| Mode | Description |
|---|---|
| **SR Core** | Codex relies on SR files, RepoMap, and direct code reading. |
| **SR Nexus KG** | A Nexus Knowledge Graph helps identify files, routes, components, services, dependencies, tests, and risk areas. |

In both cases, the principle remains the same:

> The graph or map guides the search, but the real code decides.

---

## Technical fallback commands

The normal path is **prompt-first**. The commands below are useful for fallback, audit, or automation.

### Install from a local source

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"

git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"

python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" \
  --target /path/to/project \
  --profile default \
  --write
```

### Verify the source pack

From this repository:

```bash
python3 scripts/codex/verify_codex_pack.py
python3 scripts/codex/audit_codex_pack.py --root . --json
git diff --check
```

### Verify an installed project

From the target project, depending on present files:

```bash
python3 scripts/codex/verify_codex_pack.py
python3 scripts/codex/audit_codex_pack.py --json
python3 scripts/codex/sr_post_install_check.py --root . --json
python3 scripts/codex/find_next_session_prompt.py --root . --json
python3 scripts/codex/audit_sr_project.py --root . --json
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
python3 scripts/codex/audit_sr_task_contracts.py --root . --json
git diff --check
git status --short
```

---

## Public release hygiene

Before publishing a fork or release, check that no target-project data was included by mistake.

```bash
git ls-tree -r --name-only HEAD | grep -E '(^docs/codex/|^tasks/|\.docx$|^AGENTS.md$|^DESIGN.md$|CURRENT_STATE)'
git grep -n -I -E 'absolute_path|customer_project|client_project|internal_project' HEAD -- .
```

These commands must return no publication blocker.

---

## Language policy

The technical core of the SR Method remains maintained in **canonical English** to preserve a stable and coherent base.

Developer entry points are available in multiple languages:

- README;
- installation guides;
- copy-paste Codex prompts;
- upgrade, verification, resume, and runtime-agent prompts.

The tested localized public prompt set is `00`, `01`, `05`, `06`, `07`, `08`, `09`, and `15`. Other prompts are internal/canonical workflows and are not promised as translated entry points.

An installed project can ask Codex to speak with the user in English. The technical method remains canonical in English.

---

## What this pack is not

This pack is not:

- an agentic framework;
- an automatic application generator without supervision;
- a guarantee that Codex will never make mistakes;
- a replacement for tests;
- a replacement for product validation;
- a tool that allows AI to decide business rules alone.

It is a controlled execution method to make AI-assisted development more reliable, more auditable, and easier to resume.

---

## Documentation

Main documentation:

- [SR Method](https://docs.auroramind.fr/docs/SR_Method)
- [English documentation](https://docs.auroramind.fr/docs/SR_Method/en)

Useful pages:

- Understand the SR Method
- Start with Codex
- Work by lots
- Gates and validation
- Codex skills
- Codex Project Pack
- Main SR files
- SR contracts
- Runtime AI agents
- Closure, E2E tests, and GitHub

---

## License

This repository is published under the **MIT** license.

See [LICENSE](LICENSE).

---

## Contributing

Contributions are welcome when they strengthen the method without making it heavier.

Useful areas:

- improve multilingual prompts;
- add verification checklists;
- enrich lot templates;
- improve audit scripts;
- document real use cases;
- propose reusable method or domain skills.

Before contributing, keep the project philosophy in mind:

> less improvisation, more evidence, more resumability.
