# Definir les lots SR depuis un cadrage ou une inbox

Tu travailles dans un repo equipe de la SR Method.

Objectif : transformer un cadrage, une demande utilisateur ou `docs/codex/SR_INBOX.yaml` en lots SR explicites dans `docs/codex/SR_LOTS.yaml`, sans modifier le code applicatif.

Avant de creer un lot, verifier objectifs, criteres d'acceptation, `validated_requests`, lots `user_testing` et passes validees. Si le besoin est deja couvert, classer `existing_requirement_repair`/clarification/acceptance et rouvrir ou amender le lot d'origine. Un nouveau lot exige une justification explicite du scope reellement nouveau ; ne jamais creer un micro-lot par critere d'une meme demande produit.

Regles :

- Ne modifie aucun code applicatif.
- Ne cree pas de lot `planned`, `validated`, `in_progress`, `repair` ou `reopened` sans Lot Design Evidence Gate.
- Un lot `proposed` peut capturer une piste ou une hypothese non encore verifiee.
- Ne marque jamais un lot `validated` sans validation utilisateur explicite.
- Ne renomme pas les lots legacy.

Sources a lire :

1. `AGENTS.md`
2. `docs/codex/SR_BOOTSTRAP.md`
3. `docs/codex/SR_HARNESS_METHOD.md`
4. `docs/codex/LOT_EXECUTION_METHOD.md`
5. `docs/CURRENT_STATE.md`
6. `docs/codex/SR_INBOX.yaml` si present
7. `docs/codex/SR_LOTS.yaml` si present
8. `docs/codex/CODEBASE_MAP.md`
9. `docs/codex/CODEBASE_MAP.generated.md` si la carte courte ne suffit pas
10. Les fichiers code candidats quand ils peuvent confirmer le cadrage

Methode :

1. Classer la demande : nouvelle fonction, bug, dette, decision produit, reprise, migration, integration, UI, backend, DB, agent runtime ou documentation.
2. Identifier les surfaces candidates avec `RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs`.
3. Pour chaque lot candidat, remplir `design_evidence` :
   - `status: pass` si les fichiers utiles ont ete lus ;
   - `status: not_applicable` seulement avec `not_applicable_reason` ;
   - `status: pending` si le lot reste exploratoire en `proposed`.
4. Definir des lots courts avec objectif, criteres d'acceptation, chemins autorises/interdits, dependances, stop conditions et commandes de verification.
5. Garder en `proposed` tout lot dont le cadrage depend encore d'une supposition verifiable.
6. Proposer les lots a valider avant execution.
7. Valider `SR_LOTS.yaml` avec `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml`.
8. Recommander ensuite `docs/codex/prompts/08_define_sr_passes_from_lots.md` si plusieurs lots sont executables ou proches de l'etre.

Sortie attendue :

- lots crees ou modifies ;
- statut de chaque Lot Design Evidence Gate ;
- fichiers candidats et fichiers lus ;
- hypotheses restantes ;
- questions bloquantes ;
- validation `SR_LOTS.yaml` ;
- passes a definir ensuite ou raison de ne pas le faire.
