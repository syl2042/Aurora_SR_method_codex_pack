# task_plan.md

## Objectif verifiable
Ajouter a la SR Method un Propagation Gate / Reference Integrity Gate qui oblige Codex a annoncer avant mutation les impacts probables d'un changement de symbole ou de contrat partage, demander validation humaine si le risque depasse le local, puis verifier apres mutation que les references, appels, imports/exports, signatures et consommateurs impactes ont ete propages ou justifies.

## Bootstrap SR
- SR_BOOTSTRAP lu : oui
- Reprise apres compact/resume/handoff : non
- Derniere memoire de tache consultee : oui, `docs/codex/tasks/2026-07-22_lot-completion-gate/`

## Hypotheses
- Le depot courant est le pack source SR, sans `AGENTS.md` local ni `SR_LOTS.yaml` vivant ; les blueprints et templates sont la source de distribution.
- Le changement est methodologique et contractuel, pas applicatif.
- La migration doit etre additive : les anciens contrats historiques restent auditables sans devenir bloquants.
- Le nouveau gate doit etre strict pour les nouveaux templates et contrats crees apres upgrade.

## Type de tache
- [ ] UI
- [ ] Backend
- [ ] DB/migration
- [ ] Integration
- [ ] Securite
- [x] Documentation
- [x] Architecture
- [ ] Bugfix
- [x] Domaine metier

## Skills utilisees
- aurora-lot-runner
- aurora-planning-with-files
- aurora-architecture-check
- aurora-tdd
- aurora-review-diff
- aurora-repomap-maintainer

## Skills metier Codex
- Skill metier pertinente selectionnee : non applicable
- Si non, skill a proposer : non applicable
- Sources domaine lues : non applicable

## Sources lues
- [x] Instructions globales utilisateur
- [x] `core/SR_BOOTSTRAP.md`
- [x] `core/LOT_EXECUTION_METHOD.md`
- [x] `core/SR_HARNESS_METHOD.md`
- [x] `core/SR_METHOD.md`
- [x] `tasks/_TEMPLATE/*.md`
- [x] `tasks/_TEMPLATE/*.json`
- [x] `scripts/codex/validate_loop_contract.py`
- [x] `scripts/codex/validate_sr_contract.py`
- [x] `scripts/codex/audit_sr_task_contracts.py`
- [x] memoire `2026-07-22_lot-completion-gate`

## RepoMap
- CODEBASE_MAP.md lu : oui, carte source courte minimale
- generated consulte : oui
- fichiers candidats : `core/**`, `tasks/_TEMPLATE/**`, `blueprints/**`, `prompts/**`, `profiles/default/**`, `scripts/install_codex_pack.py`, `scripts/codex/**`
- fichiers verifies : docs methode, templates, validateurs, audits, post-install checks
- RepoMap a mettre a jour : non, la carte source courte reste generique ; la carte generee existante couvre deja les scripts SR concernes.

## Knowledge mode
- Mode : `core`
- Nexus KG consulte : non disponible
- Fraicheur KG verifiee : non disponible
- Context pack Nexus requis : non
- KG a mettre a jour en cloture : non applicable

## Lot naming
- Lot ID : SR-METHOD-323-PROPAGATION-GATE
- Conforme `<PROJECT_KEY>-<AREA>-<SEQ>` : legacy methode
- Alias legacy :

## Perimetre valide et Lot Completion Gate
- Lot/passe valide explicitement : oui
- Source de validation : utilisateur, 2026-08-04, message `je valide`
- Perimetre decrit juste avant validation : ajouter le Propagation Gate a la methode SR, aux contrats, templates, validateurs, audits, prompts et strategie d'upgrade multi-projets sans regression applicative.
- Reduction/decoupage necessaire avant mutation : non
- Si oui, nouvelle validation utilisateur obtenue : non applicable

| Exigence validee | Preuve minimale prevue | Risque de couverture | Statut attendu |
|---|---|---|---|
| Preflight d'impact avant mutation | docs methode + templates | moyen | fait |
| Validation humaine si risque non local | docs methode + contrats | moyen | fait |
| Postcheck de propagation apres mutation | docs methode + gate_report + contrats | moyen | fait |
| Blocage de `done` si gate requis incomplet | validateurs + tests | fort | fait |
| Upgrade additif et legacy-compatible | audit + prompts upgrade + post-install | fort | fait |
| Guidance Codex installes sur prochains lots | AGENTS template + prompts | moyen | fait |
| Tests de non-regression validateurs | unittest cible | moyen | fait |

- Exigence UI/UX explicite : non
- Verification visuelle ou E2E prevue : non applicable

## Propagation Gate du lot courant
- Requis : oui
- Risque : high
- Preflight : cette modification touche des contrats JSON, validateurs, templates, prompts et audits du pack source.
- Validation humaine recue : oui, utilisateur 2026-08-04.
- Strategie : changement additif avec compatibilite legacy pour les anciennes task memories.
- Postcheck prevu : `rg propagation_gate`, validation templates, tests validateurs, audit pack, post-install check.

## Context budget
- `context_budget_report.py --root . --compact` execute : non disponible/non requis dans le pack source
- Statut contexte hybride : not_checked
- Selection session fiable : non applicable
- Cached/uncached consultes : non
- Signaux hybrides : non applicable
- `NEXT_SESSION_PROMPT.md` requis : non
- Si `green`, statut masque dans la reponse utilisateur : non applicable

## Plan court
1. Ajouter le Propagation Gate aux documents methode et consignes Codex.
2. Ajouter les champs aux templates `task_plan`, `gate_report`, `loop_contract.json`, `sr_contract.json` et au blueprint `SR_LOTS`.
3. Renforcer `validate_loop_contract.py` et `validate_sr_contract.py` avec un validateur proportionne.
4. Mettre a jour les audits/post-install/verification pack et les prompts d'upgrade/cloture.
5. Ajouter les tests unitaires legacy et stricts.
6. Mettre a jour la version pack en 3.3.0.
7. Valider templates, tests et audit pack.

## Verification prevue
- `python3 -m unittest scripts/codex/test_validate_sr_contract.py scripts/codex/test_validate_loop_contract.py scripts/codex/test_audit_sr_task_contracts.py`
- `python3 scripts/codex/validate_sr_contract.py --file tasks/_TEMPLATE/sr_contract.json`
- `python3 scripts/codex/validate_loop_contract.py --file tasks/_TEMPLATE/loop_contract.json`
- `python3 scripts/codex/audit_codex_pack.py --root .`
- `python3 scripts/codex/verify_codex_pack.py`
- `python3 scripts/codex/sr_post_install_check.py --root . --json`
- `rg -n "Propagation Gate|propagation_gate|reference integrity|Reference Integrity" core tasks blueprints prompts scripts`
- `git diff --check`
