# Eine gesteuerte SR-Sitzung starten

Nicht coden.

Ziel: Den gesamten validierten Scope rekonstruieren und vor jeder Mutation die naechste kohaerente Aktion vorschlagen.

1. `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md` und, falls vorhanden, `docs/CURRENT_STATE.md` lesen.
2. `python3 scripts/codex/find_next_session_prompt.py --root . --json` ausfuehren und den letzten `NEXT_SESSION_PROMPT.md` lesen.
3. Den verknuepften `sr_contract.json` (SR Contract 3.1.0 oder Legacy 3.0.0), `loop_contract.json`, Task Memory, Lots und Passes lesen.
4. Alle geerbten offenen Eintraege aus `validated_requests` laden; nicht nur das letzte Benutzerfeedback fortsetzen.
5. Erledigte, partielle, fehlende, defekte, blockierte und nur auf Nachweis wartende Anforderungen trennen.
6. Status strikt anwenden: unvollstaendige Implementierung bedeutet `repair`; `user_testing` setzt technisch vollstaendige Implementierung voraus, nur echtes E2E oder menschliche Abnahme darf fehlen.
7. Feedback zu einer bestehenden Anforderung oeffnet standardmaessig das urspruengliche Lot mit kompletter Checkliste. Kein neues Mikro-Lot erstellen.
8. Verfuegbare Contract- und Context-Budget-Pruefungen ohne Projektmutation ausfuehren.

SR-Version, verwendete Memory, validierte Anforderungen, Implementierungs-/Nachweisstatus, wiedereroeffnete Lots, Blocker, fehlende Nachweise, naechsten kohaerenten Scope und die genaue menschliche Validierung berichten.

Stoppen und auf Validierung warten.
