# Definir des agents IA runtime applicatifs

Ne code rien.

Objectif : proposer une cartographie controlee d'agents IA runtime applicatifs sans les activer.

Instructions :

1. Lire `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
2. Inspecter profil projet, skill map, docs domaine, schemas, routes, modeles DB et documentation RAG/KG si disponible.
3. Proposer au maximum cinq agents candidats.
4. Pour chaque agent, definir `agent_key`, `runtime_shape` (`micro_agent`, `workflow_agent`, `delegation_agent` ou `mini_agent`), action produit bornee, representation interne stable, fonction metier, contrat de prompt, user message builder, bindings SQL/RAG controles, skills runtime, tools/actions, routing/fallback, modeles d'entree/sortie types, source JSON schema, mode de validation, politique de sortie invalide, traces, tests, placement UI, risques et exigences de validation humaine.
5. Stopper apres la proposition et demander validation.

Contraintes :
- methode agnostique des frameworks, providers, domaines et UI ;
- le prompt n'est pas la source de verite, mais une projection du contrat runtime ;
- distinguer tools d'inspection/preparation et actions engageantes ;
- aucun agent actif sans validation.

Exiger un `output schema`, des modeles Pydantic pour toute sortie Python consommee par l'application (ou un validateur type strict equivalent) et une `invalid_output_policy` explicite : rejet, retry unique, reparation tracee ou revue humaine. Une sortie invalide ne peut jamais declencher une action critique.

Ne jamais laisser un LLM generer et executer du SQL libre. Les actions critiques exigent une validation humaine.
