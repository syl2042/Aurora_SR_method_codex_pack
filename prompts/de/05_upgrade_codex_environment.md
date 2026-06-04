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
4. Upgrade-Plan erklären und vor Mutation explizite Validierung abwarten.
5. Upgrade erst nach Validierung mit dem Installer anwenden.
6. Audit- und Validierungsskripte ausführen.
7. Source-Commit, aktualisierte Dateien, erhaltene Dateien, Backups, Warnungen und nächste Schritte berichten.

Ändere keinen Anwendungscode, keine Abhängigkeiten, Migrationen oder Secrets.
