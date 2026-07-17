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
6. Verify that `SR_PASSES.yaml` is installed and recommend `prompts/en/08_define_sr_passes_from_lots.md` after lots are defined.
7. Report files added, checks executed, warnings, and next steps.

Do not modify application code. Do not create migrations. Do not touch secrets. Do not invent project rules.
