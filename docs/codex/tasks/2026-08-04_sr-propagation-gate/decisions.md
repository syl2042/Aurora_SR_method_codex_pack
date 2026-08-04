# Decisions - SR propagation gate

- Ajouter un gate officiel nomme `Propagation Gate`, avec alias methodologique `Reference Integrity Gate`.
- Ne pas creer une nouvelle boucle SR : integrer le gate dans la boucle de lot existante, en preflight avant mutation et postcheck apres patch.
- Rendre le gate strict pour les nouveaux contrats/templates, mais compatible legacy pour les anciennes task memories via warnings d'audit.
- Version cible : SR Method 3.3.0.
