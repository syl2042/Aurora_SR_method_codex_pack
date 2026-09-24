# Candidat SR 4.1.0 — promu

Statut : promu en release officielle `v4.1.0` le 2026-09-24.

Ce candidat reduit le contexte permanent, remplace l'accumulation dans `AGENTS.md` par une reconciliation, retire le workflow TDD et les skills purement procedurales, borne les appels MCP, separe les dimensions de tokens et rend l'upgrade independant de la version precedente.

La qualification couvre une installation neuve, plusieurs formes d'installations historiques, la preservation des personnalisations, la suppression sure des artefacts geres obsoletes, l'idempotence et la restauration transactionnelle.

Tous les prompts distribues sont alignes : installation et reprise, decoupage des lots et passes, conception des agents runtime, generation et revue des skills. Les anciens champs restent lisibles uniquement pour compatibilite; ils ne recreent pas de gates autonomes.

Ce document conserve la trace du candidat qualifie avant sa promotion. Aucun deploiement applicatif ou mise a jour de serveur n'est inclus dans la publication du pack.
