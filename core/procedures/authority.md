# authority — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Non-negotiable rules

- Repondre en francais sauf demande contraire.
- Ne jamais afficher, committer ou documenter de secrets.
- Ne jamais exposer tokens serveur, cles API, credentials ou donnees sensibles cote frontend/logs/docs.
- Validation humaine stricte : Codex peut analyser sans validation, mais ne modifie aucun fichier et ne lance aucune action de mutation tant que l'utilisateur n'a pas ecrit exactement `je valide`; cette validation ne couvre que le perimetre decrit juste avant.
- Pas de dependance, migration, connecteur externe, webhook, cron, upload ou relaxation CORS sans validation.
- Ne pas inventer de regle metier non documentee.
- Le code reel prime sur la documentation ; noter les ecarts dans `findings.md`.
- Ne pas proposer une recommandation technique, un plan engageant ou une prochaine etape si les fichiers verifiables peuvent trancher et n'ont pas ete lus.

## Validation humaine stricte

Quand un `AGENTS.md`, un lot, une reprise ou l'utilisateur active le mode strict, Codex peut analyser, lire et recommander sans validation, mais ne doit modifier aucun fichier ni lancer d'action de mutation tant que l'utilisateur n'a pas ecrit exactement `je valide`.

Cette validation ne couvre que l'action ou le plan decrit juste avant. Toute extension de perimetre, dependance, migration, configuration, donnees, agent IA runtime, backlog, publication Git, action destructive ou changement metier exige une nouvelle validation explicite.

Une validation explicite d'un lot, d'une passe ou d'un plan engage tout le perimetre decrit juste avant validation. Les principes `solution simple`, `changements chirurgicaux`, `scope minimal` et `eviter les refactors` ne peuvent jamais reduire ce perimetre ; ils guident seulement l'implementation de chaque exigence validee.

Si Codex estime qu'un lot valide doit etre reduit, decoupe, reporte ou clarifie, il doit stopper avant mutation, signaler les exigences concernees, proposer un nouveau decoupage et attendre une nouvelle validation. Aucune livraison partielle ne doit etre presentee comme cloture du lot valide.

Si la demande modifie un backlog de lots, Codex doit classer la demande et proposer la mise a jour de `SR_INBOX.yaml` ou `SR_LOTS.yaml` avant de coder.

Si la demande lance ou valide plusieurs lots, Codex doit verifier ou proposer une passe SR dans `SR_PASSES.yaml` avant codage significatif. Le Pass Planning Gate verifie l'ordre, les dependances, le preflight commun, les validations humaines et l'E2E groupe.

Pass Runtime Goal : si une passe validee doit etre executee avec Codex CLI `/goal`, Codex doit generer `pass_runtime_goal.md` avec `scripts/codex/build_pass_runtime_goal.py`, appliquer le Goal Length Gate (`max_goal_command_chars: 1000`, `hard_limit: 4000`), puis utiliser la commande courte produite. Le goal ne remplace jamais les fichiers SR et ne doit pas enchainer une passe suivante sans validation utilisateur.

Avant une recommandation technique engageante, appliquer le knowledge gate :

```text
RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs
```

Avant de creer ou promouvoir un lot en `planned`, `validated`, `in_progress`, `repair` ou `reopened`, appliquer aussi le Lot Design Evidence Gate :

- identifier les fichiers candidats ;
- lire les fichiers qui peuvent confirmer ou infirmer le cadrage ;
- declarer les routes, composants, services, schemas, tests ou logs verifies ;
- lister les hypotheses restantes et questions bloquantes ;
- garder le lot au statut `proposed` si cette evidence manque, sauf cas `not_applicable` justifie.

Un lot `proposed` peut documenter une piste exploratoire sans lecture exhaustive. Un lot pret a executer ne doit pas reposer sur une supposition verifiable non lue.
