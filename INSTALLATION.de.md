# Installation

[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

Der empfohlene Ablauf ist **Codex-Prompt zuerst**. Python-Skripte sind technische Werkzeuge, die Codex nach der Prüfung ausführen kann.

## In ein Zielprojekt installieren

1. Repository klonen.
2. Codex im Zielprojekt öffnen.
3. [prompts/de/00_install_codex_environment.md](prompts/de/00_install_codex_environment.md) einfügen.
4. Codex installieren, prüfen und berichten lassen.

Technischer Fallback:

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target /path/to/project --profile default --write
```

Neue Installationen enthalten `docs/codex/SR_PASSES.yaml`. SR Passes gruppiert mehrere SR-Lose in einen begrenzten Pass mit Abhaengigkeitsreihenfolge, gemeinsamem Preflight, menschlichen Validierungen und gruppierten E2E-Pruefungen. Lose bleiben die atomare Einheit in `SR_LOTS.yaml`.

## Aktualisieren

Im Zielprojekt [prompts/de/05_upgrade_codex_environment.md](prompts/de/05_upgrade_codex_environment.md) einfügen. Codex soll auditieren, projektbezogene Dateien erhalten, den Plan melden und erst danach aktualisieren.

## Prüfen

[prompts/de/06_verify_sr_installation.md](prompts/de/06_verify_sr_installation.md) einfügen.

Codex soll auch die Passes validieren, wenn die Datei existiert:

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

## SR Passes definieren

Nachdem Lose erstellt wurden oder nach einem Upgrade eines bestehenden Projekts, [prompts/de/08_define_sr_passes_from_lots.md](prompts/de/08_define_sr_passes_from_lots.md) einfuegen. Dieser Schritt aktualisiert nur den SR-Speicher und darf keinen Anwendungscode aendern.

## Sitzung starten

[prompts/de/01_start_sr_session.md](prompts/de/01_start_sr_session.md) einfügen. Für Runtime Agents [prompts/de/15_define_runtime_agents.md](prompts/de/15_define_runtime_agents.md) verwenden.
