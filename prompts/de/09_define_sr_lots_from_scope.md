# SR-Lose aus Scope oder Inbox definieren

Ziel: Einen Rahmen, eine Nutzeranfrage oder `docs/codex/SR_INBOX.yaml` in explizite SR-Lose in `docs/codex/SR_LOTS.yaml` umwandeln, ohne Anwendungscode zu aendern.

Regeln:

- Keinen Anwendungscode aendern.
- Kein `planned`, `validated`, `in_progress` oder `reopened` Los ohne Lot Design Evidence Gate erstellen.
- Ein `proposed` Los darf explorativ bleiben.
- Ein Los niemals ohne explizite Nutzer-Validierung als `validated` markieren.

Methode:

1. `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md`, `docs/codex/SR_HARNESS_METHOD.md`, `docs/codex/LOT_EXECUTION_METHOD.md`, `docs/CURRENT_STATE.md`, `docs/codex/SR_INBOX.yaml`, `docs/codex/SR_LOTS.yaml` und `docs/codex/CODEBASE_MAP.md` lesen, wenn vorhanden.
2. Kandidaten mit `RepoMap/KG -> Kandidatendateien -> echter Code -> Tests/Logs` identifizieren.
3. `design_evidence` fuer jedes Kandidatenlos ausfuellen.
4. Jedes Los mit noch ungepruefter verifizierbarer Annahme in `proposed` halten.
5. Lose vor Ausfuehrung zur Validierung vorschlagen.
6. `SR_LOTS.yaml` mit `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` validieren.
7. Danach `docs/codex/prompts/08_define_sr_passes_from_lots.md` empfehlen, wenn mehrere Lose ausfuehrbar oder fast ausfuehrbar sind.

Erwartete Ausgabe: erstellte oder geaenderte Lose, Status des Lot Design Evidence Gate, gelesene Dateien, verbleibende Annahmen, blockierende Fragen, Validierung von `SR_LOTS.yaml`, naechster Schritt.
