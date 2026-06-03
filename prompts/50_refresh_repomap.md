# Rafraichir le RepoMap

Lire REPO_MAP_POLICY, identifier le mode connaissance (`core` ou `nexus_kg`), lancer generate_repo_map.py --write, lire le diff, mettre a jour CODEBASE_MAP.md seulement si utile, ne pas modifier le code applicatif.

Si `nexus_kg` est actif, verifier aussi si le KG doit etre rafraichi par l'outil Nexus disponible. Le RepoMap reste obligatoire et le KG ne remplace pas la lecture du code reel.
