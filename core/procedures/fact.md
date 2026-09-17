# fact — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Fact gate

Le Fact Gate s'applique a toute reponse non triviale, meme hors patch et hors lot.

But : empecher une conclusion factuelle non prouvee quand les sources peuvent trancher.

Classification :

- `opinion/methode` : conseil general, preference ou explication methodologique ;
- `fait_verifiable` : fait sur un repo, produit, code, API, migration, flux UI, donnee, configuration, etat projet ou comportement existant ;
- `hypothese_non_verifiee` : piste utile non encore prouvee.

Regles :

- un `fait_verifiable` doit etre appuye par une source locale ou officielle lue avant la reponse ;
- si la source est accessible mais non lue, le gate est rouge et Codex doit repondre `Fact Gate non satisfait` avec la source a verifier ;
- si la verification n'est pas possible ou serait disproportionnee, la conclusion reste interdite : Codex peut seulement formuler une hypothese non verifiee avec la verification minimale ;
- les mots de probabilite ne doivent jamais remplacer une preuve disponible.

## 3b. Fact gate

Avant toute conclusion factuelle, y compris hors patch, classer les elements de reponse :

- `opinion/methode` : conseil general ou preference ; pas de preuve locale obligatoire ;
- `fait_verifiable` : affirmation sur un repo, produit, code, API, migration, flux UI, donnee, configuration ou comportement existant ;
- `hypothese_non_verifiee` : piste utile non encore prouvee.

Pour tout `fait_verifiable`, verifier la source disponible avant de repondre :

- code reel, tests, logs ou diff pour un comportement applicatif ;
- fichiers SR, task memory, contrats, backlog ou `CURRENT_STATE.md` pour l'etat methode/projet ;
- documentation officielle ou source primaire pour une API externe ;
- source metier documentee ou validation humaine pour une regle metier.

Si la source est accessible mais non lue, le gate est rouge : ne pas conclure, annoncer `Fact Gate non satisfait` et indiquer la source a verifier.

Si la verification est impossible ou disproportionnee, la reponse doit rester explicitement une `hypothese_non_verifiee` et fournir la verification minimale. Les formulations probabilistes ne remplacent pas une preuve.

## Fact Gate

Avant toute reponse non triviale, appliquer un gate deterministe sur les faits utilises dans la reponse.

Classification obligatoire :

- `opinion/methode` : conseil general, preference ou explication methodologique ; source locale non obligatoire ;
- `fait_verifiable` : affirmation sur un repo, produit, code, API, migration, flux UI, donnee, configuration, etat projet ou comportement existant ;
- `hypothese_non_verifiee` : piste utile mais non encore prouvee.

Regle :

- si une source locale ou officielle peut trancher un `fait_verifiable`, la lire avant de repondre ;
- si la source est accessible mais non lue, ne pas conclure et repondre `Fact Gate non satisfait : je dois verifier <source> avant de conclure.` ;
- si la verification est impossible ou disproportionnee, garder le statut `hypothese_non_verifiee` et indiquer la verification minimale ;
- les termes probabilistes ne remplacent jamais une preuve quand le repo, les logs, les fichiers SR ou la documentation officielle peuvent trancher.

Sources attendues :

- comportement applicatif : code reel, tests, logs, diff ;
- methode SR ou etat projet : fichiers SR, task memory, contrats, backlog, `CURRENT_STATE.md` ;
- API ou outil externe : documentation officielle ou source primaire ;
- donnees metier : source metier documentee ou validation humaine.


## Regle distribuee par ancien installateur

- Fact Gate obligatoire : avant toute conclusion factuelle non triviale, lire la source locale ou officielle qui peut trancher ; sinon marquer explicitement l'hypothese et la verification minimale restante.
