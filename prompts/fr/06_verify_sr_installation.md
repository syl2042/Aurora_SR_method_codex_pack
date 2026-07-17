# Verifier une installation SR Method

Tu travailles dans un repository equipe de la Aurora SR Method.

Objectif : verifier que l'installation ou l'upgrade est complet, coherent et utilisable avant reprise du developpement.

Instructions :

1. Lancer `python3 scripts/codex/verify_codex_pack.py`.
2. Lancer `python3 scripts/codex/audit_codex_pack.py --root . --json`.
3. Lancer `python3 scripts/codex/sr_post_install_check.py --root . --json` si disponible.
4. Valider les contrats lot, passe, loop et SR quand les scripts existent.
5. Executer `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` si `SR_PASSES.yaml` existe.
6. Classer les warnings restants : acceptables, a documenter, a corriger avec validation ou bloquants.
7. Rapporter version, controles, erreurs, warnings, statut `SR_PASSES.yaml` et prochaine action recommandee.

Ce n'est pas une passe de developpement applicatif.
