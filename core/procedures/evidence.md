# evidence — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Modes de connaissance codebase

SR 2.3 distingue deux modes.

## Evidence gate

Avant un plan, une faisabilite, une architecture ou un bugfix, Codex doit verifier les sources necessaires :

- RepoMap ;
- Nexus KG si le mode `nexus_kg` est actif ;
- fichiers candidats ;
- routes/API/schemas ;
- specs pertinentes ;
- logs si bug.

Ordre attendu :

```text
RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs
```

La reponse doit distinguer :

```text
Verifie
Hypotheses restantes
Questions bloquantes
```

Si la question porte sur l'existence d'un menu, endpoint, composant, schema, route, modele, migration, configuration ou comportement deja codable, Codex doit lire le code ou les fichiers de reference avant de recommander. Repondre au conditionnel sans verification locale est un gate rouge si les sources sont accessibles.

## Knowledge gate

Le knowledge gate precise comment Codex a construit sa carte du changement.

En mode `core` :

- lire `CODEBASE_MAP.md` avant toute tache multi-fichiers ou reprise ;
- consulter `CODEBASE_MAP.generated.md` si la carte courte ne suffit pas ;
- documenter les fichiers candidats puis les fichiers vraiment lus.

En mode `nexus_kg` :

- interroger Nexus KG avant de choisir les fichiers candidats ;
- verifier la fraicheur du KG si l'outil le permet ;
- produire ou demander un context pack court ;
- apres le lot, indiquer si le KG doit etre mis a jour.

## 2b. Knowledge gate

Construire la carte du changement :

```text
RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs
```

En mode `core`, RepoMap suffit pour orienter.

En mode `nexus_kg`, interroger le KG avant de figer le scope et verifier la fraicheur si l'outil existe.

## 3. Evidence gate

Avant de planifier ou coder, noter :

- fichiers lus ;
- faits verifies ;
- hypotheses restantes ;
- questions bloquantes.

Si la demande implique une supposition non verifiee et que les fichiers peuvent trancher, lire les fichiers avant de repondre.

Si l'evidence gate n'est pas fait, ne pas donner de plan engageant. Repondre d'abord par ce qui doit etre verifie ou effectuer la verification locale.

## Knowledge mode

Mode par defaut sans Nexus : `SR Core = RepoMap only`.
Mode avec Nexus : `SR Nexus = RepoMap + Nexus KG`.
RepoMap est obligatoire dans les deux modes. Nexus KG oriente et construit le context pack quand disponible, mais le code reel et les tests restent la source finale.

## Knowledge modes

Mode `core` : RepoMap obligatoire, puis lecture ciblee du code reel.

Mode `nexus_kg` : RepoMap + Nexus KG quand disponible, puis lecture ciblee du code reel.

Le KG et RepoMap orientent. Les sources finales restent le code, les tests et les logs.


## Regle distribuee par ancien installateur

- Evidence gate obligatoire avant recommandation : lire les fichiers verifiables quand ils peuvent trancher.

## Regle distribuee par ancien installateur

- Pour une UI/UX significative, utiliser `aurora-ui-visual-qa`, appliquer le Design Gate, le UI Test Readiness Gate et le UI Visual Evidence Gate, puis executer `node scripts/codex/sr_ui_verify.mjs` sur les routes et viewports requis.

## Regle distribuee par ancien installateur

- Lot Design Evidence Gate : avant de creer ou promouvoir un lot en `planned`, `validated`, `in_progress`, `repair` ou `reopened`, remplir `design_evidence` avec fichiers candidats, fichiers reellement lus, hypotheses et questions; sans preuve suffisante, garder le lot en `proposed`.

## Regle distribuee par ancien installateur

- Knowledge gate : utiliser `RepoMap/KG -> fichiers candidats -> lecture code reel -> tests/logs`; sans Nexus, `SR Core = RepoMap only`; avec Nexus, `SR Nexus = RepoMap + Nexus KG`.
