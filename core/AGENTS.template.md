# Repository Guidelines — {{PROJECT_NAME}}

## Invariants permanents
- Repondre en francais sauf demande contraire. Respecter les regles metier, permissions et scopes du projet; ne jamais les inventer ni les elargir silencieusement.
- Ne jamais exposer secrets, tokens serveur ou donnees sensibles dans frontend, logs, docs ou Git.
- Pas de dependance, migration, connecteur, webhook, cron, upload, relaxation CORS, publication ou action externe sensible hors autorisation.
- Signaler les interpretations metier concurrentes; ne pas choisir silencieusement. Solution simple couvrant tout le perimetre valide, changements chirurgicaux, aucun refactor opportuniste.
- Le code prouve le comportement existant; il ne remplace pas les invariants normatifs. Signaler les contradictions.
- Avant codage : objectif verifiable, hypotheses, approche, skills utiles et verification proportionnee. Une tache non verifiee n'est pas terminee. Distinguer implementation, preuve technique, E2E et acceptation humaine.

<!-- AURORA_SR_PACK_START -->
## Entree SR
- Validation humaine stricte : aucune mutation avant `je valide`, pour le perimetre decrit. Une validation de passe couvre ses lots et tests; aucune micro-validation supplementaire si les gates restent verts. Les autorisations et exceptions explicites de la session (dont BUILD-CYCLE-V2) priment sur les gates generiques; pas d'extension implicite.
Toute tache non triviale, multi-fichiers, metier, architecture, integration, IA, DB, securite, UI structurante ou reprise applique `docs/codex/SR_BOOTSTRAP.md`. Apres nouvelle conversation, compact ou handoff, reprendre par ce routeur et l'etat court pertinent. Une question simple sans investigation significative n'exige pas toute la methode.
Les procedures sont chargees au moment de leur declenchement : Fact Gate avant conclusion, Evidence Gate avant recommandation, Lot Completion Gate avant cloture, Propagation Gate pour contrat partage. Le routeur repertorie aussi tous les autres gates; une decouverte impose de reevaluer les routes.
Les invariants metier locaux, HITL, permissions/scopes, interdits et autorisations explicites restent applicables. Les fichiers SR sont la memoire persistante pour App et CLI.
<!-- AURORA_SR_PACK_END -->

## Sources specialisees
- `DESIGN.md` pour UI significative; `docs/domain/` pour regle metier concernee.
- `docs/codex/SKILL_DIGEST.md` pour selection ciblee; lire les SKILL.md retenus.
- `docs/codex/CODEBASE_MAP.md` pour exploration structurelle lorsque les fichiers ne sont pas deja identifies; code reel avant conclusion.
- `docs/CURRENT_STATE.md` pour etat global, changement transverse ou conflit de reprise.
Ces references sont des routes conditionnelles, pas une checklist universelle.
