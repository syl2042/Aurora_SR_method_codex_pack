# Gesteuerte SR-Sitzung starten

Du arbeitest in einem Repository mit installierter Aurora SR Method.

Ziel: Projekt sauber aufnehmen, bevor Entwicklungsarbeit beginnt.

Anweisungen:

1. `AGENTS.md` lesen.
2. `docs/codex/SR_BOOTSTRAP.md` lesen.
3. `docs/CURRENT_STATE.md` lesen, falls vorhanden.
4. `python3 scripts/codex/find_next_session_prompt.py --root . --json` ausführen, falls verfügbar.
5. Falls `NEXT_SESSION_PROMPT.md` gefunden wird, vor jeder Arbeitsplanung lesen.
6. SR-Version mit `python3 scripts/codex/audit_codex_pack.py --root . --json` prüfen, falls verfügbar.
7. Offene Lots, aktive Entscheidungen, Blocker und empfohlene nächste Aktion zusammenfassen.

Vor Abschluss dieses Bootstraps nicht coden.
