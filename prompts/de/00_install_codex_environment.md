# SR 4.0.0 in ein neues Zielprojekt installieren

## SR 4.0.0 — veroeffentlichte Version

Zielquelle: `SR_PACK_SOURCE` ausdruecklich auswaehlen, entweder eine identifizierte veroeffentlichte Version oder den freigegebenen lokalen SR-4.0.0-Kandidaten. `core/SR_PACK_VERSION.json` (`version`, `release_status`) lesen; `source_commit`, Git-Zustand und bei lokalen Aenderungen einen Inhaltsfingerabdruck einschliesslich verwendeter unversionierter Quelldateien dokumentieren. Einen `unreleased`-Kandidaten nicht als Release ausgeben. Den Kandidaten nicht durch einen Clone der neuesten veroeffentlichten Version ersetzen; fehlt die angeforderte Quelle, vor der Installation stoppen und klaeren.

Fuer dieses SR-4.0.0-Ziel muss die Quelle `version: 4.0.0` angeben. Falls kein Release 4.0.0 veroeffentlicht ist, nur den freigegebenen lokalen Kandidaten verwenden oder sein Fehlen melden; niemals stillschweigend eine andere Version installieren.

Vor Freigabe mit dem folgenden Befehl eine Vorschau erstellen; nach `je valide` nur den passenden Modus waehlen. `--plan-out` schreibt einen lokalen Plan und erfordert Freigabe; `--apply-plan` lehnt veraltete Diagnosen ab. `--restore` ist ein separater Vorgang mit dem exakten Transaktionsjournal und verweigert spaetere Aenderungen. Keine Datei zur Konfliktumgehung loeschen.

Gespeicherte Plaene enthalten Dateiinhalte: lokal aufbewahren. `SR_TARGET` auf den Pfad des Zielrepositorys setzen.

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Überprüfbares Ziel: SR Pack 4.0.0 mit `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 und `SR_PASSES` 0.2 installieren, prüfen und vor jeder Anwendungsentwicklung stoppen.

Installiere `SR_PASSES.yaml` mit `passes: []`. Dieses leere Register ist gueltig: Eine Neuinstallation darf keine Produkt-Pass erfinden. Prompt `08` schlaegt Passes erst nach Lektuere der Lose und menschlicher Freigabe vor.

Verwende nur `https://github.com/syl2042/Aurora_SR_method_codex_pack`.

Strikte Regeln:

- Ändere keinen Anwendungscode, keine Migrationen, Abhängigkeiten, Secrets, Konfiguration oder Geschäftsregeln.
- Prüfe zuerst das Zielrepository und das nächste `AGENTS.md`.
- Wenn `docs/codex/SR_PACK_VERSION.json`, `docs/codex/SR_METHOD.md` oder `docs/codex/SR_LOTS.yaml` existiert, ist es keine Neuinstallation. Stoppe und verwende `05_upgrade_codex_environment.md`.
- Berichte vor jeder Mutation die neuen, vorhandenen und zu erhaltenden Dateien sowie die geplanten Prüfungen; warte auf die erforderliche menschliche Freigabe.
- Erfinde keine `validated_requests`, validierten Lose oder ausführbaren Passes. Templates sind kein validierter Produktumfang.
- Verwende `--write` nie für ein bestehendes SR-Projekt; verwende `--upgrade` erst nach einem Audit pro Projekt.

Nach Freigabe:

1. Verifizierten lokalen Clone und Source-Commit festhalten; Ziel als `fresh_install` klassifizieren.
2. Installer mit `--profile default --write` ausführen.
3. Version, Lots/Passes, Task-Templates, Validatoren und Prompts `01`, `05`, `06`, `07`, `08`, `09` prüfen.
4. Bestätigen, dass `sr_contract.json` `implementation_status` und `evidence_status` trennt und granulare `validated_requests` sowie ein abgeleitetes Completion Gate enthält.
5. `CHANGELOG.md`, lokalisierte oeffentliche Prompts sowie `audit_codex_pack.py`, `sr_post_install_check.py`, `validate_release_docs.py` und Lot-, Pass-, Loop- und SR-Validatoren pruefen.
6. Kein `/goal` erzeugen. Zuerst `09_define_sr_lots_from_scope.md`, dann `08_define_sr_passes_from_lots.md` empfehlen.
7. Klassifikation, Version, Commit, Dateien, Prüfungen, Warnungen und unveränderten Anwendungscode berichten.

Pflichtende: Die Methodeninstallation validiert keinen Produktumfang.

Pfade: Neuinstallation `00 -> 06`; bestehende Installation `05 -> 06 -> 07`. Prompt `06` prueft nur; `07` schlaegt Realignment vor und wartet vor Memory-Aenderungen auf `je valide`. Beide Pfade autorisieren keine Anwendungsentwicklung.
