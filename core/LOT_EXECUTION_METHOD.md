# LOT_EXECUTION_METHOD — index SR 4

Boucle lot : appliquer les routes dans l’ordre intake, evidence, plan, implementation, verification et cloture.

Entree canonique : `SR_BOOTSTRAP.md`. Les details normatifs sont dans `procedures/`. Ne pas charger tous les modules.

- Fait verifiable dans une reponse non triviale : `procedures/fact.md`
- Recommandation technique ou plan engageant : `procedures/evidence.md`
- Creation/reprise de memoire avant mutation non triviale : `procedures/memory.md`, `procedures/contracts.md`
- Nouvelle demande, retour utilisateur, lot executable : `procedures/design-evidence.md`, `procedures/execution.md`
- Fonction structurante / mutation backlog / dependances : `procedures/impact.md`
- Symbole, schema, API, config ou composant partage change : `procedures/propagation.md`
- UI significative : `procedures/ui.md`
- Plusieurs lots / passe : `procedures/passes.md`
- Passe executee avec /goal : `procedures/runtime-goal.md`
- Agent IA / LLM / prompt / RAG / outil runtime : `procedures/skills.md`
- Apres patch / verification : `procedures/verification.md`
- Cloture / changement de statut : `procedures/completion.md`, `procedures/contracts.md`
- Avancement significatif / cloture / risque de contexte : `procedures/context.md`
- Pause, handoff, prochaine conversation : `procedures/resume.md`, `procedures/context.md`

Les contrats et validateurs restent inchanges : validate_sr_contract.py, validate_loop_contract.py, validate_lot_contract.py, validate_pass_contract.py. build_pass_runtime_goal.py pour /goal. SR_PASSES.yaml et ui_validation restent applicables.
