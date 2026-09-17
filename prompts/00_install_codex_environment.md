# Installer SR 4.0.0 dans un projet cible neuf

## SR 4.0.0 — version publiee

Source cible : choisir explicitement `SR_PACK_SOURCE`, soit une version publiee identifiee, soit le candidat local SR 4.0.0 autorise. Lire `core/SR_PACK_VERSION.json` (`version`, `release_status`) et noter `source_commit`, l'etat Git et, si le clone est modifie, une empreinte du contenu source incluant les fichiers non suivis utilises. Un candidat `unreleased` ne doit pas etre presente comme une release. Ne pas remplacer une source candidate par un clone de la derniere version publiee ; si la source demandee manque, s'arreter et clarifier avant installation.

Pour cette cible SR 4.0.0, la source doit annoncer `version: 4.0.0`. Si aucune release 4.0.0 n’est publiee, utiliser uniquement le candidat local autorise ou signaler son absence ; ne pas installer silencieusement une autre version.

Previsualiser avec la commande ci-dessous avant validation ; apres `je valide`, choisir uniquement le mode correspondant au parcours. `--plan-out` ecrit un plan local et exige une autorisation ; `--apply-plan` refuse un diagnostic perime. `--restore` est une operation distincte, sur le journal exact de la transaction, et refuse les modifications ulterieures. Ne pas contourner un conflit en supprimant un fichier.

Les plans enregistres contiennent les contenus des fichiers : les conserver localement. Definir `SR_TARGET` comme chemin du repository cible.

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Tu travailles dans un repository logiciel qui doit recevoir Aurora SR Method pour la premiere fois.

Objectif verifiable : installer le pack SR 4.0.0 et ses contrats cibles (`sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4, `SR_PASSES` 0.2), verifier l'installation, puis stopper avant tout developpement applicatif.

`SR_PASSES.yaml` doit etre installe avec `passes: []`. Ce registre vide est valide : aucune passe produit ne doit etre inventee pendant l'installation neuve. Les passes sont proposees ensuite par le prompt `08`, apres lecture des lots et validation humaine.

Utilise uniquement la source officielle : `https://github.com/syl2042/Aurora_SR_method_codex_pack`.

Regles strictes :

- Ne modifie aucun code applicatif, migration, dependance, secret, configuration ou regle metier.
- Inspecte le repository cible et le `AGENTS.md` le plus proche avant d'ecrire.
- Si `docs/codex/SR_PACK_VERSION.json`, `docs/codex/SR_METHOD.md` ou `docs/codex/SR_LOTS.yaml` existe deja, ce n'est pas une installation neuve. Stoppe et utilise `05_upgrade_codex_environment.md`.
- Avant mutation, rapporte les fichiers a creer, ceux a preserver et les controles prevus ; attends la validation humaine requise par le projet.
- N'invente aucune `validated_request`, aucun lot valide et aucune passe executable. Un template n'est pas un perimetre produit valide.
- N'utilise jamais `--write` pour mettre a jour un projet SR existant ; utilise `--upgrade` seulement apres un audit par projet.

Apres validation :

1. Identifier un clone local verifie du pack officiel et noter son commit source.
2. Classer la cible `fresh_install` apres verification des marqueurs SR ci-dessus.
3. Lancer l'installateur avec `--profile default --write`.
4. Verifier `SR_PACK_VERSION.json`, `CHANGELOG.md`, `SR_LOTS.yaml`, `SR_PASSES.yaml`, les templates de task memory, les validateurs et les prompts publics localises `01`, `05`, `06`, `07`, `08`, `09` et `15`.
5. Confirmer que `sr_contract.json` separe `implementation_status` de `evidence_status` et contient `validated_requests` granulaires, lineage, closure et un Completion Gate derive.
6. Lancer `audit_codex_pack.py`, `sr_post_install_check.py`, `validate_release_docs.py`, les validateurs lots/passes et les validateurs des templates loop/SR.
7. Verifier Pass Runtime Goal et UI Verification Harness. Garder `.playwright/.auth/` hors Git et ne demander aucun credential pendant l'installation.
8. Ne generer aucun `/goal`. Recommander `09_define_sr_lots_from_scope.md`, puis `08_define_sr_passes_from_lots.md`, et ne generer un goal que pour une passe validee par l'utilisateur.
9. Rapporter la classification `fresh_install`, la version cible, le commit source, les fichiers ajoutes/preserves, les controles verts/rouges, les warnings et confirmer qu'aucun fichier applicatif n'a change.

Fin obligatoire : installer la methode ne valide aucun perimetre produit. Attends une demande utilisateur explicite avant de definir ou d'executer des lots applicatifs.

Parcours : installation neuve `00 -> 06` ; installation existante `05 -> 06 -> 07`. Le prompt `06` controle seulement ; `07` propose le realignement puis attend `je valide` avant modification de la memoire. Aucun developpement applicatif n'est autorise par ces parcours.
