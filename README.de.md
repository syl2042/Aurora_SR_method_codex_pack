# Aurora SR Method Codex Pack

SR Method 4.1 ist ein schlanker Ausfuehrungs-Harness fuer Codex: kurzer permanenter Kern, bedingte Verfahren, genaue Skill-Ausloeser, kompakter Zustand und angemessene Abschlusspruefung.

Status: **4.1.0 (`released`)**, veroeffentlicht am 2026-09-24.

[English](README.md) · [Français](README.fr.md) · **DE** · [Español](README.es.md) · [Português](README.pt.md)

[Installation](INSTALLATION.de.md) · [Changelog](CHANGELOG.md) · [Installations-Prompt](prompts/de/00_install_codex_environment.md) · [Upgrade-Prompt](prompts/de/05_upgrade_codex_environment.md) · [Pruefen](prompts/de/06_verify_sr_installation.md) · [Neu ausrichten](prompts/de/07_realign_sr_state_after_upgrade.md)

## Was sich in 4.1 aendert

- `AGENTS.md` wird abgeglichen und gekuerzt, statt durch neue Handbuchabschnitte zu wachsen.
- Der Standardkatalog enthaelt nur Lot-Orchestrierung, Diagnose, Architektur und visuelle UI-Pruefung.
- TDD, Planungsdateien, Terminalkompression, Diff-Review und RepoMap-Pflege sind Harness-Mechanismen, keine Skills.
- Keine absichtlich fehlschlagenden Tests, kuenstlichen roten Gates oder Entwicklungs-Rollback-Schleifen.
- Scope, Verification und Activation sind die einzigen Ausfuehrungsgrenzen.
- Neue Aufgaben koennen eine kompakte `task_state.yaml` verwenden; alte Vertraege bleiben lesbar.
- Im `core`-Modus erfolgen keine MCP-Aufrufe. `nexus_kg` folgt `MCP_POLICY.yaml` mit spaeter Aktivierung, Allowlist, Freigaben und Ergebnisbudgets.
- Eingabe, Cache-Lese-/Schreibvolumen, Kontextbelegung, Ausgabe und Tool-Ergebnisse werden getrennt gemessen.

## Betrieb und Upgrade

```text
AGENTS.md -> SR_ROUTES.json -> nur das ausgeloeste Verfahren
          -> 0 bis 2 spezialisierte Skills -> echte Quellen
          -> angemessene Abschlusspruefung
```

Die Aktualisierung ist versionsagnostisch: Eine alte Versionsnummer dient nur der Herkunft. Tatsaechliche Inhalte werden als fehlend, verwaltet, lokal geaendert, fremd, veraltet, konfliktbehaftet oder bereits ausgerichtet klassifiziert. Projektzustand bleibt erhalten; ein veraltetes Artefakt wird nur geloescht, wenn sein Inhalt als verwaltet erkannt ist.

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Details: [INSTALLATION.de.md](INSTALLATION.de.md). Versionshistorie und Migrationen stehen ausschliesslich in [CHANGELOG.md](CHANGELOG.md).
