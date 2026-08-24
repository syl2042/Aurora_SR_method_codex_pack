# Realigner l'etat SR apres un upgrade

Ne modifie aucun code applicatif.

Objectif : reconcilier la memoire SR avec le code et tout le perimetre precedemment valide avant de reprendre le developpement.

Lire `AGENTS.md`, `docs/CURRENT_STATE.md`, la methode SR, `SR_LOTS.yaml`, `SR_PASSES.yaml`, le dernier `NEXT_SESSION_PROMPT.md`, les task memories actives, `sr_contract.json`, `loop_contract.json` et le code/tests pertinents.

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
