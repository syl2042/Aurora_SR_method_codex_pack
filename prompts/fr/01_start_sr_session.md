# Demarrer une session SR gouvernee

Ne code rien.

Objectif : reconstruire tout le perimetre valide et proposer la prochaine action coherente avant toute mutation.

1. Lire `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md` et `docs/CURRENT_STATE.md` lorsqu'ils existent.
2. Executer `python3 scripts/codex/find_next_session_prompt.py --root . --json` et lire le dernier `NEXT_SESSION_PROMPT.md` detecte.
3. Lire le `sr_contract.json` lie (SR Contract 3.1.0 ou legacy 3.0.0), le `loop_contract.json`, la task memory, les lots et les passes utiles.
4. Recharger toutes les entrees ouvertes heritees de `validated_requests` ; ne jamais reprendre uniquement depuis le dernier retour utilisateur.
5. Separer les exigences faites, partielles, non faites, defectueuses, bloquees ou en attente de preuve.
6. Appliquer les statuts stricts : implementation incomplete signifie `repair` ; `user_testing` exige une implementation technique complete et seulement un E2E reel ou une acceptation humaine restante.
7. Si le retour concerne une exigence existante, rouvrir par defaut le lot d'origine et presenter sa checklist consolidee. Ne pas creer de micro-lot.
8. Executer les validateurs de contrats et le controle de budget contexte disponibles sans modifier le projet.

Rapporter la version SR, la memoire utilisee, les demandes validees, leurs etats implementation/preuve, les lots rouverts, les blocages, les preuves manquantes, le prochain bloc coherent et la validation humaine exacte requise.

Stopper et attendre validation.
