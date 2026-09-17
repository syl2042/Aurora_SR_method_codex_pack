# runtime-goal — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Pass Runtime Goal

Le Pass Runtime Goal est une couche d'execution optionnelle pour Codex CLI `/goal`.

Il ne remplace jamais `SR_PASSES.yaml`, `SR_LOTS.yaml` ni les `sr_contract.json`. Il est genere depuis une passe SR et sert uniquement a maintenir Codex en execution jusqu'au statut final correct de la passe.

Politique :

- `SR_PASSES.yaml`, `SR_LOTS.yaml` et les contrats de lots restent la source de verite ;
- `pass_runtime_goal.md` est un artefact derive et peut etre regenere ;
- une commande `/goal` doit rester courte et pointer vers `pass_runtime_goal.md` ;
- `max_goal_command_chars` vaut `1000` par defaut ;
- `hard_limit` vaut `4000` et ne doit jamais etre depasse ;
- si la commande depasse `max_goal_command_chars`, Codex doit la regenerer en forme plus courte ;
- si elle depasse encore `max_goal_command_chars` ou `hard_limit`, le Goal Length Gate est rouge et le goal ne doit pas etre lance ;
- une passe `proposed` ne doit jamais etre executee par goal ;
- une passe `planned` peut servir a un dry-run de generation, mais pas a une execution sans validation utilisateur ;
- une passe `validated`, `in_progress`, `repair` ou `reopened` peut recevoir un goal d'execution ;
- le goal s'arrete a la fin de la passe et propose la suivante sans l'enchainer silencieusement.

Generation recommandee :

```bash
python3 scripts/codex/build_pass_runtime_goal.py --pass-id <PASS_ID> --output docs/codex/tasks/YYYY-MM-DD_<pass-id>/pass_runtime_goal.md
```

La commande `/goal` produite doit etre copiee telle quelle depuis la sortie du script. Pour preparer une passe `planned` sans l'executer, utiliser `--allow-planned` et conserver le statut `planned` tant que l'utilisateur n'a pas valide.

## Goal Length Gate

Avant de lancer `/goal`, Codex doit verifier :

```text
Goal Length Gate:
- pass_runtime_goal.md genere : oui/non
- max_goal_command_chars: 1000
- hard_limit: 4000
- goal_command_chars: ...
- decision: pass / fail
```

Si `decision = fail`, stopper avant execution et corriger le fichier ou le chemin de sortie. Le depassement du seuil n'est pas une alerte cosmetique : il bloque le lancement du goal.

## 1c. Pass Runtime Goal

Si la passe est `validated`, `in_progress`, `repair` ou `reopened` et que `PROJECT_PROFILE.yaml` active `sr_passes.pass_runtime_goal.enabled`, generer un artefact runtime avant l'execution :

```bash
python3 scripts/codex/build_pass_runtime_goal.py --pass-id <PASS_ID> --output docs/codex/tasks/YYYY-MM-DD_<pass-id>/pass_runtime_goal.md
```

Le goal est derive de `SR_PASSES.yaml` et `SR_LOTS.yaml`. Il ne remplace jamais les contrats SR.

Goal Length Gate obligatoire :

- `max_goal_command_chars: 1000` ;
- `hard_limit: 4000` ;
- si la commande `/goal` depasse `1000` caracteres apres regeneration compacte, stopper ;
- si elle depasse `4000` caracteres, stopper obligatoirement ;
- ne pas lancer un goal pour une passe `proposed` ;
- ne pas executer une passe `planned` sauf validation utilisateur explicite et changement de statut SR.

Si `e2e_strategy.mode` vaut `grouped_at_pass_end`, le goal doit interdire la demande d'E2E utilisateur lot par lot. Codex accumule les preuves automatisees puis produit une checklist E2E groupee en fin de passe.


## Regle distribuee par ancien installateur

- Pass Runtime Goal : pour une passe `validated`/`in_progress`/`repair`/`reopened` executee avec `/goal`, generer `pass_runtime_goal.md` avec `python3 scripts/codex/build_pass_runtime_goal.py`, appliquer le Goal Length Gate (`max_goal_command_chars: 1000`, `hard_limit: 4000`) et ne pas enchainer une passe suivante sans validation utilisateur.
