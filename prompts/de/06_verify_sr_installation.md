# SR Method Installation prüfen

Du arbeitest in einem Repository mit installierter Aurora SR Method.

Ziel: Installation oder Upgrade prüfen, bevor die Entwicklung fortgesetzt wird.

Anweisungen:

1. `python3 scripts/codex/verify_codex_pack.py` ausführen.
2. `python3 scripts/codex/audit_codex_pack.py --root . --json` ausführen.
3. `python3 scripts/codex/sr_post_install_check.py --root . --json` ausführen, falls verfügbar.
4. Lot-, Loop- und SR-Contracts validieren, wenn Skripte vorhanden sind.
5. Restliche Warnungen klassifizieren: akzeptabel, zu dokumentieren, mit Validierung zu korrigieren oder blockierend.
6. Version, Prüfungen, Fehler, Warnungen und nächste empfohlene Aktion berichten.

Dies ist keine Anwendungsentwicklungsaufgabe.
