# Aurora SR Method Codex Pack

SR Method 4.1 est un harness d’exécution allégé pour Codex : noyau permanent court, procédures conditionnelles, déclencheurs de skills précis, état compact et vérification finale proportionnée.

Statut : **4.1.0 (`released`)**, publiée le 2026-09-24.

**FR** · [English](README.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt.md)

[Installation](INSTALLATION.fr.md) · [Changelog](CHANGELOG.md) · [Installer](prompts/fr/00_install_codex_environment.md) · [Mettre à jour](prompts/fr/05_upgrade_codex_environment.md) · [Vérifier](prompts/fr/06_verify_sr_installation.md) · [Réaligner](prompts/fr/07_realign_sr_state_after_upgrade.md)

## Ce qui change en 4.1

- `AGENTS.md` est réconcilié et raccourci au lieu de recevoir un manuel supplémentaire.
- Le catalogue cognitif par défaut est limité à l’exécution de lots, au diagnostic, à l’architecture et à la validation visuelle UI.
- TDD, planning par fichiers, compression terminal, revue finale et maintenance RepoMap ne sont plus des skills.
- Aucun test volontairement rouge, gate rouge artificiel ou boucle de rollback pendant le développement source.
- Scope, Vérification et Activation sont les seules frontières d’exécution.
- Une nouvelle tâche peut utiliser un unique `task_state.yaml` compact ; les anciens contrats restent lisibles.
- Le mode `core` n’effectue aucun appel MCP. `nexus_kg` suit un `MCP_POLICY.yaml` explicite : capacités différées, allowlists, approbations et budgets de résultat.
- Occupation du contexte, entrée non cachée, cache, sortie et résultats d’outils sont mesurés séparément.
- Les tests et fixtures de qualification restent dans le pack source ; les projets ne reçoivent que l’outillage d’exécution.

## Modèle d’exécution

```text
noyau AGENTS.md
  -> SR_ROUTES.json
  -> procédure déclenchée uniquement
  -> zéro à deux skills spécialisées
  -> sources réelles et outils bornés
  -> vérification finale proportionnée
```

Les questions simples et petites modifications restent sur le chemin rapide. Le harness s’applique au multi-lots. Les règles de build ou déploiement ne sont chargées qu’après une demande explicite d’activation.

## Installation ou mise à jour

Sélectionner explicitement `SR_PACK_SOURCE` et le dépôt cible. Une cible sans marqueur SR utilise le prompt `00` ; toute cible contenant des marqueurs SR utilise le prompt `05`.

La mise à jour est agnostique à la version précédente : le numéro déclaré sert uniquement à la provenance. Les fichiers réels sont classés comme absents, gérés, modifiés localement, non gérés, obsolètes, conflictuels ou déjà alignés. Les états projet sont préservés et un ancien artefact géré n’est supprimé que si son contenu est reconnu.

```bash
# prévisualisation en lecture seule
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json

# cible neuve, après validation
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --write

# cible existante ou partielle, après validation
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
  --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

Puis exécuter :

```bash
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Le code retour de l’installateur ne suffit pas. Il faut contrôler préservation, conflits, post-installation et réalignement produit restant. Voir [INSTALLATION.fr.md](INSTALLATION.fr.md).

## Compatibilité

- Les installations anciennes, partielles, sans version ou adaptées localement sont évaluées par leur contenu.
- Lots, passes, mémoires, exigences ouvertes et skills locales restent propriété du projet.
- Les anciens contrats restent lisibles sans réécriture massive.
- Un fichier pack inconnu et modifié est préservé ou signalé, jamais écrasé silencieusement.
- Code applicatif, secrets, dépendances, migrations et déploiements restent hors d’une mise à jour de méthode.

## Carte du dépôt

- `core/` : méthode, routes, procédures, profils et politiques.
- `skills-method/` : petit catalogue de skills méthode distribuées.
- `scripts/install_codex_pack.py` : preview et convergence transactionnelle.
- `scripts/codex/` : validation, audit et outils bornés.
- `prompts/` : prompts publics et traductions.
- `tasks/_TEMPLATE/` : état compact et modèles historiques encore lisibles.
- `tools/sr-cockpit/` : interface opérateur optionnelle, non installée dans les projets cibles.

L’historique et les notes de migration vivent uniquement dans [CHANGELOG.md](CHANGELOG.md).
