# AI_AGENT_RUNTIME_METHOD.md

Alias historique : ce document decrit la **SR Agent Method**, branche de la SR Method dediee aux agents IA runtime applicatifs.

## Objectif
Definir comment Codex doit concevoir les agents IA applicatifs dans les projets qui utilisent la methode SR.

Cette methode concerne les agents IA embarques dans l'application. Elle ne remplace pas les skills Codex, qui servent a guider Codex pendant le developpement.

## Principe central
Ne pas fonder la V1 sur un framework agent lourd.
Utiliser un pattern backend-first, explicite, testable et validable :

```text
modele LLM
+ system prompt
+ user prompt template
+ variables injectees
+ bindings SQL controles
+ bindings Nexus/RAG optionnels
+ skills runtime
+ output contract
+ Pydantic input/output models ou validateur type equivalent
+ JSON schema expose au LLM
+ validation runtime stricte
+ retry/repair policy
+ traces d'erreur de validation
+ traces
+ validation humaine si necessaire
```

## Contrat minimal d'un agent
Chaque agent runtime doit etre decrit avec :
- `agent_key`
- `label`
- `purpose`
- `business_function_key`
- `model_provider`
- `model`
- `temperature`
- `execution_mode`
- `system_prompt`
- `user_prompt_template`
- `input_schema`
- `output_schema`
- `input_model`
- `output_model`
- `json_schema_source`
- `output_validation_mode`
- `invalid_output_policy`
- `validation_error_trace`
- `sql_context_bindings`
- `nexus_context_bindings`
- `required_runtime_skills`
- `ui_placement`
- `test_cases`
- `typed_output_tests`
- `risk_notes`
- `human_validation_required`
- `validation_status`
- `is_active`

Champs recommandes :
- `input_model` : modele Pydantic ou equivalent qui decrit les entrees normalisees de l'agent ;
- `output_model` : modele Pydantic ou equivalent qui decrit la sortie acceptee par l'application ;
- `json_schema_source` : `generated_from_output_model`, `manual_schema` ou `external_contract` ;
- `output_validation_mode` : `pydantic_strict`, `typed_validator_strict` ou `manual_json_schema` ;
- `invalid_output_policy` : `reject`, `retry_once`, `repair_with_trace` ou `human_review` ;
- `validation_error_trace` : emplacement ou format des traces d'erreur non sensibles.

## Sortie structuree
Un agent ne doit pas produire uniquement une reponse finale textuelle si l'application doit la consommer.
Le format cible recommande est :

```json
{
  "business_result": {},
  "ui_response": {},
  "trace": {}
}
```

Adapter les champs au domaine, mais conserver :
- un resultat metier exploitable ;
- une representation UI controlee par le frontend ;
- une trace courte des sources, limites et validations.

La sortie JSON du LLM est une proposition, pas une donnee applicative fiable. Le `output JSON schema` guide le modele, mais la sortie doit etre validee cote backend avant consommation par l'application.

## Pydantic Output Contract

Pour un backend Python, toute sortie d'agent IA runtime consommee par l'application doit passer par un modele Pydantic. Pour une autre stack, utiliser un validateur type equivalent avec les memes garanties.

Flux cible :

```text
Pydantic model ou equivalent
-> JSON schema expose au LLM
-> reponse JSON du LLM
-> validation runtime stricte
-> objet applicatif valide
```

Regles obligatoires :
- generer le JSON schema depuis le modele type quand c'est possible ;
- valider avec `model_validate_json`, `model_validate` ou l'equivalent strict du framework utilise ;
- refuser ou tracer les champs inconnus quand le contrat de sortie est ferme ;
- utiliser des types explicites, enums et bornes pour les champs critiques ;
- ne jamais persister, afficher comme fait etabli ou utiliser pour une action critique une sortie non validee ;
- conserver une trace courte des erreurs de validation sans exposer secrets, prompts sensibles ou donnees personnelles inutiles ;
- declarer la politique d'echec dans le contrat de l'agent.

Politiques d'echec autorisees :
- `reject` : refuser la sortie et retourner une erreur controlee ;
- `retry_once` : relancer une seule fois avec le message d'erreur de validation ;
- `repair_with_trace` : tenter une reparation bornee, tracer l'ecart et revalider ;
- `human_review` : basculer vers validation humaine.

Une action critique ne peut pas etre declenchee depuis une sortie reparee automatiquement sans validation humaine explicite.

## Bindings SQL
Regles obligatoires :
- pas de SQL libre genere puis execute par le LLM ;
- requetes preparees et versionnees cote backend ;
- parametres types ;
- read-only par defaut ;
- limite de lignes ;
- timeout ;
- logs ;
- justification du binding ;
- statut de validation avant activation.

## Bindings Nexus/RAG
Utiliser Nexus ou RAG pour enrichir le contexte lorsque des documents, procedures, preuves ou connaissances non tabulaires sont necessaires.
Chaque binding doit preciser :
- variable injectee ;
- requete ou template ;
- source attendue ;
- caractere obligatoire ou optionnel ;
- limite et risque d'interpretation.

## Skills runtime
Une skill runtime est une instruction metier injectee dans un agent applicatif.
Elle doit contenir :
- objectif ;
- regles ;
- exemples ;
- sortie attendue ;
- limites ;
- sources SQL/Nexus utiles ;
- cas de test.

Ne pas confondre :
- skills Codex : rendent Codex expert du projet pendant le developpement ;
- skills runtime : guident les agents IA utilises par l'application.

## Agent Builder
Si un projet contient un builder d'agents, il doit proposer au maximum 5 agents candidats en V1.
Chaque candidat doit inclure :
- purpose ;
- prompts ;
- bindings SQL/Nexus ;
- skills runtime requises ;
- output schema ;
- input/output models Pydantic ou equivalent ;
- politique de validation et d'echec ;
- tests ;
- placement UI ;
- risques ;
- validation humaine requise.

Regles :
- aucun agent actif sans validation ;
- output schema obligatoire ;
- validation Pydantic ou validateur type equivalent obligatoire si la sortie est consommee par l'application ;
- test cases obligatoires ;
- typed output tests obligatoires ;
- bindings justifies ;
- risques explicites.

## Human-in-the-loop
Par defaut :
- assistance : oui ;
- autonomie totale : non ;
- action critique : validation humaine.

Une action est critique si elle modifie des donnees, declenche un paiement, envoie une communication externe, influence une decision reglementaire, fiscale, juridique, medicale, RH ou securite, ou produit un effet difficile a annuler.

## Verification minimale
Avant livraison d'un agent runtime :
- valider le schema JSON expose au LLM ;
- valider la sortie avec le modele Pydantic ou le validateur type equivalent ;
- tester une sortie valide ;
- tester une sortie JSON malformee ;
- tester un champ obligatoire absent ;
- tester un type incorrect ;
- tester une enum invalide ;
- tester un champ inattendu si le contrat est ferme ;
- tester une sortie partielle ;
- verifier qu'une sortie invalide ne declenche aucune action critique ;
- executer les test cases ;
- verifier les bindings ;
- verifier les logs/traces ;
- tester le rendu UI attendu ;
- documenter les limites et la validation humaine.
