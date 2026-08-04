# Verification - SR propagation gate

| Commande | Resultat | Notes |
|---|---|---|
| `python3 -m unittest test_validate_sr_contract.py test_validate_loop_contract.py test_audit_sr_task_contracts.py` depuis `scripts/codex` | OK | 31 tests. |
| `python3 scripts/codex/validate_loop_contract.py --file tasks/_TEMPLATE/loop_contract.json` | OK | Template Loop Contract valide. |
| `python3 scripts/codex/validate_sr_contract.py --file tasks/_TEMPLATE/sr_contract.json` | OK | Template SR Contract valide. |
| `python3 scripts/codex/audit_codex_pack.py --root .` | OK | Source alignee sur 3.3.0. |
| `python3 scripts/codex/verify_codex_pack.py` | OK | Marqueurs source presents. |
| Installation temporaire via `scripts/install_codex_pack.py`, puis `sr_post_install_check.py --no-report` | OK | Version installee 3.3.0 ; warning context budget non bloquant dans le repo temporaire vide. |
| `rg -n "3\\.2\\.2|TARGET_VERSION|EXPECTED_VERSION|Propagation Gate|propagation_gate" core prompts tasks blueprints profiles scripts MANIFEST.json` | OK | Plus de cible 3.2.2 active ; references Propagation Gate presentes. |
| `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/2026-08-04_sr-propagation-gate/sr_contract.json` | OK | Contrat SR du lot valide. |
| `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/2026-08-04_sr-propagation-gate/loop_contract.json` | OK | Loop Contract du lot valide. |
| `git diff --check` | OK | Aucun whitespace error. |
