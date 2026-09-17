# resume — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Relation avec handoff

Le handoff sert a passer d'une conversation a l'autre.

SR-Harness impose que le handoff reference :

- lots ouverts ;
- lots en test utilisateur ;
- exigences validees, faites, partielles et non faites avec leurs identifiants stables ;
- preuves manquantes et tests restant a executer ;
- retours utilisateur rattaches et lots rouverts ;
- decisions actives ;
- stop conditions ;
- prochain ensemble coherent a traiter.

Un handoff ou un compact ne peut jamais retirer silencieusement une exigence ouverte. La reprise commence par le registre herite et non par la proposition d'un nouveau gate cible.

## Continuity rule

Cloture obligatoire : memoire SR, lots traites, gates, fait, fichiers modifies, verifications, tests E2E utilisateur, risques, decisions, prochaine etape, CURRENT_STATE a mettre a jour, RepoMap a mettre a jour.
Si `SR_LOTS.yaml` a ete modifie, inclure explicitement le resultat de `validate_lot_contract.py`.


## Controles conserves du prompt de reprise

- Verifier rapidement la version SR avec `python3 scripts/codex/audit_codex_pack.py` si le script existe.
- Verifier le contrat projet avec `python3 scripts/codex/audit_sr_project.py --root .` si le script existe.
- Verifier la disponibilite du Loop Contract avec `test -f docs/codex/tasks/_TEMPLATE/loop_contract.json && test -f scripts/codex/validate_loop_contract.py`.
- Verifier la disponibilite du SR Contract 3.1.0 avec `test -f docs/codex/tasks/_TEMPLATE/sr_contract.json && test -f scripts/codex/validate_sr_contract.py`.
- Verifier le budget contexte avec `python3 scripts/codex/context_budget_report.py --root . --compact` si le script existe. Si le statut est `green`, ne pas l'afficher sauf demande explicite ; sinon appliquer le Context budget gate.
- Pour toute tache non triviale reprise dans cette conversation, prevoir `sr_contract.json` avec `validated_requests` heritees sans perte et une decision finale `conversation_transition` dans `loop_contract.json`.
- Si une nouvelle conversation est recommandee ou imposee, verifier que `resume_protocol.next_user_prompt` existe dans le contrat de boucle.

## Continuite conservee

Ne lire `SR_LOTS.yaml`, `CODEBASE_MAP.md`, les docs methode completes ou le code reel qu'apres validation utilisateur ou demande explicite de continuer. Cette regle reduit les tokens et evite de transformer une reprise vague en execution de lot.

## Continuite conservee

Ne pas creer ce fichier pour chaque micro-tache. Le creer ou le rafraichir quand le risque de perte de contexte devient reel : contexte orange/rouge, pause utilisateur, fin de batch multi-lots, changement de macro-fonction, upgrade, realignement ou decision structurante.

## Continuite conservee

Utiliser ce prompt apres un stop contexte `orange`, `red`, `unknown`, `stale` ou `ambiguous`, sauf si l'utilisateur veut explicitement continuer le developpement. Le chemin du `NEXT_SESSION_PROMPT.md` est toujours connu : le preciser dans le prompt.

## Continuite conservee

Avant de coder :
- si la demande utilisateur est vague (`reprends`, `resume`, `continue`), appliquer `Reprise SR stricte` : lire ce fichier, resumer, puis attendre validation ;
- charger `sr_contract.json` 3.1.0 et verifier que toutes les exigences ouvertes du parent sont heritees ;
- traiter par defaut tout retour sur une fonction validee comme `existing_requirement_repair`, rattache au lot d'origine ;
- ne pas proposer un nouveau micro-lot ou seulement le prochain gate cible si une exigence techniquement incomplete de la passe precedente reste ouverte ;
- appliquer evidence_gate ;
- appliquer knowledge_gate : RepoMap/KG -> fichiers candidats -> lecture code reel ;
- mettre a jour SR_INBOX/SR_LOTS si ma demande modifie le backlog ;
- demander validation si le lot est seulement proposed/planned ou si une action sensible apparait.
- utiliser aurora-lot-runner si plusieurs lots sont ouverts ;
- traiter jusqu'a 3 lots `repair`/`reopened` puis `validated` si les gates restent verts ;
- executer `context_budget_report.py --root . --compact` avant toute reponse de cloture ou d'avancement significatif ; ne rien afficher si le statut est `green` ;
- appliquer self_evaluation_gate apres patch ;
- donner les tests E2E utilisateur apres chaque lot livre.
```
