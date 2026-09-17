# SR-Zustand nach einem Upgrade neu ausrichten

## SR 4.0.0 — veroeffentlichte Version

Schreibgeschuetzt beginnen. Wiedereroeffnungen und Memory-Aktualisierungen bleiben Vorschlaege bis zur exakten Freigabe `je valide` des Realignment-Umfangs; danach nur diesen Umfang anwenden. Installationsfreigabe autorisiert keine Anwendungskorrektur.

Keinen Anwendungscode aendern.

Ziel: SR-Memory mit Code und vollstaendig validiertem Scope abgleichen, bevor Entwicklung fortgesetzt wird.

`AGENTS.md`, danach `docs/codex/SR_BOOTSTRAP.md` lesen. `python3 scripts/codex/find_next_session_prompt.py --root . --json` ausfuehren: `selected` verwenden; bei `ambiguous` nach dem Pfad fragen und `--prompt` verwenden. `latest` nie allein nach Datum auswaehlen. Den ausgewaehlten `NEXT_SESSION_PROMPT.md` und zugehoerige `sr_contract.json`/`loop_contract.json` mit allen geerbten offenen `validated_requests` lesen. Ohne Handoff offene Lots inventarisieren und Scope vorschlagen. Fuer dieses Realignment auch `docs/CURRENT_STATE.md` und Lot/Pass-Register lesen, um globale Abweichungen zu erkennen. Anschliessend detaillierte Memories, Verfahren, RepoMap/KG und Code/Tests nur fuer betroffene Lots laden; bei Nachweisbedarf, Gate oder Abhaengigkeit erweitern.

1. Pack-, Release-Dokumentations-, Post-Install-, Projekt- und Task-Contract-Audits ausfuehren.
2. Alle Eintraege in `validated_requests` mit stabiler ID, urspruenglichem Lot/Pass, `implementation_status`, `evidence_status`, fehlenden Tests und Feedback-Historie erhalten.
3. Das urspruengliche Lot wieder oeffnen, wenn eine validierte Anforderung fehlt, partiell, defekt, regressiv oder durch Benutzerfeedback widerlegt ist.
4. Die gesamte offene Checkliste von Lot und Pass laden; nicht nur den letzten Fehler isolieren.
5. Strikte Status anwenden: `done` nur bei kompletter Implementierung und Nachweisen; `user_testing` nur bei technisch kompletter Implementierung und fehlendem realen E2E/Abnahme; `repair` bei fehlender, partieller, defekter oder fehlgeschlagener Implementierung; `blocked` nur bei real nicht verfuegbarer Autoritaet, Zugriff, Secret, Entscheidung oder externer Aenderung.
6. Code-, Build-, Runtime-, E2E- und Deployment-Nachweise getrennt halten, aber derselben persistenten Anforderung zuordnen.
7. `CURRENT_STATE.md` und Task Memory erst nach belastbarem Nachweis aktualisieren.

Bericht mit `Benutzeranforderung | Status | Nachweis | Restarbeit` beginnen, wiedereroeffnete Lots und fehlende Nachweise nennen und einen konsolidierten Repair-Scope vorschlagen. Neues Lot nur fuer wirklich neuen Scope.

Stoppen und vor Mutation exakte menschliche Validierung verlangen.

Pfade: Neuinstallation `00 -> 06`; bestehende Installation `05 -> 06 -> 07`. Prompt `06` prueft nur; `07` schlaegt Realignment vor und wartet vor Memory-Aenderungen auf `je valide`. Beide Pfade autorisieren keine Anwendungsentwicklung.
