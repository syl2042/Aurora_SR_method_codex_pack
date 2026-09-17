# context — procedure canonique SR

Charger uniquement sur le declencheur de SR_BOOTSTRAP. Les references aux autres procedures ne sont pas une liste de lecture universelle.

## Context budget gate

Avant gros lot, apres 2 lots, 20 tours utilisateur, un changement de macro-fonction ou si la session devient longue :

- mettre a jour `CURRENT_STATE.md` selon la regle plein regime si un upgrade/realignement SR, changement de version, `NEXT_SESSION_PROMPT.md`, changement structurant de backlog, lot applicatif significatif ou fin de session significative vient d'avoir lieu ;
- produire ou mettre a jour `NEXT_SESSION_PROMPT.md` ;
- recommander un handoff si le contexte devient risque.

Si `scripts/codex/context_budget_report.py` est present, l'executer avant d'enchainer un nouveau lot apres une longue passe.

Seuils recommandes pour une fenetre de contexte de 258400 tokens :

```text
green  : aucun signal hybride significatif
yellow : contexte >= 70%, ou tokens non caches >= 12k, ou cache faible sur contexte significatif, ou 2 lots traites
orange : contexte >= 82%, ou tokens non caches >= 24k, ou 20 tours utilisateur, ou 3 lots traites
red    : contexte >= 92%, ou tokens non caches >= 48k
unknown/stale/ambiguous : ne pas faire confiance au budget, creer ou rafraichir NEXT_SESSION_PROMPT avant nouveau lot long
```

Le rapport doit indiquer la session utilisee, son `cwd`, `input_tokens`, `cached_input_tokens`, `uncached_input_tokens`, `cache_ratio` et `hybrid_budget.signals`. `input_tokens` et `raw_context_percent` mesurent une pression brute de diagnostic ; ils ne declenchent pas seuls une coupure orange/rouge quand la majorite est cachee. La decision repose sur `effective_context_percent`, `uncached_input_tokens`, `cache_ratio`, les tours utilisateur et les lots traites. `uncached_input_tokens` mesure le volume nouveau non cache, et `cache_ratio` evite les coupures trop precoces sans autoriser des conversations infinies. Un rapport non fiable ne doit jamais etre assimile a `green`.

Le gate doit etre visible dans `gate_report.md`. Si aucun handoff n'est cree, indiquer pourquoi le contexte reste sain.

## Context budget gate

Declencher un handoff ou `NEXT_SESSION_PROMPT.md` si :

- plus de 2 lots ont ete executes ;
- le rapport `context_budget_report.py` est `orange` ou `red` selon le statut hybride ;
- plus de 20 tours utilisateur ont eu lieu depuis le dernier compact ;
- une nouvelle macro-fonction commence ;
- un upgrade SR ou realignement SR vient d'etre effectue ;
- une decision structurante vient d'etre prise ;
- la session dure depuis plusieurs jours ;
- l'utilisateur signale qu'il s'absente ;
- la prochaine action depend fortement de decisions anterieures.

Si aucun handoff ou `NEXT_SESSION_PROMPT.md` n'est cree apres une tache non triviale, documenter dans `gate_report.md` pourquoi le contexte reste sain.

La cloture doit aussi renseigner `conversation_transition` dans `loop_contract.json` :

- `continue_current` si le contexte est green et la suite courte ;
- `recommend_new_conversation` si le contexte est yellow, si un lot significatif vient de se terminer ou si la prochaine action est longue ;
- `stop_for_new_conversation` si le contexte hybride est orange/red ou si la reprise devient fragile.

Si `conversation_transition` vaut `recommend_new_conversation` ou `stop_for_new_conversation`, renseigner aussi `resume_protocol` :

- `required: true` ;
- `mode: strict_resume` par defaut apres un stop orange/red ;
- `next_user_prompt` avec le texte exact a copier dans la nouvelle conversation ;
- `default_on_plain_resume: strict_resume` ;
- `must_not_code_before_user_validation: true` si le contexte hybride est orange/red.

## Budget contexte par iteration

Si `scripts/codex/context_budget_report.py` existe, l'executer avant chaque reponse de cloture ou d'avancement significatif :

```bash
python3 scripts/codex/context_budget_report.py --root . --compact
```

Cette commande exploite les evenements `token_count` Codex/OpenAI de la session locale : `last_token_usage`, `total_token_usage`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`, `model_context_window` et `rate_limits` quand ils sont disponibles. Ne jamais afficher le JSON complet sauf diagnostic.

Regle de sortie :
- `green` : ne rien afficher a l'utilisateur sauf s'il demande explicitement le statut contexte ;
- `yellow` : signaler sobrement qu'une reprise sera recommandee si la prochaine tache est longue ;
- `orange`, `red`, `unknown`, `stale` ou `ambiguous` : creer ou mettre a jour le `NEXT_SESSION_PROMPT.md` du lot courant avant de conclure et donner un prompt court avec le chemin explicite.

Prompt court recommande quand le chemin est connu :

```text
Reprise SR stricte. Projet : <chemin absolu du projet>. Lis docs/codex/tasks/YYYY-MM-DD_slug/NEXT_SESSION_PROMPT.md et les contrats associes. Resume l'etat, ne code pas avant validation.
```


## Continuite conservee

Le statut hybride tient compte de `effective_context_percent`, `uncached_input_tokens`, `cache_ratio`, tours utilisateur et lots traites ; ne pas couper une conversation uniquement sur `input_total` ou `raw_context_percent` quand la majorite est cachee. `raw_context_percent` est un signal de diagnostic, pas un seuil de coupure autonome. Un statut `unknown`, `stale` ou `ambiguous` ne doit jamais etre traite comme `green`.

## Continuite conservee

`NEXT_SESSION_PROMPT.md` n'est pas systematique. Il est obligatoire si :
- contexte `orange` ou `red` ;
- contexte `stale` ou `ambiguous` ;
- fin de batch multi-lots ou apres 2-3 lots dans la session ;
- pause longue ou arret annonce par l'utilisateur ;
- changement de macro-fonction ;
- upgrade SR ou realignement SR ;
- decision structurante importante ;
- prochain lot fortement dependant des decisions courantes.

## Continuite conservee

Il est recommande si le contexte est `yellow` et que la prochaine tache est longue. Il n'est pas necessaire pour une question simple, une micro-correction ou une session courte en contexte `green`.

## Continuite conservee

En cloture d'une tache non triviale, la decision doit etre visible dans `loop_contract.json` :

## Continuite conservee

- `continue_current` : conversation saine, prochain lot court ou contexte green ;
- `recommend_new_conversation` : contexte yellow, fin de lot significatif, pause probable ou prochaine action longue ;
- `stop_for_new_conversation` : contexte orange/red, changement de macro-fonction risque, decisions nombreuses ou reprise fragile.

## Continuite conservee

Si la decision est `recommend_new_conversation` ou `stop_for_new_conversation`, creer ou mettre a jour `NEXT_SESSION_PROMPT.md` et indiquer son chemin.
Le `loop_contract.json` doit aussi renseigner `resume_protocol` avec le prompt utilisateur exact a copier dans la prochaine conversation.

## Regle distribuee par ancien installateur

- Context budget gate : executer `python3 scripts/codex/context_budget_report.py --root .` si disponible avant nouveau lot long; creer `NEXT_SESSION_PROMPT.md` au statut orange/rouge, apres 2 lots ou 20 tours utilisateur; declarer si la prochaine action continue ici ou exige une nouvelle conversation.
