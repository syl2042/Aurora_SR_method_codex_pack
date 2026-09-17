# verification — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Verification gate

Les commandes du lot doivent etre executees ou l'impossibilite documentee.

Quand le Propagation Gate est requis, le Verification Gate doit inclure les recherches de references et les tests consommateurs proportionnes au risque, ou documenter pourquoi une verification equivalente a ete choisie.

## 6. Verification

Executer les commandes `verification_commands` du lot.

Si le Propagation Gate est requis, executer aussi le postcheck :

- recherches sur ancien et nouveau symbole ou contrat ;
- controle des references restantes et justification des exceptions ;
- verification des consommateurs directs ;
- typecheck/build/lint/tests/smoke/E2E proportionnes au risque.

Si une commande est impossible :

- expliquer pourquoi ;
- proposer un smoke alternatif ;
- ne pas masquer l'echec.

## 7. Repair loop

Si une verification echoue :

- diagnostiquer ;
- corriger au maximum `max_repair_attempts_per_lot` ;
- relancer la verification ciblee.

Si toujours rouge, stopper avec blocker clair.

Un retour utilisateur concernant une exigence deja validee n'est pas une nouvelle micro-demande. Le classer par defaut `existing_requirement_repair`, retrouver son `requirement_id`, rouvrir le lot d'origine, conserver toutes les autres exigences ouvertes et reexecuter leur checklist consolidee. Ne creer un nouveau lot que si la classification conclut `new_requirement` ou `scope_change` hors scope existant, avec justification explicite.

## Verification

Une tache n'est terminee que si la verification pertinente est executee ou l'impossibilite documentee.
Tests E2E utilisateur :
Pour tout lot livre, fournir aussi la liste courte des tests E2E utilisateur a effectuer, meme si les tests automatises sont verts.
