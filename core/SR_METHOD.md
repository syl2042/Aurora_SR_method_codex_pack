# SR Method

## Definition

SR signifie **Specification Runtime**.

La SR Method est la doctrine generale Auroramind pour encadrer le travail avec des agents IA dans un projet logiciel. Elle transforme des specs, une memoire projet et des gates de verification en un cadre executable par Codex ou par des agents applicatifs.

Elle comporte deux branches complementaires :

- **SR Development Method** : cadrage du developpement assiste par IA, avec lots, evidence gate, knowledge gate, verification, auto-evaluation, memoire de tache et reprise de contexte.
- **SR Agent Method** : construction d'agents IA runtime embarques dans une application, avec prompts, variables, bindings controles, schemas de sortie, traces et validation humaine.

## Positionnement

La SR Method rejoint les principes du harness engineering : l'IA n'est pas seulement appelee par un prompt, elle est encadree par un environnement de travail, des outils, des contrats et des boucles de verification.

La difference est que la SR Method applique ce principe a l'echelle complete d'un projet :

- backlog vivant ;
- cartographie codebase ;
- skills Codex et skills runtime separees ;
- gates de preuve ;
- memoire long terme ;
- budget contexte ;
- verification humaine et automatisee ;
- agents runtime applicatifs.

## Validation humaine stricte

La SR Method supporte un mode de validation humaine stricte, activable par `AGENTS.md`, par un lot, par une reprise ou par l'utilisateur. Dans ce mode, Codex peut analyser, lire et recommander sans validation, mais ne modifie aucun fichier et ne lance aucune action de mutation tant que l'utilisateur n'a pas ecrit exactement `je valide`.

La validation ne couvre que l'action ou le plan decrit juste avant. Toute extension de perimetre, dependance, migration, configuration, donnees, agent IA runtime, backlog, publication Git, action destructive ou changement metier exige une nouvelle validation explicite.

## SR 3.0.0 - Contrat vivant de lot

A partir de SR 3.0.0, la cible machine d'un lot non trivial est un contrat vivant :

```text
docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

Ce contrat ne remplace pas instantanement l'historique existant. Les fichiers `task_plan.md`, `findings.md`, `progress.md`, `decisions.md`, `verification.md`, `gate_report.md` et `loop_contract.json` restent lisibles pendant la transition, mais la source machine cible devient `sr_contract.json`.

Le contrat 3.0.0 doit porter explicitement :

- les intentions utilisateur validees dans `validated_requests` ;
- le scope inclus/exclu ;
- les verites produit/metier a ne pas perdre ;
- les sources lues et preuves ;
- les skills methode et metier ;
- le plan, les constats et decisions ;
- les fichiers modifies ;
- les commandes de verification ;
- les gates ;
- les tests E2E utilisateur ;
- le statut contexte ;
- la decision de transition conversationnelle.

Regle centrale : un lot ne peut pas etre `done` si une intention validee reste `todo`, `doing`, `requires_e2e` ou `blocked`.

Validation :

```bash
python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/YYYY-MM-DD_slug/sr_contract.json
```

La migration des anciennes tasks vers ce format est un lot separe. Tant que ce lot de migration n'a pas ete execute, ne pas supprimer les fichiers legacy.

## Regle de compatibilite

Les anciens noms techniques restent acceptes :

- `SR_HARNESS_METHOD.md` est l'alias historique de la SR Development Method.
- `AI_AGENT_RUNTIME_METHOD.md` est l'alias historique de la SR Agent Method.

Ne pas casser les projets existants pour un renommage de fichiers. Preferer ajouter les nouveaux docs et garder les anciens chemins comme alias.
