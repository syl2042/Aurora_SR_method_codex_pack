# TOKEN_OPTIMIZATION.md

Objectif : reduire les tokens des sorties terminal sans perte de qualite.

Regles :
- conserver la sortie brute locale ;
- indiquer si sortie compressee dans `verification.md` ;
- revenir au brut si diagnostic ambigu.

Outils : RTK si disponible, trs si disponible, sinon `scripts/codex/aurora_token_run.py`.

Brut obligatoire/fallback pour securite, secrets, migrations, auth, integrations critiques, erreurs runtime inconnues.

## Budget contexte hybride

`context_budget_report.py` distingue quatre signaux :

- `input_tokens` / `raw_context_percent` : volume brut lu dans `last_token_usage`, information de diagnostic seulement.
- `effective_context_percent` : estimation de pression active, calculee avec `cached_input_tokens` pondere a 10%, plus les tokens non caches et sorties recentes.
- `uncached_input_tokens` : volume nouveau non cache, utile pour estimer le cout et le risque de reprise.
- `cache_ratio` : part cachee du prompt ; un ratio eleve evite les coupures trop precoces mais ne justifie pas des conversations infinies.

Le script expose aussi `total_token_usage` et `rate_limits` quand Codex les a enregistres, mais ces valeurs restent des signaux d'observabilite. Le statut SR est base sur le dernier appel utile et la fiabilite de selection de session.

Mode compact obligatoire pour les verifications frequentes :

```bash
python3 scripts/codex/context_budget_report.py --root . --compact
```

Exemple :

```text
context=green action=continue raw=49.0% effective=12.0% uncached=10.0k cached=95.0% output=600 reasoning=100 rl=7.0/45.0 reliable=true
```

Regle SR : ne pas classer une conversation uniquement sur `input_total` ou sur le cumul `total_token_usage`. Le statut est base sur `effective_context_percent`, les signaux non caches, les tours et les lots. `raw_context_percent` ne doit jamais declencher rouge seul. Les etats `unknown`, `stale` et `ambiguous` restent prioritaires et exigent une reprise stricte ou un `NEXT_SESSION_PROMPT.md`.

En fin d'iteration significative, executer le mode compact. Si le statut est `green`, ne rien afficher a l'utilisateur sauf demande explicite. Si le statut est `yellow`, signaler seulement qu'une reprise est recommandee avant une prochaine tache longue. Si le statut est `orange`, `red`, `unknown`, `stale` ou `ambiguous`, creer ou mettre a jour le `NEXT_SESSION_PROMPT.md` du lot courant et donner un prompt court qui pointe vers ce chemin connu.
