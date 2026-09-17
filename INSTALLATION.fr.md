# Installation

## SR 4.0.0 — version publiee

Source cible : choisir explicitement `SR_PACK_SOURCE`, soit une version publiee identifiee, soit le candidat local SR 4.0.0 autorise. Lire `core/SR_PACK_VERSION.json` (`version`, `release_status`) et noter `source_commit`, l'etat Git et, si le clone est modifie, une empreinte du contenu source incluant les fichiers non suivis utilises. Un candidat `unreleased` ne doit pas etre presente comme une release. Ne pas remplacer une source candidate par un clone de la derniere version publiee ; si la source demandee manque, s'arreter et clarifier avant installation.

Pour cette cible SR 4.0.0, la source doit annoncer `version: 4.0.0`. Si aucune release 4.0.0 n’est publiee, utiliser uniquement le candidat local autorise ou signaler son absence ; ne pas installer silencieusement une autre version.

Parcours : installation neuve `00 -> 06` ; installation existante `05 -> 06 -> 07`. Le prompt `06` controle seulement ; `07` propose le realignement puis attend `je valide` avant modification de la memoire. Aucun developpement applicatif n'est autorise par ces parcours.

SR 4 charge les procedures selon la tache via `SR_BOOTSTRAP.md` et `SR_ROUTES.json`. Les gates, le HITL, les exigences ouvertes et les schemas de contrats restent preserves. Le numero du pack ne force aucune conversion des anciens contrats.

### Premiere installation
Inspecter les regles locales; obtenir `je valide` pour le perimetre; previsualiser, appliquer `--write`, puis verifier. Les fichiers projet existants sont conserves ou fusionnes explicitement. Aucun code applicatif ne change.

### Mise a jour agnostique
Utiliser `--upgrade` apres audit des fichiers reels. La version precedente est informative, jamais un pre-requis : installations anciennes, sans version, partielles ou melangees sont examinees par contenu. Un fichier pack inconnu/personnalise bloque son remplacement; ne pas le supprimer pour forcer le passage. Comparer et faire valider sa reconciliation. Les anciens contrats, lots ouverts, memoires, handoffs et skills metier restent preserves.

La previsualisation est non mutative sauf `--plan-out` explicitement demande. Un plan enregistre contient les contenus des fichiers : le conserver localement. `--apply-plan` refuse les changements intervenus depuis le diagnostic. Une transaction sauvegarde les fichiers modifies; `--restore` refuse d'ecraser une modification ulterieure. Ne jamais utiliser `--write` pour forcer un upgrade. Un numero de version cible ecrit ne prouve pas la reussite : le postcheck doit passer.

Previsualiser avec la commande ci-dessous avant validation ; apres `je valide`, choisir uniquement le mode correspondant au parcours. `--plan-out` ecrit un plan local et exige une autorisation ; `--apply-plan` refuse un diagnostic perime. `--restore` est une operation distincte, sur le journal exact de la transaction, et refuse les modifications ulterieures. Ne pas contourner un conflit en supprimant un fichier.

Previsualisation seule:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Installation neuve apres validation:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --write
```

Installation existante apres validation:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

Verification seule:

```bash
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Plan local optionnel, apres autorisation:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --plan-out "$SR_PLAN_FILE"
```

Application du plan valide, alternative aux commandes directes:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --apply-plan "$SR_PLAN_FILE"
```

Restauration distincte, uniquement si necessaire et autorisee:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --restore "$SR_JOURNAL_FILE"
```


[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

Le parcours recommande est **prompt Codex d'abord**. Les scripts Python sont des outils techniques que Codex peut lancer apres inspection.

## Choisir d'abord le bon parcours

| Etat de la cible | Prompt | Mode installateur | Comportement requis |
|---|---|---|---|
| Aucun marqueur SR | `00_install_codex_environment` | `--write` | Installer directement SR 4.0.0 |
| Marqueur SR existant, ancien ou partiel | `05_upgrade_codex_environment` | `--upgrade` | Auditer puis fusionner additivement |
| Plusieurs repositories de versions potentiellement differentes | `05_upgrade_codex_environment` | un `--upgrade` par repository | Produire une matrice de version par cible |

Ne jamais supposer que des dossiers voisins utilisent la meme version SR. Lire pour chaque cible la version et les marqueurs reels de methode, schemas, task memories, lots et passes. L'installateur refuse maintenant `--write` s'il detecte deja une installation SR.

## Installer dans un projet cible

1. Selectionner la source locale verifiee selon la section Source cible.
2. Ouvrir Codex dans le projet cible.
3. Coller [prompts/fr/00_install_codex_environment.md](prompts/fr/00_install_codex_environment.md).
4. Laisser Codex installer, verifier et produire le rapport.

Pour un projet vierge ou jamais equipe SR, Codex doit traiter cette etape comme une installation methode uniquement :

- inspecter le repository cible avant d'ecrire ;
- expliquer les fichiers SR qui seront ajoutes ;
- attendre validation si le projet impose la validation humaine stricte ;
- installer les fichiers methode et scripts SR ;
- ne pas modifier le code applicatif, les migrations, dependances, secrets ou regles metier ;
- lancer les scripts de verification ;
- stopper avec un rapport et les prochains prompts recommandes.

La cible d'une installation neuve est le pack SR 4.0.0 : `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 et `SR_PASSES` 0.2. Le contrat SR separe `implementation_status` de `evidence_status`. L'installation ne doit inventer aucune exigence produit validee, aucun lot valide et aucune passe executable.

Fallback technique :

Sans option de mutation et sans `--plan-out`, l’installateur effectue une previsualisation en lecture seule. `--write`, `--upgrade`, `--apply-plan` et `--restore` sont mutuellement exclusifs.

Utiliser le clone `SR_PACK_SOURCE` deja selectionne et verifie. Pour une version publiee, cloner la source officielle si necessaire puis selectionner la reference publiee validee ; le clone seul ne selectionne pas SR 4 candidate. Le candidat exige le contenu local explicitement autorise. Definir `SR_TARGET` comme chemin du projet vise avant les commandes.

Les nouvelles installations incluent `docs/codex/SR_PASSES.yaml`. Les passes SR regroupent plusieurs lots dans une execution bornee avec ordre de dependances, preflight commun, validations humaines et tests E2E groupes. Les lots restent l'unite atomique dans `SR_LOTS.yaml`.

Le registre installe commence par `passes: []`. Cet etat est valide et ne signifie pas qu'une configuration manque : l'installation n'invente aucune passe produit. Utiliser le prompt `08` lorsque les lots sont connus et valides.

Les nouvelles installations incluent aussi l'outillage Pass Runtime Goal :

```text
scripts/codex/build_pass_runtime_goal.py
docs/codex/tasks/_TEMPLATE/pass_runtime_goal.md
```

Ne pas generer de goal de passe immediatement sur un projet vierge. Il faut d'abord definir les lots, proposer les passes, puis valider la passe a executer. `pass_runtime_goal.md` se genere seulement pour une vraie passe `validated` ou `in_progress`.

Les nouvelles installations incluent aussi le UI Verification Harness :

```text
scripts/codex/sr_ui_verify.mjs
scripts/codex/playwright_auth_smoke.mjs  # wrapper legacy
docs/codex/skills-method/aurora-ui-visual-qa/
PROJECT_PROFILE.yaml ui_validation
```

Pour une application publique, garder `ui_validation.auth.mode = none`. Pour une application authentifiee, configurer `auth.mode = storage_state` et garder `.playwright/.auth/` hors Git.

## Mettre a jour

Dans le projet cible, coller [prompts/fr/05_upgrade_codex_environment.md](prompts/fr/05_upgrade_codex_environment.md). Codex doit auditer, preserver les fichiers projet, proposer le plan, puis seulement appliquer l'upgrade.

Pour un projet qui utilise deja une ancienne SR Method, l'upgrade doit etre non regressif :

- preserver `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `PROJECT_PROFILE.yaml`, `SKILL_MAP.md`, docs metier locales, handoffs, task memories et skills projet ;
- preserver `SR_LOTS.yaml` et les statuts de lots existants sauf preuve et validation ;
- ajouter ou rafraichir `SR_PASSES.yaml` de facon additive si absent/obsolète, sans marquer silencieusement des passes `validated` ;
- conserver les anciennes task memories et ne pas les convertir en batch vers `sr_contract.json` sans validation explicite ;
- traiter les anciens contrats sans nouveaux gates comme warnings legacy, pas comme erreurs bloquantes ;
- ajouter `ui_validation` de facon additive quand c'est possible ; si elle est absente, garder le projet utilisable pour les taches non UI mais bloquer la cloture d'un lot UI significatif tant qu'elle n'est pas configuree ;
- preserver le comportement legacy via le wrapper `playwright_auth_smoke.mjs` et privilegier `sr_ui_verify.mjs` pour les nouvelles validations UI ;
- ne jamais commiter ni imprimer de storageState Playwright, cookies ou tokens ;
- mettre a jour `docs/CURRENT_STATE.md` avec version SR avant/apres, commit source, controles, warnings et prochain prompt ;
- lancer `07_realign_sr_state_after_upgrade` avant de reprendre le developpement applicatif.
- conserver la lecture des contrats historiques `sr_contract` 3.0.0, tandis que les nouvelles task memories et lots rouverts utilisent 3.1.0 ;
- avertir lorsqu'un contrat historique multi-lots ne contient qu'un `validated_request` generique ;
- ne pas reecrire les memoires historiques en masse ; normaliser seulement le perimetre actif ou rouvert apres lecture de sa source et validation requise ;
- conserver chaque requirement ID ouvert et rouvrir son lot d'origine par defaut, sans creer de micro-lots de migration.

Les layouts officiels representatifs SR 2.2.0, 2.3.0, 2.3.5, 2.4.1 et 3.0.0 sont couverts par des regressions d'upgrade. Si une cible ancienne n'a pas de `SR_PASSES.yaml`, l'upgrade cree un registre valide `passes: []` et ne deduit aucune passe depuis les lots existants. Les layouts inconnus, partiels ou adaptes localement restent soumis a l'audit fichier par fichier du prompt `05` ; la fixture ne garantit pas toute structure locale arbitraire.

Un code retour 0 de l'installateur constitue seulement une preuve d'execution. L'upgrade n'est reussi que si `sr_post_install_check.py` est aussi vert ; sinon la cible reste en `repair` avec ses erreurs explicites.

Pour plusieurs repositories, auditer et rapporter chaque cible separement. Un resultat vert dans un dossier ne doit pas masquer une installation ancienne, partielle, rouge ou adaptee localement dans un autre.

## Verifier

Coller [prompts/fr/06_verify_sr_installation.md](prompts/fr/06_verify_sr_installation.md).

Verifier aussi la version, le changelog et les prompts publics localises :

```bash
python3 scripts/codex/validate_release_docs.py --root . --json
```

Codex doit aussi valider les passes si le fichier existe :

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

## Definir les lots SR

Apres cadrage d'une fonction ou collecte dans l'inbox, demander a Codex de definir ou promouvoir les lots avec evidence code :

```text
prompts/fr/09_define_sr_lots_from_scope.md
```

Cette etape met uniquement a jour la memoire SR et ne doit pas modifier le code applicatif.

## Definir les passes SR

Apres creation des lots ou apres upgrade d'un projet existant, coller [prompts/fr/08_define_sr_passes_from_lots.md](prompts/fr/08_define_sr_passes_from_lots.md). Cette etape met uniquement a jour la memoire SR et ne doit pas modifier le code applicatif.

## Generer un Pass Runtime Goal

Apres validation d'une passe, Codex peut generer un goal runtime :

```bash
python3 scripts/codex/build_pass_runtime_goal.py \
  --pass-id <PASS_ID> \
  --output docs/codex/tasks/YYYY-MM-DD_<pass-id>/pass_runtime_goal.md
```

La commande `/goal` generee est volontairement courte. Le script impose :

```yaml
max_goal_command_chars: 1000
hard_limit: 4000
```

Si des E2E utilisateur sont requis, Codex doit terminer la passe en `user_testing`, pas en `done`. La passe suivante doit etre proposee, jamais lancee silencieusement.

## Demarrer une session

Coller [prompts/fr/01_start_sr_session.md](prompts/fr/01_start_sr_session.md). Pour les agents IA runtime, utiliser [prompts/fr/15_define_runtime_agents.md](prompts/fr/15_define_runtime_agents.md).
