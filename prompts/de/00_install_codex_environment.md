# SR 3.7 in ein neues Zielprojekt installieren

Überprüfbares Ziel: SR Pack 3.7.0 mit `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 und `SR_PASSES` 0.2 installieren, prüfen und vor jeder Anwendungsentwicklung stoppen.

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
