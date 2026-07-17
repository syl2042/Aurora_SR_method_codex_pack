# SR Agent Method

## Objectif

La SR Agent Method definit comment construire des agents IA runtime dans une application sans rendre le projet dependant d'un framework agent lourd, d'un provider modele, d'un domaine metier, d'une interface ou d'une representation technique particuliere.

Elle privilegie un pattern backend-first, explicite, testable et validable.

Principe fondateur :

```text
Un agent runtime n'est pas defini par son modele ni par son prompt.
Il est defini par l'action produit bornee qu'il sert, la representation interne stable qu'il lit ou produit, le contrat type qui valide sa sortie, et la surface runtime qui consomme le resultat valide.
```

## Pattern minimal

```text
action produit bornee
+ representation interne stable
+ contrat runtime type
+ input/output models Pydantic ou validateur type equivalent
+ JSON schema ou equivalent expose au LLM
+ prompt contract derive du contrat runtime
+ user message builder cote application
+ variables injectees explicites et limitees
+ bindings SQL controles
+ bindings Nexus/RAG optionnels
+ skills runtime optionnelles
+ tools/actions explicites
+ routing/fallback si plusieurs agents peuvent repondre
+ validation runtime stricte
+ retry/repair policy
+ traces d'erreur de validation
+ traces non sensibles
+ validation humaine si necessaire
```

## Principes

- Un agent runtime est un composant applicatif, pas une conversation libre.
- La methode est agnostique des frameworks : elle peut etre appliquee avec LangChain, LangGraph, LlamaIndex, PydanticAI, CrewAI, un SDK agents ou aucun framework agentique.
- La methode est agnostique des domaines, providers, UI et representations internes.
- Le prompt systeme n'est pas la source de verite ; il est une projection du contrat runtime vers le modele.
- Les donnees injectees doivent etre explicites, versionnees et limitees.
- Les bindings SQL sont controles cote backend ; le LLM ne genere pas puis n'execute pas du SQL libre.
- Les sorties doivent etre structurees si l'application les consomme.
- Le LLM produit une proposition JSON ; elle ne devient une donnee applicative qu'apres validation par un contrat type backend.
- Pour les backends Python, Pydantic est le standard recommande et obligatoire des que la sortie d'un agent est consommee par l'application.
- Pour les autres stacks, utiliser un validateur type equivalent avec les memes garanties : types stricts, champs obligatoires, enums controlees, erreurs tracees.
- Les actions critiques exigent une validation humaine.
- Les skills Codex et les skills runtime sont deux objets differents.

## Runtime agent shapes

Chaque agent runtime doit etre classe selon sa forme d'execution principale :

- `micro_agent` : un appel modele, une action produit bornee, une sortie structuree, pas de boucle autonome ;
- `workflow_agent` : boucle bornee avec outils, observations, actions visibles ou etapes successives ;
- `delegation_agent` : route, transfere ou reformule une demande vers un agent specialise ;
- `mini_agent` : variante reduite pour cout, latence, modele moins capable, contexte limite ou risque controle.

Ces formes ne sont pas des niveaux de maturite. Elles servent a choisir le contrat runtime le plus simple suffisant.

## Product action scope

Un agent runtime doit etre rattache a une action produit bornee avant d'etre rattache a un prompt.

Contrat recommande :

```yaml
product_action_scope:
  user_action:
  business_moment:
  runtime_entrypoint:
  triggering_condition:
  expected_user_visible_result:
  out_of_scope:
  fallback_policy:
```

Regle : ne pas definir un agent global si une action produit bornee peut etre identifiee.

## Internal representation contract

Un agent fiable lit, produit ou modifie une representation interne stable que le runtime sait valider et consommer.

Contrat recommande :

```yaml
internal_representation_contract:
  representation_name:
  representation_type:
  source_of_truth:
  allowed_changes:
  forbidden_changes:
  consumer:
  validation_owner:
```

Exemples generiques de representations : `RiskFinding[]`, `SupportReplyDraft`, `InvoiceClassification`, `QueryPlan`, `DocumentOutline`, `ActionRecommendation[]`, `UIStatePatch`.

## Prompt contract and user message builder

Flux attendu :

```text
Runtime contract
-> typed input/output models
-> JSON schema or equivalent
-> prompt contract
-> user message builder
-> LLM response
-> strict runtime validation
-> accepted object or controlled failure
```

Le `user_message_builder` est le code applicatif qui transforme l'etat reel de l'application en message utilisateur controle.

Contrat recommande :

```yaml
user_message_builder:
  owner:
  source_files:
  injected_variables:
  forbidden_variables:
  serialization_rules:
  truncation_rules:
  redaction_rules:
```

## Tools and actions

Un tool inspecte, recupere ou prepare. Une action engage l'interface, l'etat applicatif, une ecriture, une notification, une decision ou un artefact utilisateur.

Contrat recommande :

```yaml
tools_and_actions:
  inspection_tools:
  retrieval_tools:
  computation_tools:
  committing_actions:
  user_visible_actions:
  state_mutating_actions:
  human_confirmed_actions:
```

Une action qui modifie l'etat, declenche une ecriture, notifie un tiers ou influence une decision critique doit etre controlee explicitement et, si necessaire, validee humainement.

## Routing policy

Quand plusieurs agents peuvent repondre, le runtime doit definir une politique de routage et de fallback.

Contrat recommande :

```yaml
routing_policy:
  router_required:
  router_agent_key:
  allowed_intents:
  default_route:
  uncertainty_policy:
  fallback_agent:
  target_refusal_allowed:
```

Le fallback doit privilegier la route la moins risquee, pas la plus autonome.

## Pydantic Output Contract

Le `output JSON schema` guide le LLM, mais ne suffit pas a proteger l'application. Le schema expose au LLM doit venir autant que possible du modele type backend.

Flux attendu :

```text
modele Pydantic ou equivalent
-> JSON schema donne au LLM
-> reponse JSON du LLM
-> validation runtime stricte
-> objet applicatif accepte ou erreur controlee
```

Regles :
- valider la sortie avant tout rendu UI avance, persistance, action ou decision ;
- refuser ou tracer les champs inconnus lorsque le domaine exige une sortie fermee ;
- utiliser des enums et types stricts pour les statuts, severites, actions et categories ;
- separer le message utilisateur controle par l'UI du resultat metier consomme par le backend ;
- tracer les erreurs de validation sans exposer de donnees sensibles ;
- ne jamais declencher une action critique depuis une sortie reparee automatiquement sans validation humaine.

Politiques d'echec autorisees :
- `reject` : refuser la sortie et retourner une erreur controlee ;
- `retry_once` : relancer une seule fois avec l'erreur de validation comme contexte ;
- `repair_with_trace` : tenter une reparation bornee et tracer l'ecart ;
- `human_review` : envoyer la sortie en validation humaine.

## Relation avec AI_AGENT_RUNTIME_METHOD.md

`AI_AGENT_RUNTIME_METHOD.md` reste l'ancien nom technique du document operationnel. La SR Agent Method est le nom public de cette branche.
