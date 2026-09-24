# Installation — SR Method 4.1

Status: veroeffentlichte Version `4.1.0`. Eine eindeutige `SR_PACK_SOURCE` waehlen und `release_status`, `source_commit` sowie Git-Zustand festhalten.

[English](INSTALLATION.md) · [Français](INSTALLATION.fr.md) · [Español](INSTALLATION.es.md) · [Português](INSTALLATION.pt.md)

## Pfad nach beobachtetem Zustand waehlen

| Zielzustand | Prompt | Modus |
|---|---|---|
| Kein SR-Marker | `prompts/de/00_install_codex_environment.md` | `--write` |
| SR-Marker, teilweise oder unbekannt | `prompts/de/05_upgrade_codex_environment.md` | `--upgrade` |

Die vorherige Versionsnummer bestimmt niemals den Algorithmus. Vorschau, Konflikte und erhaltene Dateien pruefen, dann anwenden:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Fuer ein neues Ziel `--write` statt `--upgrade` verwenden. Die Transaktion sichert geaenderte Dateien, erkennt zwischenzeitliche Aenderungen und unterstuetzt ein genaues `--restore`.

Der Post-Check ist standardmaessig schreibgeschuetzt. `--write-report` nur fuer einen ausdruecklich gewuenschten dauerhaften Auditbericht verwenden.

Verwaltete Inhalte werden konvergiert, Projektzustand bleibt erhalten, unbekannte Anpassungen werden als Konflikt gemeldet und veraltete Dateien nur bei erkanntem verwaltetem Inhalt entfernt. Kein Produktcode, keine Secrets, Migrationen, Deployments, offenen Anforderungen oder historischen `SR_LOTS.yaml`/`SR_PASSES.yaml` werden veraendert.

Eine frische Installation enthaelt `SR_PASSES.yaml` mit `passes: []`, `MCP_POLICY.yaml` und `task_state.yaml`. Nach erfolgreicher Pruefung `prompts/de/07_realign_sr_state_after_upgrade.md` nur verwenden, wenn der Projektzustand real neu ausgerichtet werden muss. Die Passdefinition bleibt in `08_define_sr_passes_from_lots.md`, die Lots in `09_define_sr_lots_from_scope.md`; `build_pass_runtime_goal.py` bleibt ein optionales Legacy-Werkzeug.
