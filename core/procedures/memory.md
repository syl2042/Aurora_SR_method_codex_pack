# memory — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## 9. Mise a jour memoire

Mettre a jour :

- `progress.md` ;
- `verification.md` ;
- `decisions.md` ;
- `SR_LOTS.yaml` ;
- `CURRENT_STATE.md` pour tout upgrade SR, realignement SR, changement de version SR, creation de `NEXT_SESSION_PROMPT.md`, modification structurante de `SR_LOTS.yaml`, lot applicatif significatif passe en `done` ou `user_testing`, ou fin de session significative ;
- RepoMap si structure changee.
- Nexus KG si mode `nexus_kg` et changement structurel ou lot termine.

Si `SR_LOTS.yaml` a ete modifie pendant le lot, valider le backlog avant cloture :

```bash
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
```

Si `SR_PASSES.yaml` a ete modifie ou utilise pour une execution multi-lots, valider la passe avant cloture :

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

Si un `pass_runtime_goal.md` a ete utilise, verifier que le Goal Length Gate a ete documente et que la commande `/goal` ne depasse pas `max_goal_command_chars`. La passe ne doit pas etre marquee `done` si des E2E utilisateur ou une validation humaine restent requis ; utiliser `user_testing` avec checklist E2E concrete.

Cette validation est obligatoire meme si `git diff --check` est vert. `git diff --check` ne valide pas les champs obligatoires du contrat de lot et peut manquer un fichier non suivi.

Si `SR_LOTS.yaml` n'a pas ete modifie apres une tache non triviale, documenter dans `gate_report.md` ou le contrat pourquoi le Backlog Mutation Gate conclut `no_backlog_mutation_required`.

## Planning with files

Pour toute tache non triviale, creer/mettre a jour :
```text
docs/codex/tasks/YYYY-MM-DD_slug/task_plan.md
docs/codex/tasks/YYYY-MM-DD_slug/findings.md
docs/codex/tasks/YYYY-MM-DD_slug/progress.md
docs/codex/tasks/YYYY-MM-DD_slug/decisions.md
docs/codex/tasks/YYYY-MM-DD_slug/verification.md
docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
```

## Memoire de tache

Creer ou reprendre :

```text
docs/codex/tasks/YYYY-MM-DD_slug/
  sr_contract.json
  task_plan.md
  findings.md
  progress.md
  decisions.md
  verification.md
  loop_contract.json
```

En SR 3.1.0, `sr_contract.json` est la cible machine du lot. Il doit lister les intentions utilisateur granulaires dans `validated_requests`, separer implementation et preuve, heriter des demandes ouvertes lors d'une reprise et etre valide avec :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Pendant la transition, les fichiers legacy restent crees ou maintenus si le projet les exige. Ne pas les supprimer sans lot de migration explicite.

Le `task_plan.md` doit contenir au minimum :
- objectif verifiable ;
- hypotheses ;
- sources lues ;
- skills utilisees ;
- fichiers candidats puis fichiers confirmes apres lecture ;
- perimetre valide et table de couverture prevue si un lot ou une passe a ete valide ;
- Propagation Gate preflight si un symbole ou contrat partage peut changer : consommateurs, surfaces a risque, niveau de risque, validation humaine requise et verifications prevues ;
- risques ;
- plan court ;
- verification prevue.


## Vues derivees SR 4
Utiliser `python3 scripts/codex/render_sr_state.py --file <sr_contract.json>` pour produire la table de couverture depuis le contrat canonique; `--json` expose les champs derives. La commande est en lecture seule et retourne un echec si le contrat est invalide. Sa sortie peut etre capturee comme artefact de verification, sans reecrire le texte par LLM. Mettre a jour uniquement les faits changes dans les fichiers memoire existants. Ne jamais transformer un resultat derive en preuve de test ou acceptation humaine. Les schemas et conditions de validation restent ceux des validateurs.
