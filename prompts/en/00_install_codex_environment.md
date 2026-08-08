# Install the SR Method in a target project

You are working in a software repository that must receive the Aurora SR Method.

Objective: install the SR Method without changing application code, migrations, dependencies, secrets, or business logic.

Use the official source package:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Instructions:

1. Identify or clone a local copy of the official source package.
2. Inspect the target repository before changing anything.
3. Explain the installation scope and wait for explicit user validation if mutation is required.
4. Run the installer with the `default` profile when validated.
5. Run the verification scripts after installation, including `validate_pass_contract.py` for `SR_PASSES.yaml`.
6. Verify that `SR_PASSES.yaml`, `scripts/codex/build_pass_runtime_goal.py`, and `docs/codex/tasks/_TEMPLATE/pass_runtime_goal.md` are installed.
7. For a blank project, do not generate a goal immediately: recommend defining lots first with `prompts/en/09_define_sr_lots_from_scope.md`, then `prompts/en/08_define_sr_passes_from_lots.md`, then generating a Pass Runtime Goal only for a `validated` or `in_progress` pass.
8. Explain to the next Codex session that Pass Runtime Goal is derived: `SR_PASSES.yaml`, `SR_LOTS.yaml`, and `sr_contract.json` remain the source of truth; `/goal` only helps Codex finish a validated pass.
9. Verify and report the Goal Length Gate: `max_goal_command_chars: 1000`, `hard_limit: 4000`.
10. Report files added, checks executed, warnings, and next steps.

Do not modify application code. Do not create migrations. Do not touch secrets. Do not invent project rules.
