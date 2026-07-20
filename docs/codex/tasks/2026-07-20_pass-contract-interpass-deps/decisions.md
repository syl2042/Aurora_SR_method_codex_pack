# Decisions

- Conserver la signature de `validate_pass()` compatible en ajoutant un parametre optionnel de contexte global.
- Refuser explicitement tout lot reference dans plusieurs passes, faute de mecanisme officiel documente.
- Autoriser une dependance inter-passes anterieure non terminee seulement quand la passe courante est `proposed` ou `planned`.
- Exiger `done` ou `user_testing` pour une dependance anterieure des passes `validated` et `in_progress`.
