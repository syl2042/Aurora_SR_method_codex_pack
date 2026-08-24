---
name: aurora-lot-runner
description: >-
  utiliser quand l'utilisateur demande d'executer une roadmap, un gros brief, plusieurs lots, une reprise longue, une phase autonome bornee ou une nouvelle fonction non triviale. Orchestre SR_INBOX, SR_LOTS, CURRENT_STATE, task memory, evidence_gate, design_gate, ui_test_readiness_gate, ui_visual_evidence_gate, context_budget_gate, verification, gate_report et les skills methode existantes pour classer la demande, choisir le prochain lot, limiter le scope, mettre a jour le backlog vivant et decider continuer, reparer ou stopper.
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
5. `docs/codex/SR_PASSES.yaml` si present
6. `docs/codex/SR_INBOX.yaml` si present
7. `docs/codex/SR_CONTEXT_PACK.md` si present
8. `docs/codex/SKILL_MAP.md`
9. RepoMap et sources du lot courant
10. Nexus KG/context pack si `PROJECT_PROFILE.yaml` active le mode `nexus_kg`

## Classification obligatoire

Avant de coder, chercher si le besoin est deja couvert par un objectif, un critere d'acceptation, une `validated_request`, un lot `user_testing` ou une passe validee, puis classer la demande :

- `existing_requirement_repair` ;
- `existing_requirement_clarification` ;
- `existing_requirement_acceptance` ;
- `new_requirement` ;
- `scope_change` ;
- `cancelled_requirement`.

Un retour sur une fonction validee est par defaut `existing_requirement_repair`, pas `new_requirement`. Rattacher le retour au `requirement_id`, rouvrir le lot d'origine, heriter de toutes ses exigences ouvertes et executer la reprise consolidee. Un nouveau lot exige une justification explicite prouvant que la demande est hors scope existant et une decision utilisateur.

## Boucle d'execution

1. Recharger le registre `validated_requests`, son parent et tous les identifiants ouverts avant de selectionner le prochain lot.
2. Selectionner le prochain bloc coherent : lots `repair`/`reopened`, puis `validated`, sans creer un micro-lot par critere.
3. Creer ou reprendre une task memory et un `sr_contract.json` 3.1.0.
4. Appliquer `pass_planning_gate` avant toute execution multi-lots.
5. Appliquer `evidence_gate` avant plan ou faisabilite.
6. Appliquer `knowledge_gate` : RepoMap/KG -> fichiers candidats -> lecture code reel.
7. Selectionner les skills utiles :
   - `aurora-planning-with-files`
   - `aurora-diagnose` si bug
   - `aurora-tdd` si test automatisable
   - `aurora-architecture-check` si structurant
   - `aurora-repomap-maintainer` si structure change
   - `aurora-review-diff` avant cloture
   - `aurora-ui-visual-qa` si UI/UX significative
   - skill metier locale si domaine
   - skill design si UI et disponible
8. Implementer dans le scope du lot ou de la passe.
9. Lancer les verifications.
10. Corriger au maximum selon `max_repair_attempts_per_lot`.
11. Appliquer `self_evaluation_gate`.
12. Produire `gate_report.md`.
13. Produire et valider `sr_contract.json`, puis `loop_contract.json` 1.1 lie au meme registre, avec les validateurs disponibles.
14. Valider `SR_PASSES.yaml` avec `scripts/codex/validate_pass_contract.py` si une passe a ete creee, modifiee ou utilisee.
15. Mettre a jour `SR_LOTS.yaml`, `SR_PASSES.yaml`, task memory, RepoMap/KG et `CURRENT_STATE.md` si necessaire.
16. Continuer seulement si le niveau d'autonomie l'autorise et que les gates critiques sont verts.

## Gates minimales

- `evidence_gate` : verifier les fichiers avant suppositions.
- `pass_planning_gate` : avant multi-lots, verifier ordre, dependances, preflight, validations humaines et E2E groupe.
- `knowledge_gate` : utiliser RepoMap, puis KG si actif, avant de choisir les fichiers.
- `scope_gate` : respecter `allowed_paths` / `forbidden_paths`.
- `spec_gate` : couvrir les criteres d'acceptation.
- `verification_gate` : executer ou documenter les verifications.
- `self_evaluation_gate` : relire diff/fichiers, verifier preuves, risques et oublis possibles.
- `loop_contract_gate` : verifier que `loop_contract.json` declare status, preuves, fichiers modifies, verifications, E2E utilisateur, memoire, budget contexte et decision de transition conversationnelle.
- `requirement_registry_gate` : separer implementation et preuve, calculer le statut depuis chaque demande et heriter sans perte de toutes les exigences ouvertes lors d'une reprise.
- `design_gate` : obligatoire pour UI non triviale.
- `ui_test_readiness_gate` : obligatoire pour UI non triviale quand `ui_validation.required` vaut `true`.
- `ui_visual_evidence_gate` : obligatoire avant cloture `done` d'un lot UI significatif.
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

- commencer par `Demande utilisateur | Etat | Preuve | Reste a faire` ;
- lots traites ;
- statut backlog mis a jour ;
- fichiers touches ;
- verifications executees ;
- gates OK/KO ;
- loop contract OK/KO ;
- decision self evaluation : done / user_testing / repair / blocked ;
- risques restants ;
- prochain bloc coherent recommande.

Ne jamais qualifier la passe de terminee, complete, livree ou implementee si son Completion Gate est rouge. `user_testing` est reserve aux exigences techniquement completes auxquelles il manque seulement un E2E ou une acceptation humaine.
