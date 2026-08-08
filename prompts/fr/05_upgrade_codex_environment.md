# Mettre a jour un projet vers la derniere SR Method

Tu travailles dans un repository applicatif deja equipe d'une version existante de la Aurora SR Method, possiblement ancienne, partielle ou adaptee localement.

Objectif verifiable : mettre a jour la SR Method vers la derniere version officielle disponible, sans regression, sans modifier le code applicatif, sans ecraser les adaptations projet, et en laissant le projet dans un etat SR realigne avant toute reprise de developpement.

Source officielle SR Method :

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Source locale du pack :

```text
SR_PACK_SOURCE
```

`SR_PACK_SOURCE` designe le chemin local du clone officiel sur le serveur courant. Ne suppose jamais un chemin absolu specifique a une machine. Si l'utilisateur n'a pas donne ce chemin, le detecter ou proposer un chemin local adapte au serveur courant, par exemple `./.sr-method-pack`, `/opt/aurora/SR_Method` ou un dossier de travail choisi par l'utilisateur.

Si la source locale n'existe pas ou n'est pas un clone du repo officiel, proposer de la creer ou de la mettre a jour depuis le repo GitHub officiel avant d'appliquer l'upgrade. Ne pas telecharger depuis une autre source sans validation utilisateur.

Regles strictes :

- Ne modifie aucun code applicatif.
- Ne cree aucune migration.
- Ne modifie aucune dependance applicative.
- Ne touche pas aux secrets, variables d'environnement ou fichiers de configuration sensibles.
- Ne remplace pas aveuglement `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `PROJECT_PROFILE.yaml`, `SKILL_MAP.md`, `docs/codex/SR_LOTS.yaml`, `docs/codex/SR_PASSES.yaml`, les task memories, handoffs, decisions ou skills projet.
- Preserve les adaptations locales du projet.
- Preserve les fichiers legacy de task memory ; ne cree pas de contrats retroactifs en batch sans validation explicite.
- Preserve `SR_LOTS.yaml`. Ajouter `SR_PASSES.yaml` de facon additive si absent, mais ne pas convertir automatiquement les anciens lots ou task memories en passes validees.
- Ne pas convertir massivement les anciens lots pour ajouter `design_evidence`; ajouter le Lot Design Evidence Gate seulement aux lots crees, promus ou repris apres upgrade.
- Ajouter l'outillage Pass Runtime Goal de facon additive (`build_pass_runtime_goal.py`, template `pass_runtime_goal.md`, options `sr_passes.pass_runtime_goal`) sans generer de goal tant qu'une passe n'est pas validee.
- Ne jamais lancer `/goal` pendant l'upgrade. L'upgrade prepare la methode ; l'execution par goal ne vient qu'apres realignement, pass planning et validation utilisateur.
- Preserve les task memories historiques sans `propagation_gate` : les signaler comme legacy warnings, pas comme erreurs bloquantes. Les nouveaux templates et contrats crees apres upgrade doivent inclure le Propagation Gate.
- En SR plein regime, tout changement de version SR doit mettre a jour `docs/CURRENT_STATE.md` avec la version installee, la date de revue, les controles executes, le dernier `NEXT_SESSION_PROMPT.md`, les lots significatifs et la prochaine etape.
- Un `loop_contract.json` de type `upgrade` ne peut pas se cloturer en `done` avec `memory_updates.current_state_updated=false`.
- Avant toute modification de fichier, expose le plan d'upgrade et attends la validation explicite de l'utilisateur.

Etape 1 - Diagnostic de version :

1. Lis les fichiers SR existants :
   - `docs/codex/SR_PACK_VERSION.json` si present ;
   - `docs/codex/SR_LOTS.yaml` si present ;
   - `docs/codex/SR_PASSES.yaml` si present ;
   - `docs/CURRENT_STATE.md` si present ;
   - `AGENTS.md` si present ;
   - `docs/codex/tasks/` si present.
2. Lance les audits disponibles sans modifier :
   - `python3 scripts/codex/audit_codex_pack.py --json` si disponible ;
   - `python3 scripts/codex/verify_codex_pack.py` si disponible ;
   - `python3 scripts/codex/sr_post_install_check.py --root .` si disponible.
3. Si ces scripts n'existent pas ou echouent parce que la version est trop ancienne, classe la version comme `unknown` ou `legacy`.

Etape 2 - Classification :

Classe le projet dans un de ces flux :

- `upgrade_minor_3x` si la version installee est deja `3.x` ;
- `upgrade_standard_235_plus` si la version est `2.3.5+` ;
- `upgrade_legacy_unknown` si la version est absente, illisible, inferieure a `2.3.5`, ou si l'installation SR est partielle.

Etape 3 - Source officielle :

1. Verifie si un clone local du pack officiel existe deja.
2. S'il existe, verifie son remote et son etat git.
3. S'il n'existe pas, propose de cloner :
   `git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git ./.sr-method-pack`
4. Utilise uniquement la source officielle ou un clone local verifie.
5. Note le commit source utilise dans le rapport final.

Etape 4 - Analyse avant mutation :

Compare l'installation actuelle avec la derniere version du pack et identifie :

- fichiers SR manquants ;
- fichiers SR anciens ;
- fichiers projet a preserver ;
- fichiers necessitant une fusion prudente ;
- presence ou absence de `SR_PASSES.yaml` ;
- presence ou absence de l'outillage Pass Runtime Goal ;
- presence ou absence du Lot Design Evidence Gate ;
- risques d'ecrasement ;
- anciens contrats ou task memories a laisser en legacy warnings.

Important : les anciens lots sans `design_evidence` ne doivent pas etre modifies en masse. Le `design_evidence` doit etre ajoute seulement aux lots crees, promus ou repris apres upgrade.

Etape 5 - Plan a faire valider :

Avant toute modification, presente un plan court avec :

- version detectee ;
- flux retenu ;
- fichiers a ajouter ;
- fichiers a mettre a jour ;
- fichiers a preserver ;
- risques identifies ;
- commandes de verification prevues ;
- impact attendu sur `SR_LOTS.yaml`, `SR_PASSES.yaml`, `AGENTS.md`, `CURRENT_STATE.md` et `docs/codex/tasks/`.

Attends la validation explicite de l'utilisateur avant de modifier.

Etape 6 - Upgrade apres validation :

Apres validation seulement :

1. Applique l'upgrade SR de maniere additive.
2. Preserve les fichiers projet et les historiques.
3. Mets a jour les scripts, templates, prompts et docs SR necessaires.
4. Ajoute `SR_PASSES.yaml` si absent, sans declarer de passe executable automatiquement.
5. Ajoute l'outillage Pass Runtime Goal si absent :
   - `build_pass_runtime_goal.py`
   - template `pass_runtime_goal.md`
   - options `sr_passes.pass_runtime_goal`
6. Verifie que le Goal Length Gate est present :
   - `max_goal_command_chars: 1000`
   - `hard_limit: 4000`
7. Verifie que le Lot Design Evidence Gate est documente et actif pour les nouveaux lots ou les lots repris.

Etape 7 - Verifications :

Lance les verifications disponibles et adaptees :

- `python3 scripts/codex/audit_codex_pack.py`
- `python3 scripts/codex/verify_codex_pack.py`
- `python3 scripts/codex/sr_post_install_check.py --root .`
- `python3 scripts/codex/find_next_session_prompt.py --root .`
- `python3 scripts/codex/audit_sr_project.py --root .`
- `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` si le fichier existe
- `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` si `SR_PASSES.yaml` existe
- `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json` si present
- `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json` si present
- `python3 scripts/codex/audit_sr_task_contracts.py --root .`
- `python3 scripts/codex/context_budget_report.py --root . --compact`
- `python3 scripts/codex/validate_skills.py --path ~/.codex/skills` si les skills methode sont installees

Si certains scripts sont absents avant upgrade, signale-le comme information normale pour version ancienne, puis relance apres upgrade.

Etape 8 - Realignement obligatoire :

Apres l'upgrade, mets a jour ou propose la mise a jour de `docs/CURRENT_STATE.md` avec :

- version SR avant ;
- version SR apres ;
- date de mise a jour ;
- commit source utilise ;
- fichiers ajoutes ou mis a jour ;
- fichiers preserves ;
- warnings legacy ;
- statut `SR_LOTS.yaml` ;
- statut `SR_PASSES.yaml` ;
- statut Pass Runtime Goal ;
- statut Lot Design Evidence Gate ;
- prochaine etape recommandee.

Etape 9 - Suite recommandee :

A la fin, ne reprends pas le developpement applicatif directement.

Propose la sequence suivante selon l'etat du projet :

1. utiliser `07_realign_sr_state_after_upgrade.md` pour realigner l'etat SR ;
2. utiliser `09_define_sr_lots_from_scope.md` pour creer ou promouvoir les lots avec analyse prealable des fichiers concernes ;
3. utiliser `08_define_sr_passes_from_lots.md` pour proposer automatiquement les regroupements de lots par passe ;
4. generer un `pass_runtime_goal.md` uniquement apres validation humaine d'une passe ;
5. lancer `/goal` uniquement pour une passe validee, jamais pendant l'upgrade.

Rapport final attendu :

- version avant/apres ;
- flux d'upgrade retenu ;
- commit source SR Method utilise ;
- fichiers modifies ;
- fichiers preserves ;
- validations reussies ;
- validations echouees ou non applicables ;
- warnings legacy ;
- action suivante proposee.

Fin obligatoire : attends la validation avant toute modification applicative ou toute execution de passe.
