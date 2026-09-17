# Realigner l'etat SR apres un upgrade

## SR 4.0.0 — version publiee

Commencer en lecture seule. Les reouvertures et mises a jour ci-dessous sont des propositions jusqu'a validation exacte `je valide` du perimetre de realignement ; les appliquer ensuite uniquement dans ce perimetre. Une autorisation d'installation ne vaut pas validation d'une correction applicative.

Ne modifie aucun code applicatif.

Objectif : reconcilier la memoire SR avec le code et tout le perimetre precedemment valide avant de reprendre le developpement.

Lire `AGENTS.md`, puis `docs/codex/SR_BOOTSTRAP.md`. Executer `python3 scripts/codex/find_next_session_prompt.py --root . --json` : utiliser `selected`; si `ambiguous`, demander le chemin puis utiliser `--prompt`. Ne jamais choisir `latest` selon la seule date. Lire le `NEXT_SESSION_PROMPT.md` selectionne et ses `sr_contract.json`/`loop_contract.json`, avec toutes les `validated_requests` ouvertes heritees. Sans reprise, inventorier les lots ouverts et proposer le perimetre. Pour ce realignement apres upgrade, lire aussi `docs/CURRENT_STATE.md` et les registres lots/passes afin de detecter les ecarts globaux. Charger ensuite seulement les memoires detaillees, procedures, RepoMap/KG et fichiers code/tests necessaires aux lots concernes ; elargir si une preuve, un gate ou une dependance l'exige.

1. Executer les audits du pack, de la documentation de release, du post-install, du projet et des contrats de tache.
2. Inventorier chaque entree de `validated_requests` et conserver son requirement ID stable, lot/passe d'origine, `implementation_status`, `evidence_status`, tests manquants et historique des retours.
3. Rouvrir le lot d'origine lorsqu'une exigence validee est absente, partielle, defectueuse, regressive ou contredite par un retour utilisateur.
4. Recharger toute la checklist ouverte de ce lot et de sa passe ; ne pas isoler seulement le dernier defaut.
5. Appliquer les statuts stricts :
   - `done` : implementation et preuves requises completes ;
   - `user_testing` : implementation technique complete, seul E2E reel ou acceptation humaine restant ;
   - `repair` : au moins une implementation absente, partielle, defectueuse ou en echec ;
   - `blocked` : autorite, acces, secret, decision ou changement externe reellement indisponible.
6. Garder les preuves code/build/runtime/E2E/deploiement separees mais rattachees a la meme exigence persistante.
7. Mettre a jour `CURRENT_STATE.md` et la task memory active seulement lorsque les preuves soutiennent le nouvel etat.

Commencer le rapport par `Demande utilisateur | Etat | Preuve | Reste a faire`, lister les lots rouverts et preuves manquantes, puis proposer un seul perimetre de reprise consolide. Ne creer un nouveau lot que pour une demande reellement hors scope valide.

Stopper et demander la validation humaine exacte avant mutation.

Parcours : installation neuve `00 -> 06` ; installation existante `05 -> 06 -> 07`. Le prompt `06` controle seulement ; `07` propose le realignement puis attend `je valide` avant modification de la memoire. Aucun developpement applicatif n'est autorise par ces parcours.
