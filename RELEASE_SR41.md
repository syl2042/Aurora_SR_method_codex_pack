# Notes de release — SR 4.1.0

Statut : release officielle `v4.1.0`, publiee le 2026-09-24.

## Points principaux

- noyau `AGENTS.md` court et reconcilie a chaque installation ou mise a jour;
- routes conditionnelles et memoire compacte `task_state.yaml`;
- quatre skills methode par defaut et deux facultatives;
- suppression du TDD impose et des tests volontairement rouges;
- appels MCP desactives en mode `core`, deferes et bornes en mode `nexus_kg`;
- mesures separees pour contexte, entree non cachee, cache, sortie et outils;
- convergence transactionnelle par contenu, sans branchement sur la version source;
- preservation des donnees projet et lecture compatible des anciens contrats.
- prompts agents integralement alignes sur le chargement minimal, les trois frontieres et la politique MCP conditionnelle, dans toutes les variantes distribuees.

## Migration

Utiliser la preview puis `--upgrade`, examiner les conflits et lancer `sr_post_install_check.py`. Les artefacts obsoletes ne sont supprimes que si leur empreinte est reconnue comme geree; les adaptations locales sont preservees ou signalees.

Voir `CANDIDATE_SR41.md` pour la qualification pre-release et `CHANGELOG.md` pour l'historique complet.
