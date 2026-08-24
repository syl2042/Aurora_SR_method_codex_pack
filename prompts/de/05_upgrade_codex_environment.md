# Projekt auf die neueste SR Method aktualisieren

Du arbeitest in einem Anwendungs-Repository, das bereits eine Aurora SR Method Installation enthaelt, moeglicherweise alt, unvollstaendig oder lokal angepasst.

Nachweisbares Ziel: Die SR Method auf die neueste offizielle Version aktualisieren, ohne Regression, ohne Anwendungscode zu aendern, ohne projektspezifische Anpassungen zu ueberschreiben, und das Projekt vor jeder Entwicklungsfortsetzung in einen neu ausgerichteten SR-Zustand bringen.

Dieser Prompt akzeptiert ein Ziel oder eine explizite Repository-Liste. Behandle bei mehreren Ordnern jedes Repository als unabhaengiges Ziel und erstelle vor jeder Mutation die Matrix `repository | gelesene Marker | erkannte Version | Installationszustand | Upgrade-Flow | zu erhaltende Dateien | Freigabe`. Nimm niemals eine gemeinsame Version an; aktualisiere und pruefe Ziel fuer Ziel.

Hat ein Ziel keinen SR-Marker, klassifiziere es als `fresh_install`, entferne es aus dem Upgrade-Flow und verwende `00_install_codex_environment.md` mit eigener Freigabe.

Offizielle SR Method Quelle:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Lokale Pack-Quelle:

```text
SR_PACK_SOURCE
```

`SR_PACK_SOURCE` bezeichnet den lokalen Pfad zum offiziellen Clone auf dem aktuellen Server. Nimm niemals einen maschinenspezifischen absoluten Pfad an. Wenn der Benutzer keinen Pfad angegeben hat, erkenne ihn oder schlage einen passenden lokalen Pfad vor, zum Beispiel `./.sr-method-pack`, `/opt/aurora/SR_Method` oder ein vom Benutzer bestaetigtes Arbeitsverzeichnis.

Wenn die lokale Quelle nicht existiert oder kein Clone des offiziellen Repositories ist, schlage vor, sie aus dem offiziellen GitHub-Repository zu erstellen oder zu aktualisieren, bevor das Upgrade angewendet wird. Lade nichts aus einer anderen Quelle ohne Benutzerfreigabe.

Strikte Regeln:

- Aendere keinen Anwendungscode.
- Erzeuge keine Migrationen.
- Aendere keine Anwendungsabhaengigkeiten.
- Beruehre keine Secrets, Umgebungsvariablen oder sensiblen Konfigurationsdateien.
- Ersetze `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `PROJECT_PROFILE.yaml`, `SKILL_MAP.md`, `docs/codex/SR_LOTS.yaml`, `docs/codex/SR_PASSES.yaml`, Task Memories, Handoffs, Entscheidungen oder Projektskills nicht blind.
- Erhalte lokale Projektanpassungen.
- Erhalte Legacy-Task-Memory-Dateien; erstelle keine rueckwirkenden Contracts im Batch ohne explizite Freigabe.
- Erhalte `SR_LOTS.yaml`. Wenn `SR_PASSES.yaml` fehlt, fuege ein gueltiges Register `passes: []` hinzu; kopiere keine Beispiel-Pass und konvertiere alte Lose oder Task Memories nicht automatisch in validierte Passes.
- Konvertiere alte Lose nicht massenhaft, um `design_evidence` hinzuzufuegen; fuege das Lot Design Evidence Gate nur fuer Lose hinzu, die nach dem Upgrade erstellt, promoted oder wiederaufgenommen werden.
- Fuege Pass Runtime Goal Tooling additiv hinzu (`build_pass_runtime_goal.py`, Template `pass_runtime_goal.md`, Optionen `sr_passes.pass_runtime_goal`), ohne ein Goal zu generieren, solange keine Pass validiert ist.
- Starte niemals `/goal` waehrend des Upgrades. Das Upgrade bereitet die Methode vor; Goal-Ausfuehrung kommt erst nach Realignment, Pass Planning und Benutzerfreigabe.
- Schliesse, promote oder reklassifiziere kein Anwendungs-Los und keine Anwendungs-Pass als impliziten Nebeneffekt des Upgrades. Wenn der Benutzer ausdruecklich verlangt, im selben Auftrag ein Los oder eine Pass zu schliessen, behandle diese Schliessung als separate Unterphase nach dem Upgrade, mit validiertem Scope, eigenem SR-Contract, Nachweisen und separatem Bericht.
- Erhalte historische Task Memories ohne `propagation_gate`: melde sie als Legacy Warnings, nicht als blockierende Fehler. Neue Templates und Contracts nach dem Upgrade muessen das Propagation Gate enthalten.
- Erhalte `sr_contract` 3.0.0 lesekompatibel. Neue Task Memories und wiedereroeffnete Lose verwenden 3.1.0 mit getrenntem `implementation_status` und `evidence_status`.
- Schreibe alte `validated_requests` nicht massenhaft um. Markiere Multi-Lot-Contracts mit nur einer globalen Anforderung; normalisiere nur aktive oder wiedereroeffnete Umfaenge nach Quellenpruefung und menschlicher Freigabe.
- Das Upgrade darf offene, partielle oder defekte Anforderungen weder schliessen noch verschieben oder in neue Lose umwandeln.
- Im vollen SR-Betrieb muss jede SR-Versionsaenderung `docs/CURRENT_STATE.md` mit installierter Version, Review-Datum, ausgefuehrten Checks, letztem `NEXT_SESSION_PROMPT.md`, wichtigen Losen und naechstem Schritt aktualisieren.
- Ein `loop_contract.json` vom Typ `upgrade` darf nicht als `done` geschlossen werden, wenn `memory_updates.current_state_updated=false` ist.
- Vor jeder Dateiaenderung den Upgrade-Plan vorlegen und explizite Benutzerfreigabe abwarten.

Schritt 1 - Versionsdiagnose:

1. Lies vorhandene SR-Dateien:
   - `docs/codex/SR_PACK_VERSION.json`, falls vorhanden;
   - `docs/codex/SR_LOTS.yaml`, falls vorhanden;
   - `docs/codex/SR_PASSES.yaml`, falls vorhanden;
   - `docs/CURRENT_STATE.md`, falls vorhanden;
   - `AGENTS.md`, falls vorhanden;
   - `docs/codex/tasks/`, falls vorhanden.
2. Fuehre verfuegbare Audits ohne Aenderung aus:
   - `python3 scripts/codex/audit_codex_pack.py --json`, falls verfuegbar;
   - `python3 scripts/codex/verify_codex_pack.py`, falls verfuegbar;
   - `python3 scripts/codex/sr_post_install_check.py --root .`, falls verfuegbar.
3. Wenn diese Skripte nicht existieren oder wegen einer zu alten Version fehlschlagen, klassifiziere die Version als `unknown` oder `legacy`.

Schritt 2 - Klassifizierung:

Klassifiziere das Projekt in einen Flow:

- `upgrade_minor_3x`, wenn die installierte Version bereits `3.x` ist;
- `upgrade_standard_235_plus`, wenn die Version `2.3.5+` ist;
- `upgrade_legacy_unknown`, wenn die Version fehlt, unlesbar ist, unter `2.3.5` liegt oder die SR-Installation unvollstaendig ist.

SR-3.7.0-Matrix: Neuinstallation auf Schemas 3.1.0/1.1 und Lots 0.4/Passes 0.2; SR 3.6.x additiv auffrischen; SR 3.0-3.5 mit Legacy-Lesen, Warnungen und gezielter Normalisierung aktiver/wiedereroeffneter Lose; SR 2.x/unknown/partial mit Backup und Datei-Inventar; lokale Anpassungen ausserhalb verwalteter SR-Bloecke erhalten.

Fuer repraesentative offizielle Layouts SR 2.2.0, 2.3.0, 2.3.5, 2.4.1 und 3.0.0 bestehen Upgrade-Regressionstests. Unknown/partial bleibt ein Datei-Audit; die Fixture beweist den Minimalpfad, nicht jede lokale Anpassung.

Schritt 3 - Offizielle Quelle:

1. Pruefe, ob ein lokaler Clone des offiziellen Packs bereits existiert.
2. Falls ja, pruefe Remote und Git-Zustand.
3. Falls nein, schlage vor zu klonen:
   `git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git ./.sr-method-pack`
4. Verwende nur die offizielle Quelle oder einen verifizierten lokalen Clone.
5. Notiere den verwendeten Source-Commit im Abschlussbericht.

Schritt 4 - Analyse vor Mutation:

Vergleiche die aktuelle Installation mit der neuesten Pack-Version und identifiziere:

- fehlende SR-Dateien;
- alte SR-Dateien;
- projektspezifische Dateien, die erhalten bleiben muessen;
- Dateien, die vorsichtig gemerged werden muessen;
- Vorhandensein oder Fehlen von `SR_PASSES.yaml`;
- Vorhandensein oder Fehlen des Pass Runtime Goal Toolings;
- Vorhandensein oder Fehlen des Lot Design Evidence Gate;
- Ueberschreibungsrisiken;
- Anwendungs-Lose oder -Passes, die eventuell wiederaufgenommen oder geschlossen werden muessen, aber nur bei ausdruecklicher Benutzeranforderung als separate Unterphase zu behandeln sind;
- alte Contracts oder Task Memories, die als Legacy Warnings erhalten bleiben.

Wichtig: Alte Lose ohne `design_evidence` duerfen nicht im Batch geaendert werden. `design_evidence` darf nur zu Losen hinzugefuegt werden, die nach dem Upgrade erstellt, promoted oder wiederaufgenommen werden.

Schritt 5 - Plan zur Freigabe:

Vor jeder Aenderung einen kurzen Plan vorlegen mit:

- erkannter Version;
- gewaehltem Upgrade-Flow;
- hinzuzufuegenden Dateien;
- zu aktualisierenden Dateien;
- zu erhaltenden Dateien;
- identifizierten Risiken;
- geplanten Verifikationsbefehlen;
- erwarteter Auswirkung auf `SR_LOTS.yaml`, `SR_PASSES.yaml`, `AGENTS.md`, `CURRENT_STATE.md` und `docs/codex/tasks/`.
- Bestaetigung, dass kein Anwendungs-Los und keine Anwendungs-Pass implizit durch das Upgrade geschlossen wird; jede angeforderte Schliessung muss als validierte Unterphase isoliert werden.

Warte auf explizite Benutzerfreigabe, bevor du Dateien aenderst.

Schritt 6 - Upgrade nach Freigabe:

Nur nach Freigabe:

1. Wende das SR-Upgrade additiv an.
2. Erhalte Projektdateien und Historie.
3. Aktualisiere notwendige SR-Skripte, Templates, Prompts und Docs.
4. Fuege `SR_PASSES.yaml` mit `passes: []` hinzu, wenn es fehlt. Prompt `08` fuellt das Register erst nach Lektuere der Lose und menschlicher Freigabe.
5. Fuege Pass Runtime Goal Tooling hinzu, wenn es fehlt:
   - `build_pass_runtime_goal.py`
   - Template `pass_runtime_goal.md`
   - Optionen `sr_passes.pass_runtime_goal`
6. Pruefe, dass das Goal Length Gate vorhanden ist:
   - `max_goal_command_chars: 1000`
   - `hard_limit: 4000`
7. Pruefe, dass das Lot Design Evidence Gate fuer neue oder wiederaufgenommene Lose dokumentiert und aktiv ist.

Schritt 7 - Verifikation:

Fuehre die verfuegbaren und passenden Checks aus:

- `python3 scripts/codex/audit_codex_pack.py`
- `python3 scripts/codex/verify_codex_pack.py`
- `python3 scripts/codex/sr_post_install_check.py --root .`
- `python3 scripts/codex/validate_release_docs.py --root . --json` fuer `CHANGELOG.md`, Version und lokalisierte oeffentliche Prompts
- `python3 scripts/codex/find_next_session_prompt.py --root .`
- `python3 scripts/codex/audit_sr_project.py --root .`
- `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml`, wenn die Datei existiert
- `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml`, wenn `SR_PASSES.yaml` existiert
- `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json`, wenn vorhanden
- `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json`, wenn vorhanden
- `python3 scripts/codex/audit_sr_task_contracts.py --root .`
- `python3 scripts/codex/context_budget_report.py --root . --compact`
- `python3 scripts/codex/validate_skills.py --path ~/.codex/skills`, wenn Method Skills installiert sind

Wenn einige Skripte vor dem Upgrade fehlen, melde das als normal fuer eine alte Version und fuehre sie nach dem Upgrade erneut aus.

Exit-Code 0 des Installers reicht nicht fuer einen erfolgreichen Abschluss. `sr_post_install_check.py` muss ebenfalls gruen sein; sonst bleibt das Ziel in `repair`.

Schritt 8 - Pflicht-Realignment:

Nach dem Upgrade `docs/CURRENT_STATE.md` aktualisieren oder die Aktualisierung vorschlagen mit:

- SR-Version vorher;
- SR-Version nachher;
- Update-Datum;
- verwendeter Source-Commit;
- hinzugefuegte oder aktualisierte Dateien;
- erhaltene Dateien;
- Legacy Warnings;
- Status `SR_LOTS.yaml`;
- Status `SR_PASSES.yaml`;
- Status Pass Runtime Goal;
- Status Lot Design Evidence Gate;
- empfohlener naechster Schritt.

Schritt 9 - Empfohlene Fortsetzung:

Am Ende die Anwendungsentwicklung nicht direkt fortsetzen.

Schlage je nach Projektzustand diese Sequenz vor:

1. `07_realign_sr_state_after_upgrade.md` nutzen, um den SR-Zustand neu auszurichten;
2. `09_define_sr_lots_from_scope.md` nutzen, um Lose mit vorheriger Analyse der betroffenen Dateien zu erstellen oder zu promoten;
3. `08_define_sr_passes_from_lots.md` nutzen, um Losgruppen automatisch als Passes vorzuschlagen;
4. `pass_runtime_goal.md` nur nach menschlicher Validierung einer Pass generieren;
5. `/goal` nur fuer eine validierte Pass starten, niemals waehrend des Upgrades.

Erwarteter Abschlussbericht:

- Version vorher/nachher;
- gewaehlter Upgrade-Flow;
- verwendeter SR Method Source-Commit;
- geaenderte Dateien;
- erhaltene Dateien;
- erfolgreiche Validierungen;
- fehlgeschlagene oder nicht anwendbare Validierungen;
- Legacy Warnings;
- Anwendungs-Lose oder -Passes, die als Kandidaten fuer Schliessung oder Wiederaufnahme erkannt wurden, sowie Status jeder ausdruecklich angeforderten Schliessungs-Unterphase;
- vorgeschlagene naechste Aktion.

Pflichtabschluss: vor jeder Anwendungsaenderung oder Pass-Ausfuehrung auf Validierung warten.
