# Installation

[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

Der empfohlene Ablauf ist **Codex-Prompt zuerst**. Python-Skripte sind technische Werkzeuge, die Codex nach der Prüfung ausführen kann.

## Zuerst den richtigen Pfad wählen

- Kein SR-Marker: Prompt `00`, SR 3.7.0 mit `--write` neu installieren.
- Vorhandener, alter oder partieller SR-Marker: Prompt `05`, nach Audit additiv mit `--upgrade` aktualisieren.
- Mehrere Repositories: pro Repository Version und Marker lesen, eine Zielmatrix erstellen und je ein `--upgrade` ausführen. Niemals eine gemeinsame Version annehmen.

Neuinstallationen zielen auf `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 und `SR_PASSES` 0.2. `implementation_status` und `evidence_status` bleiben getrennt. Die Installation darf keine `validated_requests` oder validierten Produkt-Lose erfinden. Der Installer verweigert `--write`, wenn bereits eine SR-Installation erkannt wird.

## In ein Zielprojekt installieren

1. Repository klonen.
2. Codex im Zielprojekt öffnen.
3. [prompts/de/00_install_codex_environment.md](prompts/de/00_install_codex_environment.md) einfügen.
4. Codex installieren, prüfen und berichten lassen.

Technischer Fallback:

Ohne `--write` oder `--upgrade` arbeitet der Installer nur als schreibgeschuetzte Vorschau. Beide Mutationsmodi schliessen sich gegenseitig aus.

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target /path/to/project --profile default --write
```

Neue Installationen enthalten `docs/codex/SR_PASSES.yaml`. SR Passes gruppiert mehrere SR-Lose in einen begrenzten Pass mit Abhaengigkeitsreihenfolge, gemeinsamem Preflight, menschlichen Validierungen und gruppierten E2E-Pruefungen. Lose bleiben die atomare Einheit in `SR_LOTS.yaml`.

Das Register startet mit `passes: []`. Dieser Zustand ist gueltig; die Installation erfindet keine Produkt-Pass. Prompt `08` wird erst nach Lektuere und Freigabe der Lose verwendet.

## Aktualisieren

Im Zielprojekt [prompts/de/05_upgrade_codex_environment.md](prompts/de/05_upgrade_codex_environment.md) einfügen. Codex soll auditieren, projektbezogene Dateien erhalten, den Plan melden und erst danach aktualisieren.

Historische `sr_contract` 3.0.0 bleiben lesbar. Keine Task Memories massenhaft umschreiben: nur aktive oder wiedereroeffnete Anforderungen nach Quellenpruefung normalisieren, offene requirement IDs erhalten und standardmaessig das urspruengliche Los wiedereroeffnen. Ein gruener Ordner darf Probleme anderer Zielordner nicht verdecken.

Repraesentative offizielle Layouts SR 2.2.0, 2.3.0, 2.3.5, 2.4.1 und 3.0.0 sind durch Upgrade-Regressionen abgedeckt. Ein fehlendes `SR_PASSES.yaml` wird als gueltiges `passes: []` angelegt. Unknown/partial oder lokal angepasste Layouts brauchen weiterhin ein Datei-Audit. Installer-Code 0 reicht nicht: `sr_post_install_check.py` muss ebenfalls gruen sein, sonst bleibt das Ziel in `repair`.

## Prüfen

[prompts/de/06_verify_sr_installation.md](prompts/de/06_verify_sr_installation.md) einfügen.

Release-Dokumentation und oeffentliche Prompts ebenfalls pruefen:

```bash
python3 scripts/codex/validate_release_docs.py --root . --json
```

Codex soll auch die Passes validieren, wenn die Datei existiert:

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

## SR Lots definieren

Nach dem Framing einer Funktion [prompts/de/09_define_sr_lots_from_scope.md](prompts/de/09_define_sr_lots_from_scope.md) verwenden, um `SR_LOTS.yaml` mit Lot Design Evidence Gate zu definieren.

## SR Passes definieren

Danach [prompts/de/08_define_sr_passes_from_lots.md](prompts/de/08_define_sr_passes_from_lots.md) verwenden, um eine kohaerente Passe in `SR_PASSES.yaml` vorzuschlagen. Diese Schritte aktualisieren nur den SR-Speicher und duerfen keinen Anwendungscode aendern.

## Pass Runtime Goal erzeugen

Fuer eine validierte Passe kann Codex den begrenzten Runtime-Goal erzeugen:

```bash
python3 scripts/codex/build_pass_runtime_goal.py --pass-id <PASS_ID> --output docs/codex/tasks/YYYY-MM-DD_<pass-id>/pass_runtime_goal.md
```

## Sitzung starten

[prompts/de/01_start_sr_session.md](prompts/de/01_start_sr_session.md) einfügen. Für Runtime Agents [prompts/de/15_define_runtime_agents.md](prompts/de/15_define_runtime_agents.md) verwenden.
