# Installation — SR Method 4.1

Statut : version publiée `4.1.0`. Sélectionner explicitement `SR_PACK_SOURCE` et relever son `release_status`, son `source_commit` et son état Git.

[English](INSTALLATION.md) · [Deutsch](INSTALLATION.de.md) · [Español](INSTALLATION.es.md) · [Português](INSTALLATION.pt.md)

## Choisir le parcours

| État observé | Prompt | Mode installateur |
|---|---|---|
| Aucun marqueur SR | `prompts/fr/00_install_codex_environment.md` | `--write` |
| Un marqueur SR, état partiel ou inconnu | `prompts/fr/05_upgrade_codex_environment.md` | `--upgrade` |

Ne jamais choisir l’algorithme depuis le numéro de version précédent. La mise à jour s’appuie sur le contenu réel, les empreintes gérées et les modifications locales.

## Prévisualiser

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Examiner chaque conflit et fichier préservé. `--plan-out` est facultatif et enregistre localement le contenu des fichiers ; protéger ce plan.

## Appliquer après validation

```bash
# cible neuve
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --write

# cible existante, partielle, sans version ou adaptée localement
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

La transaction protège la preview contre les modifications concurrentes, sauvegarde les fichiers touchés et permet un `--restore` exact. Elle refuse d’écraser une modification postérieure.

## Convergence des fichiers

| État | Action |
|---|---|
| absent | Créer la cible. |
| géré intact | Mettre à jour sûrement. |
| bloc géré entouré de règles locales | Remplacer le bloc et préserver les règles locales. |
| propriété du projet | Préserver ; ajouter uniquement les valeurs sûres définies. |
| fichier pack personnalisé inconnu | Signaler un conflit, ne pas écraser. |
| ancien fichier géré reconnu | Supprimer transactionnellement. |
| ancien fichier modifié localement | Préserver et signaler. |
| déjà aligné | Aucune opération. |

La mise à jour ne ferme aucun lot applicatif, ne réécrit pas les mémoires historiques, ne modifie pas le produit et ne déploie rien.

## Vérifier

```bash
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" \
  --root "$SR_TARGET" --json
```

Le post-check est en lecture seule par défaut. Ajouter `--write-report` uniquement si un artefact d’audit persistant est souhaité.

Le résultat doit prouver la version `4.1.0`, les fichiers requis, le noyau AGENTS court, le catalogue de skills actif, les routes, la documentation et la préservation. Utiliser ensuite `prompts/fr/07_realign_sr_state_after_upgrade.md` uniquement si l’état projet nécessite un réalignement.

Une installation neuve inclut `SR_LOTS.yaml`, `SR_PASSES.yaml` avec `passes: []`, `MCP_POLICY.yaml`, `task_state.yaml`, le validateur UI et les lecteurs des anciens contrats. Aucun lot, aucune passe et aucune capacité MCP produit ne sont inventés.
