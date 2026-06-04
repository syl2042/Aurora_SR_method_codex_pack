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

## Aktualisieren

Im Zielprojekt [prompts/de/05_upgrade_codex_environment.md](prompts/de/05_upgrade_codex_environment.md) einfügen. Codex soll auditieren, projektbezogene Dateien erhalten, den Plan melden und erst danach aktualisieren.

## Prüfen

[prompts/de/06_verify_sr_installation.md](prompts/de/06_verify_sr_installation.md) einfügen.

## Sitzung starten

[prompts/de/01_start_sr_session.md](prompts/de/01_start_sr_session.md) einfügen. Für Runtime Agents [prompts/de/15_define_runtime_agents.md](prompts/de/15_define_runtime_agents.md) verwenden.
