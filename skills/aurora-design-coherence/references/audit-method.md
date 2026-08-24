# Aurora Design Audit V2

## Goal

Evaluate whether an Auroramind app supports user decisions and workflows with premium B2B clarity while preserving business behavior and suite coherence.

## Evidence

Use code inventory plus rendered application evidence whenever possible. A repository-only audit cannot fully score hierarchy, density, navigation clarity, or user comprehension.

## Scoring grid

| Area | Weight | What good looks like |
|---|---:|---|
| Product intent and job clarity | 14 | screens organize around user jobs/decisions/actions |
| Information hierarchy/disclosure | 14 | right information visible at L0; technical detail progressively disclosed |
| Shell and navigation | 12 | predictable orientation, hierarchy, and movement |
| Page composition and density | 10 | calm, deliberate layout; no generic card stacking |
| Tables/lists/work objects | 10 | work objects use appropriate comparison/filter/detail patterns |
| Status/actions language | 7 | clear business language and stable status semantics |
| AI/data trust patterns | 9 | evidence/traceability available at the right level |
| Responsive/accessibility/states | 9 | intentional responsive design and non-happy paths |
| Theme/component coherence | 8 | Aurora/shadcn discipline without visual drift |
| Technical maintainability | 7 | reusable patterns and safe migration path |

## Procedure

1. Identify app role and target personas.
2. Inventory framework, routes, UI libraries, shared patterns, theme system.
3. Inspect representative rendered screens: shell, list/workspace, detail, settings, complex AI/data screen.
4. For each screen, write persona/job/primary action and complete information triage for visible technical content.
5. Identify developer-interface leakage and generic AI-slop patterns.
6. Compare high-impact screens with current design references when available.
7. Score manually using rendered + code evidence.
8. Identify quick wins and structural redesign candidates separately.
9. Recommend screens for the first redesign pilot.
10. Do not modify code in audit-only mode.

## Script use

`scan_ui_inventory.py` and `score_design_coherence.py` remain useful for inventory/code signals only. Their heuristic score does not replace this V2 product/visual score.
