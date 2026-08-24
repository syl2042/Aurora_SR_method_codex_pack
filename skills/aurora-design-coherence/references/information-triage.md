# Information triage and progressive disclosure

## Mandatory classification

Inventory visible information, controls, metadata, statuses, explanations, diagnostics, and repeated summaries. Classify each item:

| Decision | Meaning |
|---|---|
| PROMOTE | Essential to the screen's primary decision/action; increase priority. |
| KEEP | Correct content, hierarchy, and location. |
| GROUP | Useful, but consolidate with related information. |
| MOVE | Useful, but belongs elsewhere in the flow or layout. |
| HIDE | Preserve behind progressive disclosure, advanced settings, or diagnostics. |
| REMOVE | No sufficient value for the target persona/context. |

## Progressive disclosure levels

- **L0 — Work**: information/action needed for the normal job.
- **L1 — Context**: secondary detail via drawer, popover, expansion, side rail, or detail area.
- **L2 — Advanced**: uncommon configuration for expert users.
- **L3 — Diagnostics**: IDs, raw logs, traces, provider/model internals, debug payloads, support data.

Do not confuse “inspectable” with “always visible”. AI and data products need traceability, but most traceability belongs in L1–L3.

## Developer-interface leakage checklist

Challenge by default:

- UUIDs and internal IDs;
- raw provider/model names;
- collection/vector-store identifiers;
- endpoint names;
- JSON/raw payloads;
- token counts and latency unless they drive the user's decision;
- ingestion pipeline internals;
- implementation terminology copied from database models;
- logs and stack-like status text;
- duplicated status explanations;
- configuration controls used only during setup.

## Visibility test

Keep information at L0 only when at least one is true:

1. the user needs it to understand current business state;
2. the user needs it to make the primary decision;
3. the user needs it to perform the primary action;
4. the user needs it frequently enough that disclosure creates measurable friction.

Otherwise move it down the disclosure ladder.
