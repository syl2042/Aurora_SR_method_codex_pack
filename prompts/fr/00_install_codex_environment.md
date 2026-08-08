# Installer la SR Method dans un projet cible

Tu travailles dans un repository logiciel qui doit recevoir Aurora SR Method.

Objectif : installer la SR Method sans modifier le code applicatif, les migrations, les dependances, les secrets ou les regles metier.

Utilise le package source officiel :

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Instructions :

1. Identifier ou cloner une copie locale du package officiel.
2. Inspecter le repository cible avant toute modification.
3. Expliquer le perimetre d'installation et attendre la validation explicite de l'utilisateur si une mutation est requise.
4. Lancer l'installateur avec le profil `default` apres validation.
5. Lancer les scripts de verification apres installation, dont `validate_pass_contract.py` pour `SR_PASSES.yaml`.
6. Verifier que `SR_PASSES.yaml`, `scripts/codex/build_pass_runtime_goal.py` et `docs/codex/tasks/_TEMPLATE/pass_runtime_goal.md` sont installes.
7. Pour un projet vierge, ne pas generer de goal immediatement : recommander d'abord la definition des lots avec `prompts/fr/09_define_sr_lots_from_scope.md`, puis `prompts/fr/08_define_sr_passes_from_lots.md`, puis la generation d'un Pass Runtime Goal uniquement pour une passe `validated` ou `in_progress`.
8. Expliquer au futur Codex que le Pass Runtime Goal est derive : `SR_PASSES.yaml`, `SR_LOTS.yaml` et `sr_contract.json` restent source de verite ; `/goal` sert seulement a aller au bout d'une passe validee.
9. Verifier et rappeler le Goal Length Gate : `max_goal_command_chars: 1000`, `hard_limit: 4000`.
10. Rapporter les fichiers ajoutes, les controles executes, les warnings et les prochaines etapes.

Ne modifie pas le code applicatif. Ne cree pas de migration. Ne touche pas aux secrets. N'invente pas de regle projet.
