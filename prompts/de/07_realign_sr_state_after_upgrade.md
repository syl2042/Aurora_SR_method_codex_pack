# SR-Zustand nach einem Upgrade neu ausrichten

Keinen Anwendungscode aendern.

Ziel: SR-Memory mit Code und vollstaendig validiertem Scope abgleichen, bevor Entwicklung fortgesetzt wird.

`AGENTS.md`, `docs/CURRENT_STATE.md`, SR-Methode, `SR_LOTS.yaml`, `SR_PASSES.yaml`, letzten `NEXT_SESSION_PROMPT.md`, aktive Task Memories, `sr_contract.json`, `loop_contract.json` und relevante Code/Tests lesen.

1. Pack-, Release-Dokumentations-, Post-Install-, Projekt- und Task-Contract-Audits ausfuehren.
2. Alle Eintraege in `validated_requests` mit stabiler ID, urspruenglichem Lot/Pass, `implementation_status`, `evidence_status`, fehlenden Tests und Feedback-Historie erhalten.
3. Das urspruengliche Lot wieder oeffnen, wenn eine validierte Anforderung fehlt, partiell, defekt, regressiv oder durch Benutzerfeedback widerlegt ist.
4. Die gesamte offene Checkliste von Lot und Pass laden; nicht nur den letzten Fehler isolieren.
5. Strikte Status anwenden: `done` nur bei kompletter Implementierung und Nachweisen; `user_testing` nur bei technisch kompletter Implementierung und fehlendem realen E2E/Abnahme; `repair` bei fehlender, partieller, defekter oder fehlgeschlagener Implementierung; `blocked` nur bei real nicht verfuegbarer Autoritaet, Zugriff, Secret, Entscheidung oder externer Aenderung.
6. Code-, Build-, Runtime-, E2E- und Deployment-Nachweise getrennt halten, aber derselben persistenten Anforderung zuordnen.
7. `CURRENT_STATE.md` und Task Memory erst nach belastbarem Nachweis aktualisieren.

Bericht mit `Benutzeranforderung | Status | Nachweis | Restarbeit` beginnen, wiedereroeffnete Lots und fehlende Nachweise nennen und einen konsolidierten Repair-Scope vorschlagen. Neues Lot nur fuer wirklich neuen Scope.

Stoppen und vor Mutation exakte menschliche Validierung verlangen.
