# Installer SR 3.7 dans un projet neuf

Tu travailles dans un repository logiciel qui doit recevoir Aurora SR Method pour la premiere fois.

Objectif verifiable : installer le pack SR 3.7.0 et ses contrats cibles (`sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4, `SR_PASSES` 0.2), verifier l'installation, puis stopper avant tout developpement applicatif.

`SR_PASSES.yaml` doit etre installe avec `passes: []`. Ce registre vide est valide : aucune passe produit ne doit etre inventee pendant l'installation neuve. Les passes sont proposees ensuite par le prompt `08`, apres lecture des lots et validation humaine.

Source officielle :

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Regles strictes :

- Ne modifie aucun code applicatif, migration, dependance, secret ou regle metier.
- Inspecte d'abord le repository cible et son `AGENTS.md` le plus proche.
- Si `docs/codex/SR_PACK_VERSION.json`, `docs/codex/SR_METHOD.md` ou `docs/codex/SR_LOTS.yaml` existe deja, ce n'est pas une installation neuve : stoppe et utilise `05_upgrade_codex_environment.md`.
- Avant toute mutation, presente les fichiers a creer, les fichiers existants a preserver et les commandes de verification, puis attends la validation humaine exigee par le projet.
- N'invente aucune `validated_request`, aucun lot `validated` et aucune passe executable. Les templates peuvent contenir des exemples explicites, jamais un faux perimetre utilisateur.
- N'utilise jamais `--write` pour mettre a niveau un projet existant ; l'installateur doit refuser ce cas et imposer `--upgrade` apres audit.

Etapes :

1. Identifier ou cloner une copie locale verifiee du pack officiel et noter son commit source.
2. Confirmer par lecture que le projet est `fresh_install` et qu'aucun marqueur SR existant n'est present.
3. Creer une task memory d'installation si les regles du projet l'exigent.
4. Apres validation, lancer :

   ```bash
   python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" \
     --source "$SR_PACK_SOURCE" \
     --target . \
     --profile default \
     --write
   ```

5. Verifier la presence de `AGENTS.md`, `docs/codex/SR_PACK_VERSION.json`, `docs/codex/CHANGELOG.md`, `SR_LOTS.yaml`, `SR_PASSES.yaml`, des templates de task memory, des validateurs et des prompts publics localises `01`, `05`, `06`, `07`, `08`, `09` et `15`.
6. Verifier que le template `sr_contract.json` separe `implementation_status` et `evidence_status`, contient `validated_requests`, `lineage`, `closure` et un Completion Gate derive.
7. Lancer au minimum :

   ```bash
   python3 scripts/codex/audit_codex_pack.py --root . --json
   python3 scripts/codex/sr_post_install_check.py --root . --json
   python3 scripts/codex/validate_release_docs.py --root . --json
   python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
   python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
   python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json
   python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json
   ```

8. Verifier l'outillage Pass Runtime Goal et UI Verification Harness. Pour une application authentifiee, garder `.playwright/.auth/` hors Git ; ne demander aucun secret pendant l'installation.
9. Ne generer aucun `/goal`. Recommander ensuite `09_define_sr_lots_from_scope.md`, puis `08_define_sr_passes_from_lots.md`, puis un Pass Runtime Goal seulement pour une passe validee.
10. Produire le rapport : classification `fresh_install`, version et commit source, fichiers ajoutes/preserves, controles verts/rouges, warnings, absence de code applicatif modifie et prochaine validation humaine.

Fin obligatoire : l'installation de la methode ne valide aucun perimetre produit. Attends une demande utilisateur explicite avant de definir ou d'executer des lots applicatifs.
