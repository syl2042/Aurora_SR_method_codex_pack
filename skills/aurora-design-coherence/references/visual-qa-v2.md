# Visual QA V2 — Current / Target / Implemented

Use after Codex implementation.

## Comparable evidence

Capture with the same, or intentionally documented, values for:

- route;
- persona/permissions;
- viewport;
- product state/data;
- open drawer/dialog state when relevant.

## Compare three artifacts

1. `CURRENT` — baseline before redesign.
2. `TARGET` — human-approved target.
3. `IMPLEMENTED` — rendered production/dev implementation.

## Review order

1. product intent and primary action;
2. information hierarchy and disclosure;
3. navigation/interaction behavior;
4. target layout/density fidelity;
5. Reference Lock / Decision Ledger fidelity;
6. component mapping;
7. responsive behavior;
8. empty/loading/error/permission states;
9. themes and accessibility basics;
10. technical regressions.

## Verdicts

- **PASS** — hierarchy, behavior, disclosure, and visual target are materially respected.
- **MINOR FIX** — localized styling/spacing/state issues without structural drift.
- **FAIL** — structural hierarchy, navigation, visibility, or approved target is materially violated.

## Findings

Each finding states:

- target expectation;
- implemented observation;
- evidence;
- affected file/component when identifiable;
- exact correction;
- severity.

Do not pass merely because the page builds and the tests are green.
