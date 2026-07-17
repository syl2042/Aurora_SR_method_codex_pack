# SR Method in ein Zielprojekt installieren

Du arbeitest in einem Software-Repository, das die Aurora SR Method erhalten soll.

Ziel: SR Method installieren, ohne Anwendungscode, Migrationen, Abhängigkeiten, Secrets oder Geschäftslogik zu ändern.

Nutze das offizielle Source-Paket:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Anweisungen:

1. Lokale Kopie des offiziellen Pakets finden oder klonen.
2. Zielrepository vor jeder Änderung prüfen.
3. Installationsumfang erklären und bei Mutationen explizite Benutzervalidierung abwarten.
4. Nach Validierung den Installer mit Profil `default` ausführen.
5. Nach der Installation Verifikationsskripte ausführen, einschliesslich `validate_pass_contract.py` fuer `SR_PASSES.yaml`.
6. Pruefen, dass `SR_PASSES.yaml` installiert ist, und `prompts/de/08_define_sr_passes_from_lots.md` empfehlen, nachdem Lose definiert wurden.
7. Dateien, Prüfungen, Warnungen und nächste Schritte berichten.

Ändere keinen Anwendungscode. Erzeuge keine Migration. Berühre keine Secrets. Erfinde keine Projektregeln.
