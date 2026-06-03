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
- priorite
- modele recommande
- temperature
- system prompt
- user prompt template
- bindings SQL justifies
- bindings Nexus/RAG justifies
- skills runtime requises
- output schema
- input model Pydantic ou validateur type equivalent
- output model Pydantic ou validateur type equivalent
- source du JSON schema (`generated_from_output_model`, `manual_schema` ou `external_contract`)
- mode de validation (`pydantic_strict`, `typed_validator_strict` ou `manual_json_schema`)
- politique d'echec (`reject`, `retry_once`, `repair_with_trace` ou `human_review`)
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
