# Projekt auf die neueste SR Method aktualisieren

Du arbeitest in einem Repository, das bereits eine ältere Aurora SR Method Version enthält.

Ziel: SR Pack auditieren und aktualisieren, ohne Anwendungscode zu ändern oder projektspezifische Anpassungen zu überschreiben.

Nutze das offizielle Source-Paket:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Anweisungen:

1. Installierte SR-Version erkennen.
2. Offizielles Source-Paket prüfen oder klonen.
3. Projektdateien identifizieren, die erhalten bleiben müssen: `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `docs/codex/tasks/`, Projektskills und lokale Entscheidungen.
4. `SR_LOTS.yaml` erhalten und `SR_PASSES.yaml` additiv hinzufuegen, wenn es fehlt, ohne alte Lose oder Task Memories automatisch zu konvertieren.
5. Alte Lose nicht massenhaft zu `design_evidence` konvertieren; Lot Design Evidence Gate nur fuer nach dem Upgrade erstellte, promotete oder wiederaufgenommene Lose hinzufuegen.
6. Upgrade-Plan erklären und vor Mutation explizite Validierung abwarten.
7. Upgrade erst nach Validierung mit dem Installer anwenden.
8. Audit- und Validierungsskripte ausführen, einschliesslich `validate_pass_contract.py`, wenn `SR_PASSES.yaml` existiert.
9. Source-Commit, aktualisierte Dateien, erhaltene Dateien, Backups, Warnungen, Status von `SR_PASSES.yaml` und nächste Schritte berichten.
10. `prompts/de/09_define_sr_lots_from_scope.md` empfehlen, um Lose vor der Ausfuehrung mit Lot Design Evidence Gate zu erstellen oder zu promoten.
11. `prompts/de/08_define_sr_passes_from_lots.md` empfehlen, wenn das Projekt mehrere Lose und keine validen Passes hat.

Ändere keinen Anwendungscode, keine Abhängigkeiten, Migrationen oder Secrets.
