# DESIGN.md — Aurora SR Cockpit

## Direction
Cockpit operationnel personnel pour supervision multi-projets SR.

- UI dense, moderne et rapide.
- Priorite a la lecture immediate : projets actifs, version SR, Codex ouvert, Git dirty, lots et gates.
- Palette claire, sobre, avec statuts lisibles et non decoratifs.
- Navigation par tableau principal + detail projet lateral.

## UX principles
Chaque ecran doit dire : que faire, quelle information critique, quelle preuve/source, quelle action attendue.

- Le premier ecran est l'outil, pas une landing page.
- Les filtres rapides doivent rester visibles : toutes, SR installee, Codex ouvert, a mettre a jour, Git dirty, reopened, user testing, bloques.
- Les descriptions de lots restent limitees a 3 ou 4 lignes.
- Les badges de statut doivent etre scannables sans ouvrir le detail.

## Tech UI
React/Vite, CSS local, lucide-react pour les icones. Pas de librairie UI lourde au MVP.

## Interdictions
Pas de dashboard decoratif, pas de score opaque, pas de conclusion engageante sans preuve ou validation humaine.
