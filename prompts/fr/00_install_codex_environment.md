# Installer SR 3.7 dans un projet cible neuf

Tu travailles dans un repository logiciel qui doit recevoir Aurora SR Method pour la premiere fois.

Objectif verifiable : installer le pack SR 3.7.0 et ses contrats cibles (`sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4, `SR_PASSES` 0.2), verifier l'installation, puis stopper avant tout developpement applicatif.

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
