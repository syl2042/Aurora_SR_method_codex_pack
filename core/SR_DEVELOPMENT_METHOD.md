# SR Development Method

## Objectif

La SR Development Method encadre le developpement assiste par Codex dans un projet logiciel.

Elle vise a reduire les iterations inutiles en forcant Codex a :

- verifier les fichiers avant de recommander ;
- travailler par lots explicites ;
- maintenir une memoire de tache ;
- executer les verifications utiles ;
- produire une liste E2E utilisateur concrete ;
- auto-evaluer son travail avant cloture ;
- surveiller le budget contexte ;
- creer un prompt de reprise quand la session devient longue.

## Boucle standard

```text
demande utilisateur
-> bootstrap SR
-> objectif verifiable
-> classification backlog
-> knowledge gate : RepoMap/KG -> fichiers candidats -> code reel
-> evidence gate
-> plan court
-> implementation ciblee
-> verification
-> repair loop si necessaire
-> loop contract
-> gate report
-> mise a jour memoire/backlog
-> cloture avec tests E2E utilisateur
```

## Contrat de boucle

A partir de SR 2.4.0, toute tache non triviale doit produire ou mettre a jour :

```text
docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
```

Ce fichier est volontairement court. Il ne contient pas les logs ni les details longs. Il declare seulement les preuves minimales permettant de verifier que la boucle SR a ete appliquee.

Le validateur de reference est :

```bash
python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/loop_contract.json
```

## Relation avec SR_HARNESS_METHOD.md

`SR_HARNESS_METHOD.md` reste le document operationnel historique. Il detaille les lots, niveaux d'autonomie, gates et conditions d'arret. La SR Development Method est le nom public de cette branche.
