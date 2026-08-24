# SR Passes aus bestehenden Losen definieren

Du arbeitest in einem Repository, das bereits mit der SR Method ausgestattet ist.

Ziel: `docs/codex/SR_PASSES.yaml` aus `docs/codex/SR_LOTS.yaml` vorschlagen oder aktualisieren, ohne Anwendungscode zu aendern.

`repair`/`reopened` Lose priorisieren, alle offenen `validated_request_ids` behalten und Reparaturen desselben Produktumfangs in einem kohaerenten Pass konsolidieren.

Regeln:

- Keinen Anwendungscode aendern.
- Keinen Losstatus ohne Belege und Validierung aendern.
- Keinen Pass ohne explizite Nutzer-Validierung als `validated` markieren.
- Ein Pass gruppiert Lose; er ersetzt niemals Kriterien oder Gates der Lose.

Zu lesende Quellen:

1. `AGENTS.md`
2. `docs/codex/SR_HARNESS_METHOD.md`
3. `docs/codex/LOT_EXECUTION_METHOD.md`
4. `docs/CURRENT_STATE.md`
5. `docs/codex/SR_LOTS.yaml`
6. `docs/codex/SR_PASSES.yaml`, falls vorhanden
7. `docs/codex/CODEBASE_MAP.md`

Methode:

1. `SR_LOTS.yaml` validieren.
2. Lose nach Status und Abhaengigkeiten klassifizieren.
3. Lot Design Evidence Gate pruefen: jedes `planned`, `validated`, `in_progress`, `repair` oder `reopened` Los ohne `design_evidence.status: pass` oder begruendetes `not_applicable` aus ausfuehrbaren Passes ausschliessen. Ein `proposed` Los darf explorativ bleiben.
4. Den Graphen `depends_on`, `blocked_by`, `impacts`, `impacted_by` bauen.
5. Passes mit Reihenfolge, Rationale, Preflight, menschlichen Validierungen, Migrationen/externen Aktionen, gemeinsamen Quellen, gruppiertem E2E und Stop Conditions vorschlagen.
6. `SR_PASSES.yaml` nur nach Validierung erstellen oder aktualisieren, wenn das Projekt strikte Validierung verlangt.
7. Validieren mit `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml`.

Erwartete Ausgabe:

- vorgeschlagene Passes;
- ausgeschlossene Lose mit Grund;
- wegen fehlendem oder unvollstaendigem Lot Design Evidence Gate ausgeschlossene Lose;
- blockierende Fragen;
- Preflight pro Pass;
- empfohlenes gruppiertes E2E;
- geaenderte SR-Dateien;
- Validierungsergebnis;
- naechster empfohlener Pass.
