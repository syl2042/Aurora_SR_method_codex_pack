---
name: aurora-lot-runner
description: >-
  utiliser quand l'utilisateur demande d'executer une roadmap, un gros brief, plusieurs lots, une reprise longue, une phase autonome bornee ou une nouvelle fonction non triviale. Orchestre SR_INBOX, SR_LOTS, CURRENT_STATE, task memory, evidence_gate, design_gate, context_budget_gate, verification, gate_report et les skills methode existantes pour classer la demande, choisir le prochain lot, limiter le scope, mettre a jour le backlog vivant et decider continuer, reparer ou stopper.
---

# Role

Orchestrer une execution SR-Harness bornee sans remplacer les skills existantes.

## Declenchement

Utiliser si :

- l'utilisateur demande de traiter plusieurs lots ;
- l'utilisateur demande de travailler en autonomie ;
- une nouvelle fonction doit etre cadree en lots ;
- une demande semble rouvrir un lot existant ;
- un bug ou retour test doit etre rattache au backlog ;
- la session reprend apres compact, handoff ou longue interruption ;
- le projet contient `docs/codex/SR_LOTS.yaml` ou `docs/codex/SR_INBOX.yaml`.

## Sources a lire

Lire uniquement ce qui est utile :

1. `docs/codex/SR_HARNESS_METHOD.md`
2. `docs/codex/LOT_EXECUTION_METHOD.md`
3. `docs/CURRENT_STATE.md`
4. `docs/codex/SR_LOTS.yaml` si present
5. `docs/codex/SR_INBOX.yaml` si present
6. `docs/codex/SR_CONTEXT_PACK.md` si present
7. `docs/codex/SKILL_MAP.md`
8. RepoMap et sources du lot courant
9. Nexus KG/context pack si `PROJECT_PROFILE.yaml` active le mode `nexus_kg`

## Classification obligatoire

Avant de coder, classer la demande :

- nouveau lot ;
- lot existant a rouvrir ;
- bug/regression ;
- decision produit ;
- question de faisabilite ;
- demande de plan ;
- execution d'un lot valide ;
- phase multi-lots bornee.

Si la demande modifie le backlog, proposer ou effectuer la mise a jour de `SR_INBOX.yaml` ou `SR_LOTS.yaml` selon le risque.

## Boucle d'execution

1. Selectionner le prochain lot executable.
2. Creer ou reprendre une task memory.
3. Appliquer `evidence_gate` avant plan ou faisabilite.
4. Appliquer `knowledge_gate` : RepoMap/KG -> fichiers candidats -> lecture code reel.
5. Selectionner les skills utiles :
   - `aurora-planning-with-files`
   - `aurora-diagnose` si bug
   - `aurora-tdd` si test automatisable
   - `aurora-architecture-check` si structurant
   - `aurora-repomap-maintainer` si structure change
   - `aurora-review-diff` avant cloture
   - skill metier locale si domaine
   - skill design si UI et disponible
6. Implementer dans le scope du lot.
7. Lancer les verifications.
8. Corriger au maximum selon `max_repair_attempts_per_lot`.
9. Appliquer `self_evaluation_gate`.
10. Produire `gate_report.md`.
11. Produire et valider `loop_contract.json` avec `scripts/codex/validate_loop_contract.py` si disponible.
12. Mettre a jour `SR_LOTS.yaml`, task memory, RepoMap/KG et `CURRENT_STATE.md` si necessaire.
13. Continuer seulement si le niveau d'autonomie l'autorise et que les gates critiques sont verts.

## Gates minimales

- `evidence_gate` : verifier les fichiers avant suppositions.
- `knowledge_gate` : utiliser RepoMap, puis KG si actif, avant de choisir les fichiers.
- `scope_gate` : respecter `allowed_paths` / `forbidden_paths`.
- `spec_gate` : couvrir les criteres d'acceptation.
- `verification_gate` : executer ou documenter les verifications.
- `self_evaluation_gate` : relire diff/fichiers, verifier preuves, risques et oublis possibles.
- `loop_contract_gate` : verifier que `loop_contract.json` declare status, preuves, fichiers modifies, verifications, E2E utilisateur, memoire, budget contexte et decision de transition conversationnelle.
- `design_gate` : obligatoire pour UI non triviale.
- `context_budget_gate` : rapport contexte, handoff ou prompt de reprise si orange/rouge, 2 lots ou 20 tours utilisateur, puis decision `conversation_transition`.
- `nexus_context_gate` : utiliser un context pack court si Nexus/RAG est pertinent.

## Stop conditions

Stopper si :

- validation humaine requise ;
- lot `proposed` ou `planned` non valide pour un changement significatif ;
- migration, dependance ou architecture non specifiee ;
- regle metier absente ;
- action sensible non encadree ;
- tests bloquants apres tentatives autorisees ;
- scope impossible a respecter ;
- contexte trop long sans handoff.

## Sortie attendue

Pendant l'execution, rester concis.

En cloture :

- lots traites ;
- statut backlog mis a jour ;
- fichiers touches ;
- verifications executees ;
- gates OK/KO ;
- loop contract OK/KO ;
- decision self evaluation : done / user_testing / repair / blocked ;
- risques restants ;
- prochain lot recommande.
