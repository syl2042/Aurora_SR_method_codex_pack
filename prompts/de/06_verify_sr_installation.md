# Eine SR-Method-Installation pruefen

Keine Dateien aendern.

Ziel: Fuer jedes Repository nachweisen, dass Installation oder Upgrade vollstaendig, kohaerent und vor weiterer Anwendungsentwicklung nutzbar ist.

1. Reale Marker in `AGENTS.md`, `docs/codex/SR_PACK_VERSION.json`, Methode, Contracts, Lots, Passes und Task Memories lesen. Keine Version von einem Nachbarordner ableiten.
2. `python3 scripts/codex/verify_codex_pack.py` ausfuehren.
3. `python3 scripts/codex/validate_release_docs.py --root . --json` ausfuehren.
4. `python3 scripts/codex/audit_codex_pack.py --root . --json` ausfuehren.
5. `python3 scripts/codex/sr_post_install_check.py --root . --json` ausfuehren.
6. `python3 scripts/codex/audit_sr_task_contracts.py --root . --json` ausfuehren.
7. `SR_LOTS.yaml`, `SR_PASSES.yaml`, aktive Loop Contracts und den SR Contract 3.1.0 oder explizit erkannte Legacy-3.0.0-Contracts validieren.
8. `docs/codex/CHANGELOG.md`, Zielversion, lokalisierte oeffentliche Prompts und additive Erhaltung projektspezifischer Dateien pruefen.

Jede Warnung als kompatiblen Legacy-Zustand, Dokumentationsschuld, `repair` oder echten externen Blocker klassifizieren. Installer-Code `0` allein reicht nicht.

Pro Repository Version, Kontrollen, Fehler, Warnungen, Contracts, offene `validated_requests`, fehlende Nachweise und naechste Aktion berichten. `user_testing` gilt nur fuer technisch vollstaendige Arbeit; fehlende Implementierung bleibt `repair`.

Ohne Fix stoppen und fuer jeden Repair-Scope exakte Validierung verlangen.
