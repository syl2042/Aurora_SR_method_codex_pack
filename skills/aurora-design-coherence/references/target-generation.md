# Target visual generation

The target visual is the contract the human validates before implementation.

## Inputs

Generate from:

- current screenshot(s);
- `SCREEN_REDESIGN_SPEC.md`;
- information triage;
- selected reference patterns;
- approved Reference Lock;
- Decision Ledger;
- existing product theme/brand constraints;
- target Aurora/shadcn components.

## Renderer policy

Use the strongest available AI-operated renderer:

1. direct image generation for fast concept validation;
2. Magic Patterns / Stitch / Figma Make / equivalent when connected and useful;
3. generated non-production prototype only when a visual renderer is unavailable and it can be produced without modifying the product.

The human validator must not be required to edit Figma or manually design the screen.

## Fidelity rules

The visual must:

- preserve real product concepts and plausible data;
- express the specified information hierarchy;
- respect progressive disclosure decisions;
- avoid invented business features;
- avoid fake metrics not present in the product;
- preserve theme direction unless a rebrand was requested;
- represent realistic density for a B2B application.

## Variants

Generate 1 strong default. Generate 2–3 variants only when there is a meaningful unresolved structural choice, not merely different decoration.

## Required presentation

Present at minimum:

- `CURRENT` — rendered current screen;
- `TARGET` — proposed visual;
- 3–7 structural changes in concise prose.

Do not send implementation instructions to Codex until the human explicitly approves the target.

## Codex App prototype renderer

When running in Codex App and no direct image/design renderer is available, create an **isolated non-production target prototype** solely to render the approved design proposal before implementation.

Rules:

- place it under `docs/design/prototypes/<screen>/` or another clearly non-production design workspace;
- use static representative data only; do not wire APIs, auth, database, or business actions;
- reuse the app's actual typography/tokens/Aurora or shadcn components when that improves fidelity, but do not import the prototype into production routes;
- implement only enough interaction to demonstrate layout/disclosure states that matter to validation;
- render it with Playwright at the reference viewport and save `TARGET.png` beside the redesign spec;
- present the screenshot to the human as `TARGET PROPOSED`;
- iterate this prototype until `TARGET APPROVED`;
- only then modify production UI files.

This prototype is a renderer for the Design Director's decisions, not a second implementation of the product.
