# WORKFLOW_CODEX.md - SR Method

## Workflow standard
Bootstrap SR, comprendre, reformuler, identifier hypotheses, consulter `SKILL_DIGEST.md`, selectionner skills methode et metier, lire uniquement les `SKILL.md` selectionnes, lire sources, creer task memory, planifier, attendre validation si risque, implementer petite tranche, verifier, reviewer diff, cloturer.

Avant une reponse non triviale, appliquer le Fact Gate : classer les elements de reponse en `opinion/methode`, `fait_verifiable` ou `hypothese_non_verifiee`. Tout fait verifiable doit etre prouve par une source locale ou officielle accessible avant conclusion, sinon rester explicitement au statut d'hypothese.

Si le mode validation humaine stricte est actif dans `AGENTS.md`, un lot, une reprise ou la demande utilisateur, Codex peut analyser sans validation mais ne modifie aucun fichier et ne lance aucune action de mutation tant que l'utilisateur n'a pas ecrit exactement `je valide`. La validation ne couvre que le perimetre decrit juste avant.

## Bootstrap obligatoire
Au debut d'une conversation, apres compact, apres resume ou apres handoff, lire `SR_BOOTSTRAP.md`.
Pour toute tache non triviale, creer ou reprendre la memoire de tache avant modification.

## Domaine metier
Si la tache touche objets metier, workflows, ecrans metier, validations humaines, donnees sensibles ou integration verticale :
- lire `DOMAIN_EXPERTISE_BOOTSTRAP.md` ;
- selectionner une skill metier Codex ;
- si aucune skill n'existe, proposer sa creation avant de coder.

## Agents IA runtime
Si la tache touche LLM, agent IA applicatif, prompt, outil, orchestration, structured output, RAG/Nexus ou skill runtime :
- lire `AI_AGENT_RUNTIME_METHOD.md` ;
- utiliser le pattern prompt + bindings controles + skills runtime + JSON schema + validation + traces ;
- exiger validation humaine pour les actions critiques.

## SR Development Method et lots
Si la tache concerne une roadmap, un gros brief, une reprise longue, plusieurs lots ou une phase autonome bornee :
- lire `SR_HARNESS_METHOD.md` et `LOT_EXECUTION_METHOD.md` ;
- utiliser `aurora-lot-runner` ;
- maintenir `SR_INBOX.yaml` et `SR_LOTS.yaml` ;
- appliquer knowledge_gate puis evidence_gate avant plan/faisabilite ;
- appliquer fact_gate avant toute conclusion factuelle sur l'existant ;
- produire `gate_report.md` apres execution d'un lot ;
- produire et valider `loop_contract.json` pour toute tache non triviale ;
- appliquer le Self Evaluation Gate apres patch et avant cloture ;
- verifier `context_budget_report.py` avant d'enchainer un lot long si le script existe ;
- stopper si un gate critique est rouge ou si une validation humaine est requise.

## Knowledge modes
Mode `core` : RepoMap obligatoire, puis lecture ciblee du code reel.

Mode `nexus_kg` : RepoMap + Nexus KG quand disponible, puis lecture ciblee du code reel.

Le KG et RepoMap orientent. Les sources finales restent le code, les tests et les logs.

## Stop conditions
S'arreter si regle metier absente, skill metier manquante, architecture, dependance, migration, securite, secret, connecteur externe, agent runtime non valide, SQL libre LLM, plan invalide, hors-perimetre, gate SR-Harness rouge ou contexte trop long sans handoff.

## Fin de tache SR obligatoire
- Resume.
- Fichiers modifies.
- Verifications executees.
- Loop Contract valide ou raison de non-applicabilite.
- Risques restants.
- Decisions prises.
- Prochaine etape.
- CURRENT_STATE.md a mettre a jour ?
- RepoMap/KG a mettre a jour ?

## CURRENT_STATE.md
Mettre a jour apres tranche significative, architecture, route majeure, agent runtime, integration, bug bloquant.

En mode SR plein regime, `CURRENT_STATE.md` est obligatoire apres tout upgrade SR, realignement SR, changement de version SR, creation de `NEXT_SESSION_PROMPT.md`, modification structurante de `SR_LOTS.yaml`, lot applicatif significatif passe en `done` ou `user_testing`, ou fin de session significative. Pas obligatoire pour micro-corrections sans impact de reprise.
