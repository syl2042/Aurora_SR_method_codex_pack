# Mettre a jour un projet vers la derniere SR Method

Tu travailles dans un repo deja equipe d'une ancienne version de la SR Method.

Objectif : auditer puis mettre a jour le pack SR sans modifier le code applicatif et sans ecraser les adaptations projet.

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

Regles :

- Ne modifie aucun code applicatif.
- Ne cree aucune migration.
- Ne touche pas aux secrets.
- Ne remplace pas aveuglement `AGENTS.md`, `DESIGN.md`, `CURRENT_STATE.md`, `PROJECT_PROFILE.yaml`, `SKILL_MAP.md` ou les docs metier sans analyse.
- Preserve les `docs/codex/tasks/`, handoffs, decisions et project-skills existants.
- Preserve les fichiers legacy de task memory ; ne cree pas de contrats retroactifs en batch sans validation explicite.
- En SR plein regime, tout changement de version SR doit mettre a jour `docs/CURRENT_STATE.md` avec la version installee, la date de revue, les controles executes, le dernier `NEXT_SESSION_PROMPT.md`, les lots significatifs et la prochaine etape.
- Un `loop_contract.json` de type `upgrade` ne peut pas se cloturer en `done` avec `memory_updates.current_state_updated=false`.

Etapes :

1. Detecter la version SR installee :
   - lire `docs/codex/SR_PACK_VERSION.json` si present ;
   - lancer `python3 scripts/codex/audit_codex_pack.py --json` si disponible ;
   - si le script n'existe pas ou la version est absente, classer la version comme `unknown`.
2. Classer le flux :
   - `upgrade_minor_3x` si la version installee est deja `3.x` ;
   - `upgrade_standard_235_plus` si la version est `2.3.5+` ;
   - `upgrade_legacy_unknown` si la version est `<2.3.5`, `2.0.0`, absente ou illisible.
3. Si le script d'audit n'existe pas, comparer manuellement les fichiers SR attendus.
4. Verifier ou preparer la source SR :
   - si l'utilisateur a indique `SR_PACK_SOURCE`, verifier son remote GitHub et faire `git pull` si possible ;
   - sinon, chercher un clone local evident du repo officiel sans parcourir inutilement tout le systeme ;
   - si aucun clone local fiable n'existe, proposer de cloner le repo officiel dans un chemin adapte au serveur courant, par exemple `git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git ./.sr-method-pack` ;
   - noter le commit source utilise dans le rapport.
5. Identifier :
   - fichiers manquants ;
   - fichiers presents mais anciens ;
   - fichiers projet a fusionner manuellement ;
   - risques d'ecrasement.
6. Proposer un plan d'upgrade adapte au flux detecte.
7. Appliquer uniquement les fichiers methode/scripts/templates validés.
8. Installer ou verifier les skills methode globales.
9. Relancer :
   - `python3 scripts/codex/audit_codex_pack.py`
   - `python3 scripts/codex/verify_codex_pack.py`
   - `python3 scripts/codex/sr_post_install_check.py --root .`
   - `python3 scripts/codex/find_next_session_prompt.py --root .`
   - `python3 scripts/codex/audit_sr_project.py --root .`
   - `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml`
   - `python3 scripts/codex/context_budget_report.py --root . --compact`
   - `python3 scripts/codex/validate_skills.py --path ~/.codex/skills`
   - `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json`
   - `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json`
   - `python3 scripts/codex/audit_sr_task_contracts.py --root .`
10. Mettre a jour `docs/CURRENT_STATE.md` avec une entree structuree de l'upgrade SR : version avant/apres, commit source, date, warnings, dernier prompt de reprise, statut des contrats, decision sur `07`, et prochaine etape.
11. Produire un rapport :
   - version avant/apres ;
   - flux detecte : `upgrade_minor_3x`, `upgrade_standard_235_plus` ou `upgrade_legacy_unknown` ;
   - source officielle et commit source utilise ;
   - fichiers ajoutes ;
   - fichiers fusionnes ;
   - fichiers laisses intacts ;
   - mode connaissance detecte : `core` ou `nexus_kg` ;
   - presence RepoMap et besoin eventuel de Nexus KG ;
   - actions manuelles restantes.
   - mise a jour `docs/CURRENT_STATE.md` executee et resumee.
   - presence des docs `SR_METHOD.md`, `SR_DEVELOPMENT_METHOD.md`, `SR_AGENT_METHOD.md`.
   - presence et validation du template `loop_contract.json`.
   - presence et validation du template `sr_contract.json` SR 3.0.0.
   - resultat de l'audit `audit_sr_task_contracts.py`, en distinguant legacy acceptable, contrat invalide et migration a valider.
   - decision sur les prompts suivants :
     - `06` requis si les verifications ci-dessus n'ont pas toutes ete executees ou si le flux est standard/legacy ;
     - `07` requis apres tout changement de version SR ; il peut rester court pour un upgrade mineur, mais doit realigner `CURRENT_STATE.md` et confirmer les prochains lots avant tout code applicatif ;
     - `15` recommande si le projet contient ou prevoit des agents IA runtime.

Fin obligatoire : attendre validation avant toute modification applicative.
