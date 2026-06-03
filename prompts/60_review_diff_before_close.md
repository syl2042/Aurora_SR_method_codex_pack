# Revue de diff avant cloture

Verifier demande, scope, securite, dependances/migrations, tests, CURRENT_STATE, RepoMap/KG, risques restants, appliquer le Fact Gate puis le Self Evaluation Gate, puis valider le SR Contract 3.0.0 et le Loop Contract si la tache est non triviale.

Commande attendue si un contrat existe :

```bash
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
```

Commande attendue si un SR Contract existe :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Commande obligatoire si `docs/codex/SR_LOTS.yaml` a ete modifie :

```bash
python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml
```

`git diff --check` ne remplace pas cette validation du backlog.

Repondre OK cloture ou corrections requises avec :

- ce qui est fait ;
- resultat observe ;
- verifications executees ;
- validation `SR_LOTS.yaml` si le backlog a ete modifie ;
- memoire SR mise a jour ;
- SR Contract 3.0.0 valide ou raison de non-applicabilite, avec couverture `validated_requests` ;
- Loop Contract valide ou raison de non-applicabilite, avec decision `conversation_transition` et `resume_protocol` si reprise nouvelle conversation ;
- tests E2E utilisateur a faire ;
- prochain lot ou point d'arret.
