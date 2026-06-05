# Aurora SR Method Codex Pack

[English](README.md) |
[Francais](README.fr.md) |
[Deutsch](README.de.md) |
[Portugues](README.pt.md) |
[Espanol](README.es.md)

[Repository mit Stern markieren](https://github.com/syl2042/Aurora_SR_method_codex_pack/stargazers) |
[Dokumentation](https://docs.auroramind.fr/docs/SR_Method) |
[Mit Codex installieren](INSTALLATION.de.md) |
[Projekt aktualisieren](prompts/de/05_upgrade_codex_environment.md) |
[Installation prüfen](prompts/de/06_verify_sr_installation.md)

## Was ist das?

Aurora SR Method Codex Pack ist ein öffentliches Source-Paket, mit dem eine gesteuerte Codex-Arbeitsmethode in Softwareprojekten installiert wird.

SR bedeutet **Specification Runtime**. Die Methode gibt Codex einen projektlokalen Arbeitsrahmen: Bootstrap-Regeln, Task-Memory-Vorlagen, Evidence Gates, Repo Maps, kontrollierte Prompts, Validierungsskripte und wiederverwendbare Method Skills.

```text
Pack klonen -> Codex-Prompt einfügen -> SR Method installieren -> Prüfen -> Gesteuert entwickeln
```

## Sprachrichtlinie

Der Kern der SR Method bleibt als kanonische technische Sprache auf Englisch.

Die Einstiegspunkte für Entwickler sind mehrsprachig: README-Dateien, Installationsanleitungen und kopierbare Codex-Prompts.

Ein installiertes Projekt kann Codex anweisen, mit dem Benutzer auf Deutsch zu sprechen. Der technische Methodenkern bleibt Englisch.

## Schnellstart

1. Repository klonen.
2. Codex im Zielprojekt öffnen.
3. Den deutschen Installationsprompt einfügen.
4. Codex prüfen, installieren, verifizieren und berichten lassen.

Wichtige Prompts:

| Aktion | Prompt |
| --- | --- |
| Installieren | [00](prompts/de/00_install_codex_environment.md) |
| Sitzung starten | [01](prompts/de/01_start_sr_session.md) |
| Aktualisieren | [05](prompts/de/05_upgrade_codex_environment.md) |
| Prüfen | [06](prompts/de/06_verify_sr_installation.md) |
| Runtime Agents definieren | [15](prompts/de/15_define_runtime_agents.md) |

Python-Befehle sind technische Werkzeuge oder Fallbacks. Der empfohlene Ablauf ist prompt-first mit Codex.

## Öffentlicher Inhalt

```text
core/             englischer kanonischer Methodenkern und Templates
prompts/          Root-Prompts und mehrsprachige Einstiegsprompts
scripts/          Installation, Audit und Validierung
skills-method/    wiederverwendbare Codex Method Skills
blueprints/       Templates für Lots, Inbox, Tasks und Skills
profiles/         generische Profile
project-skills/   Platzhalter für lokale Projektskills
adr/              ADR-Template
```

Der öffentliche Repository-Zustand enthält keine Projektzustände, historischen Tasks, `.docx`, lokalen Handoffs, Kundenpfade oder Projektdaten.

## Lizenz

MIT License. Siehe [LICENSE](LICENSE).
