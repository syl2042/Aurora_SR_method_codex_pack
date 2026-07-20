# Verification

- `python3 -m unittest discover scripts/codex -p 'test_*.py'` : OK, 45 tests.
- `python3 scripts/codex/validate_lot_contract.py --file docs/codex/examples/sr_lots_interpass_dependencies.yaml` : OK, 2 lots.
- `python3 scripts/codex/validate_pass_contract.py --file docs/codex/examples/sr_passes_interpass_dependencies.yaml --lots-file docs/codex/examples/sr_lots_interpass_dependencies.yaml` : OK, 2 passes.
- `python3 scripts/codex/validate_pass_contract.py --file blueprints/sr_passes.template.yaml --lots-file blueprints/sr_lots.template.yaml` : OK, 1 passe.
- Smoke audit temporaire avec installation du pack puis remplacement de `SR_LOTS.yaml`/`SR_PASSES.yaml` par le scenario inter-passes : OK, `audit_sr_project.py --root <tmp>` vert.
- `python3 scripts/codex/verify_codex_pack.py` : OK.
- `python3 scripts/codex/audit_codex_pack.py` : OK.
- Smoke post-install temporaire : OK, `installed_version: 3.2.1`, `expected_version: 3.2.1`; warning non bloquant sur `context_budget_report.py` dans le repertoire temporaire.
- `git diff --check` : OK.
