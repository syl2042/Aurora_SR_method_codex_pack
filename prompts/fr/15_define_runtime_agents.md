# Definir des agents IA runtime applicatifs

Ne code rien.

Objectif : proposer une cartographie controlee d'agents IA runtime applicatifs sans les activer.

Instructions :

1. Lire `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
2. Inspecter profil projet, skill map, docs domaine, schemas, routes, modeles DB et documentation RAG/KG si disponible.
3. Proposer au maximum cinq agents candidats.
4. Pour chaque agent, definir purpose, fonction metier, contrat de prompt, bindings SQL/RAG controles, skills runtime, modeles d'entree/sortie types, source JSON schema, mode de validation, politique de sortie invalide, traces, tests, placement UI, risques et exigences de validation humaine.
5. Stopper apres la proposition et demander validation.

Ne jamais laisser un LLM generer et executer du SQL libre. Les actions critiques exigent une validation humaine.
