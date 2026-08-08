# Realigner la SR Method avec le projet courant

Tu travailles dans un repo qui vient d'etre installe ou mis a jour avec la SR Method.

Objectif : faire un audit SR de reprise avant de continuer le developpement, pour aligner la memoire SR avec ce qui est reellement implemente dans le code.

Ce n'est pas une passe de developpement.
Ce n'est pas une migration applicative.

Regles :

- Ne modifie aucun code applicatif.
- Ne cree aucune migration.
- Ne change aucune dependance.
- Ne corrige aucun bug pendant cette passe.
- Ne suppose pas qu'un lot est fait parce qu'il est note comme fait dans la documentation.
- Verifie dans le code et les tests ce qui est reellement implemente.
- En SR 3.0.0, `sr_contract.json` est le contrat machine cible de chaque task memory.
- Les fichiers legacy `task_plan.md`, `findings.md`, `progress.md`, `decisions.md`, `verification.md`, `gate_report.md` et `loop_contract.json` restent historiques.
- Ne supprime aucun fichier legacy.
- Ne cree pas de contrats retroactifs pour toutes les anciennes taches sans validation explicite.
- Tu peux mettre a jour uniquement la memoire SR si elle est obsolete : `docs/CURRENT_STATE.md`, `docs/codex/SR_LOTS.yaml`, `docs/codex/SR_INBOX.yaml`, `docs/codex/tasks/`, et eventuellement `docs/codex/CODEBASE_MAP.md` si la carte est manifestement perimee.
- Apres tout changement de version SR, `docs/CURRENT_STATE.md` doit etre mis a jour meme si aucun code applicatif ne change : version SR installee, date de revue, dernier prompt de reprise, warnings, lots significatifs, validations E2E en attente et prochaine etape.
- Le `loop_contract.json` de cette passe doit declarer `memory_updates.current_state_updated=true` avant une cloture `done` ou `user_testing`.

Sources a lire :

1. `AGENTS.md`
2. `docs/codex/SR_BOOTSTRAP.md`
3. `docs/codex/SR_HARNESS_METHOD.md`
4. `docs/CURRENT_STATE.md`
5. `docs/codex/SR_LOTS.yaml`
6. `docs/codex/SR_PASSES.yaml` si present
7. `docs/codex/SR_INBOX.yaml`
8. `docs/codex/CODEBASE_MAP.md` et `docs/codex/CODEBASE_MAP.generated.md` si presents
9. `docs/codex/NEXUS_CONTEXT_PACK.md` ou context pack KG si `knowledge.mode: nexus_kg`
10. La derniere memoire de tache pertinente dans `docs/codex/tasks/`
11. Le code reel lie aux lots en cours, partiels, reopened ou user_testing
12. `docs/codex/tasks/_TEMPLATE/loop_contract.json` et `scripts/codex/validate_loop_contract.py`
13. `docs/codex/tasks/_TEMPLATE/sr_contract.json` et `scripts/codex/validate_sr_contract.py`

Methode :

1. Lancer si possible :
   - `python3 scripts/codex/audit_codex_pack.py`
   - `python3 scripts/codex/audit_sr_project.py --root .`
   - `python3 scripts/codex/audit_sr_task_contracts.py --root .`
   - `python3 scripts/codex/sr_post_install_check.py --root .`
   - `python3 scripts/codex/context_budget_report.py --root . --compact`
   - `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json`
   - `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json`
   - `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` si `SR_PASSES.yaml` existe
2. Identifier le mode connaissance :
   - `core` : RepoMap seulement ;
   - `nexus_kg` : RepoMap + Nexus KG.
3. Lister les lots ouverts, partiels, reopened, user_testing et recemment marques done.
4. Pour chaque lot prioritaire, appliquer la chaine `RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs`, puis verifier dans le code :
   - fichiers concernes ;
   - routes, endpoints, services, composants ou tests attendus ;
   - preuves de fonctionnement ;
   - ecarts entre documentation et implementation.
5. Appliquer le Lot Design Evidence Gate avant tout statut executable :
   - `proposed` autorise les hypotheses et fichiers candidats ;
   - `planned`, `validated`, `in_progress` et `reopened` exigent `design_evidence.status: pass` ou `not_applicable` justifie ;
   - si `code_read_required: true`, renseigner `confirmed_files_read` ;
   - sans preuve suffisante, garder le lot en `proposed`.
6. Classer chaque lot :
   - `done` : implemente et verifiable ;
   - `partial` : implemente en partie ;
   - `reopened` : annonce termine mais incomplet ou incoherent ;
   - `validated` : pret a developper ;
   - `blocked` : decision humaine, dependance ou information manquante.
7. Si plusieurs lots restent executables ou proches de l'etre, proposer des passes :
   - lots inclus et ordre ;
   - dependances terminees, incluses ou bloquees ;
   - prerequis communs : secrets, identifiants, assets, services, comptes de test ;
   - validations humaines, migrations et actions externes ;
   - E2E groupe ou par lot ;
   - statut initial `planned` sauf validation explicite.
8. Si une passe existe deja ou vient d'etre proposee, verifier le statut Pass Runtime Goal :
   - `scripts/codex/build_pass_runtime_goal.py` present ;
   - `docs/codex/tasks/_TEMPLATE/pass_runtime_goal.md` present ;
   - `PROJECT_PROFILE.yaml` contient `sr_passes.pass_runtime_goal` ;
   - Goal Length Gate documente : `max_goal_command_chars: 1000`, `hard_limit: 4000` ;
   - aucun `/goal` ne doit etre lance pendant le realignement.
9. Recommander la generation de `pass_runtime_goal.md` uniquement apres validation d'une passe executable :
   - passe `validated` ou `in_progress` pour execution ;
   - `--allow-planned` seulement pour dry-run ;
   - jamais pour une passe `proposed`.
10. Rappeler la regle de cloture de passe : `done` seulement si aucun E2E utilisateur ou validation humaine ne reste requis ; sinon `user_testing`, `repair` ou `blocked`.
11. Auditer les task memories avec `audit_sr_task_contracts.py` :
   - par defaut, rester en lecture seule ;
   - lister les taches legacy sans `sr_contract.json` ;
   - lister les contrats existants invalides ;
   - ne pas assimiler "contrat absent" a "lot incomplet".
12. Si une ancienne task doit etre reprise, proposer avant execution :
   - soit une reprise legacy sans creer de contrat retroactif ;
   - soit une creation controlee pour une tache ciblee avec `python3 scripts/codex/audit_sr_task_contracts.py --root . --task docs/codex/tasks/<task> --write` ;
   - soit une migration batch, uniquement apres validation explicite.
13. Si un `sr_contract.json` est cree :
   - conserver tous les fichiers legacy ;
   - marquer les intentions comme `todo` tant qu'elles n'ont pas ete relues ;
   - valider avec `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/<task>/sr_contract.json`.
14. Mettre a jour `docs/CURRENT_STATE.md` pour tout changement de version SR et mettre a jour les autres memoires SR uniquement si l'audit prouve un ecart.
15. Creer un `loop_contract.json` et, pour la passe de realignement elle-meme, un `sr_contract.json` si le projet exige SR 3.0.0.
16. Produire un plan net :
   - fait ;
   - partiel ;
   - restant ;
   - lots a rouvrir ;
   - prochains lots recommandes ;
   - tests ou validations humaines necessaires.

Sortie attendue :

- objectif courant detecte ;
- tableau court des lots audites et leur statut corrige ;
- fichiers SR mis a jour ;
- entree `docs/CURRENT_STATE.md` ajoutee ou actualisee ;
- preuves consultees dans le code ;
- etat du Lot Design Evidence Gate pour les lots executables ;
- mode connaissance et etat RepoMap/KG ;
- etat budget contexte ;
- audit des `sr_contract.json` existants ou manquants ;
- statut `SR_PASSES.yaml`, passes proposees ou raison de non-proposition ;
- statut Pass Runtime Goal : outillage present/absent, Goal Length Gate, prochaine passe eligible ou raison de non-generation ;
- Loop Contract de realignement avec decision `conversation_transition` ;
- SR Contract 3.0.0 de la passe de realignement si requis par le projet ;
- plan de reprise priorise ;
- point d'arret avant tout code applicatif.
