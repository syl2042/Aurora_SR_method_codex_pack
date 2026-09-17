# Installation

## SR 4.0.0 — veroeffentlichte Version

Zielquelle: `SR_PACK_SOURCE` ausdruecklich auswaehlen, entweder eine identifizierte veroeffentlichte Version oder den freigegebenen lokalen SR-4.0.0-Kandidaten. `core/SR_PACK_VERSION.json` (`version`, `release_status`) lesen; `source_commit`, Git-Zustand und bei lokalen Aenderungen einen Inhaltsfingerabdruck einschliesslich verwendeter unversionierter Quelldateien dokumentieren. Einen `unreleased`-Kandidaten nicht als Release ausgeben. Den Kandidaten nicht durch einen Clone der neuesten veroeffentlichten Version ersetzen; fehlt die angeforderte Quelle, vor der Installation stoppen und klaeren.

Fuer dieses SR-4.0.0-Ziel muss die Quelle `version: 4.0.0` angeben. Falls kein Release 4.0.0 veroeffentlicht ist, nur den freigegebenen lokalen Kandidaten verwenden oder sein Fehlen melden; niemals stillschweigend eine andere Version installieren.

Pfade: Neuinstallation `00 -> 06`; bestehende Installation `05 -> 06 -> 07`. Prompt `06` prueft nur; `07` schlaegt Realignment vor und wartet vor Memory-Aenderungen auf `je valide`. Beide Pfade autorisieren keine Anwendungsentwicklung.

SR 4 laedt Verfahren gezielt ueber `SR_BOOTSTRAP.md` und `SR_ROUTES.json`. Gates, HITL, offene Anforderungen und Vertragsschemata bleiben erhalten. Die Paketversion erzwingt keine Konvertierung alter Vertraege.

### Erstinstallation
Lokale Regeln pruefen; `je valide` fuer den Umfang erhalten; Vorschau, `--write`, danach Pruefung. Vorhandene Projektdateien bleiben erhalten oder werden ausdruecklich zusammengefuehrt. Kein Anwendungscode wird geaendert.

### Versionsunabhaengiges Upgrade
Nach Inhaltspruefung `--upgrade` verwenden. Die alte Versionsnummer ist nur informativ. Alte, unversionierte, teilweise oder gemischte Installationen werden anhand der Dateien erkannt. Unbekannte oder angepasste Paketdateien blockieren das Ersetzen: nicht loeschen, um den Konflikt zu umgehen. Abgleich pruefen und freigeben. Vertraege, offene Lose, Aufgabenhistorie, Handoffs und Fachskills erhalten.

Die Vorschau schreibt nur bei ausdruecklichem `--plan-out`. Plaene enthalten Dateiinhalte und bleiben lokal. `--apply-plan` verweigert veraltete Plaene. Transaktionen sichern geaenderte Dateien; `--restore` ueberschreibt keine spaeteren Aenderungen. Upgrades nie mit `--write` erzwingen. Die Zielversion allein beweist keinen Erfolg: Postcheck erforderlich.

Vor Freigabe mit dem folgenden Befehl eine Vorschau erstellen; nach `je valide` nur den passenden Modus waehlen. `--plan-out` schreibt einen lokalen Plan und erfordert Freigabe; `--apply-plan` lehnt veraltete Diagnosen ab. `--restore` ist ein separater Vorgang mit dem exakten Transaktionsjournal und verweigert spaetere Aenderungen. Keine Datei zur Konfliktumgehung loeschen.

Nur Vorschau:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Neuinstallation nach Freigabe:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --write
```

Bestehende Installation nach Freigabe:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

Nur Pruefung:

```bash
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Optionaler lokaler Plan nach Freigabe:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --plan-out "$SR_PLAN_FILE"
```

Freigegebenen Plan anwenden, Alternative zu direkten Befehlen:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --apply-plan "$SR_PLAN_FILE"
```

Separate Wiederherstellung, nur bei Bedarf und Freigabe:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --restore "$SR_JOURNAL_FILE"
```


[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

Der empfohlene Ablauf ist **Codex-Prompt zuerst**. Python-Skripte sind technische Werkzeuge, die Codex nach der Prüfung ausführen kann.

## Zuerst den richtigen Pfad wählen

- Kein SR-Marker: Prompt `00`, SR 4.0.0 mit `--write` neu installieren.
- Vorhandener, alter oder partieller SR-Marker: Prompt `05`, nach Audit additiv mit `--upgrade` aktualisieren.
- Mehrere Repositories: pro Repository Version und Marker lesen, eine Zielmatrix erstellen und je ein `--upgrade` ausführen. Niemals eine gemeinsame Version annehmen.

Neuinstallationen zielen auf `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 und `SR_PASSES` 0.2. `implementation_status` und `evidence_status` bleiben getrennt. Die Installation darf keine `validated_requests` oder validierten Produkt-Lose erfinden. Der Installer verweigert `--write`, wenn bereits eine SR-Installation erkannt wird.

## In ein Zielprojekt installieren

1. Gepruefte lokale Quelle gemaess Zielquelle auswaehlen.
2. Codex im Zielprojekt öffnen.
3. [prompts/de/00_install_codex_environment.md](prompts/de/00_install_codex_environment.md) einfügen.
4. Codex installieren, prüfen und berichten lassen.

Technischer Fallback:

Ohne Mutationsoption und ohne `--plan-out` erstellt der Installer eine schreibgeschuetzte Vorschau. `--write`, `--upgrade`, `--apply-plan` und `--restore` schliessen sich gegenseitig aus.

Den zuvor ausgewaehlten und geprueften Clone `SR_PACK_SOURCE` verwenden. Fuer ein Release bei Bedarf die offizielle Quelle klonen und die freigegebene veroeffentlichte Referenz auswaehlen; Klonen allein waehlt nicht den SR-4-Kandidaten. Der Kandidat erfordert den freigegebenen lokalen Inhalt. `SR_TARGET` vor den Befehlen auf den Zielprojektpfad setzen.

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
