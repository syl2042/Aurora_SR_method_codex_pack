# Definir les agents IA runtime

Ne code rien.

Lire :
- `docs/codex/AI_AGENT_RUNTIME_METHOD.md`
- `docs/codex/DOMAIN_EXPERTISE_BOOTSTRAP.md`
- PROJECT_PROFILE
- SKILL_MAP
- docs/domain
- AIP/export domaine si disponible
- schemas, routes, modeles DB, documentation Nexus/RAG

Objectif : proposer une cartographie d'agents IA applicatifs sans les activer.

Pour chaque agent candidat, produire :
- `agent_key`
- `label`
- `purpose`
- `business_function_key`
- `runtime_shape` (`micro_agent`, `workflow_agent`, `delegation_agent` ou `mini_agent`)
- `product_action_scope`
- `internal_representation_contract`
- priorite
- modele recommande
- temperature
- `prompt_contract`
- system prompt
- user prompt template
- `user_message_builder`
- bindings SQL justifies
- bindings Nexus/RAG justifies
- skills runtime requises
- `tools_and_actions`
- `routing_policy` si plusieurs agents ou intentions peuvent repondre
- output schema
- input model Pydantic ou validateur type equivalent
- output model Pydantic ou validateur type equivalent
- source du JSON schema (`generated_from_output_model`, `manual_schema` ou `external_contract`)
- mode de validation (`pydantic_strict`, `typed_validator_strict` ou `manual_json_schema`)
- politique d'echec (`reject`, `retry_once`, `repair_with_trace` ou `human_review`)
- champ machine `invalid_output_policy` aligne sur cette politique
- traces d'erreur de validation non sensibles
- cas de test
- tests de sortie typee :
  - sortie valide
  - JSON malforme
  - champ obligatoire absent
  - type incorrect
  - enum invalide
  - champ inattendu si contrat ferme
  - sortie partielle
  - action critique interdite si sortie invalide
- placement UI
- risques
- validation humaine requise

Contraintes :
- maximum 5 agents candidats en V1 ;
- methode agnostique des frameworks, providers, domaines et UI ;
- le prompt n'est pas la source de verite : il est une projection du contrat runtime ;
- chaque agent doit servir une action produit bornee ou justifier pourquoi ce n'est pas possible ;
- chaque agent doit declarer la representation interne stable qu'il lit, produit ou modifie ;
- distinguer tools d'inspection/preparation et actions qui engagent l'UI, l'etat, une ecriture, une notification ou un artefact ;
- definir fallback et refus possibles quand le routage ou le perimetre sont incertains ;
- aucun agent actif sans validation ;
- output schema obligatoire ;
- Pydantic obligatoire pour backend Python si la sortie est consommee par l'application ;
- validateur type equivalent obligatoire hors Python ;
- le JSON du LLM est une proposition et ne devient donnee applicative qu'apres validation runtime stricte ;
- aucune action critique ne peut partir d'une sortie reparee automatiquement sans validation humaine ;
- cas de test obligatoires ;
- pas de SQL libre genere puis execute par LLM ;
- actions critiques sous validation humaine.

Stop apres proposition et questions de validation.
