# Definir les lots SR depuis un cadrage ou une inbox

Objectif : transformer un cadrage, une demande utilisateur ou `docs/codex/SR_INBOX.yaml` en lots SR explicites dans `docs/codex/SR_LOTS.yaml`, sans modifier le code applicatif.

Regles :

- Ne modifie aucun code applicatif.
- Ne cree pas de lot `planned`, `validated`, `in_progress` ou `reopened` sans Lot Design Evidence Gate.
- Un lot `proposed` peut rester exploratoire.
- Ne marque jamais un lot `validated` sans validation utilisateur explicite.

Methode :

1. Lire `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md`, `docs/codex/SR_HARNESS_METHOD.md`, `docs/codex/LOT_EXECUTION_METHOD.md`, `docs/CURRENT_STATE.md`, `docs/codex/SR_INBOX.yaml`, `docs/codex/SR_LOTS.yaml` et `docs/codex/CODEBASE_MAP.md` quand ils existent.
2. Identifier les surfaces candidates avec `RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs`.
3. Remplir `design_evidence` pour chaque lot candidat.
4. Garder en `proposed` tout lot dont le cadrage depend encore d'une supposition verifiable.
5. Proposer les lots a valider avant execution.
6. Valider `SR_LOTS.yaml` avec `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml`.
7. Recommander ensuite `docs/codex/prompts/08_define_sr_passes_from_lots.md` si plusieurs lots sont executables ou proches de l'etre.

Sortie attendue : lots crees ou modifies, statut du Lot Design Evidence Gate, fichiers lus, hypotheses restantes, questions bloquantes, validation `SR_LOTS.yaml`, prochaine etape.
