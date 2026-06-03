# SR Agent Method

## Objectif

La SR Agent Method definit comment construire des agents IA runtime dans une application sans rendre le projet dependant d'un framework agent lourd.

Elle privilegie un pattern backend-first, explicite, testable et validable.

## Pattern minimal

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

## Principes

- Un agent runtime est un composant applicatif, pas une conversation libre.
- Les donnees injectees doivent etre explicites, versionnees et limitees.
- Les bindings SQL sont controles cote backend ; le LLM ne genere pas puis n'execute pas du SQL libre.
- Les sorties doivent etre structurees si l'application les consomme.
- Le LLM produit une proposition JSON ; elle ne devient une donnee applicative qu'apres validation par un contrat type backend.
- Pour les backends Python, Pydantic est le standard recommande et obligatoire des que la sortie d'un agent est consommee par l'application.
- Pour les autres stacks, utiliser un validateur type equivalent avec les memes garanties : types stricts, champs obligatoires, enums controlees, erreurs tracees.
- Les actions critiques exigent une validation humaine.
- Les skills Codex et les skills runtime sont deux objets differents.

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
