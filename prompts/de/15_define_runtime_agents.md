# Anwendungsspezifische Runtime Agents definieren

Nicht coden.

Ziel: Kontrollierte Karte von Runtime AI Agents vorschlagen, ohne sie zu aktivieren.

Anweisungen:

1. `docs/codex/AI_AGENT_RUNTIME_METHOD.md` lesen.
2. Projektprofil, Skill Map, Domänendokumente, Schemas, Routen, DB-Modelle und RAG/KG-Dokumentation prüfen, falls verfügbar.
3. Maximal fünf Kandidaten vorschlagen.
4. Fuer jeden Agent `agent_key`, `runtime_shape` (`micro_agent`, `workflow_agent`, `delegation_agent` oder `mini_agent`), begrenzte Produktaktion, stabile interne Representation, Business Function, Prompt Contract, User Message Builder, kontrollierte SQL/RAG-Bindings, Runtime Skills, Tools/Actions, Routing/Fallback, typisierte Input/Output-Modelle, JSON-Schema-Quelle, Validierungsmodus, Invalid-Output-Policy, Traces, Tests, UI-Platzierung, Risiken und Human Validation definieren.
5. Nach dem Vorschlag stoppen und Validierung anfordern.

Constraints:
- die Methode ist framework-, provider-, domain- und UI-agnostisch;
- der Prompt ist nicht die Source of Truth, sondern eine Projektion des Runtime Contract;
- Inspection/Preparation Tools von verpflichtenden Actions unterscheiden;
- kein Agent ist ohne Validierung aktiv.

Ein LLM darf niemals freies SQL erzeugen und ausführen. Kritische Aktionen brauchen menschliche Validierung.
