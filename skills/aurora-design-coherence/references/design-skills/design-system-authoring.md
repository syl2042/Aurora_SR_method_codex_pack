# Design System Authoring Skill

Use this reference to create or improve an app-level design system markdown file.

## Goal

Create an implementation-ready design system for an Auroramind app without locking it to one color theme. The design system should guide Codex and other agents toward coherent screens, components, states, and data patterns.

## Required sections

1. Product role and UX promise.
2. User types and jobs-to-be-done.
3. Navigation model.
4. Layout and density rules.
5. Component tiers selected for this app.
6. Page patterns.
7. Cards, metrics, tables, filters, badges, drawers.
8. Forms and validation.
9. AI/data patterns when relevant.
10. Empty/loading/error/permission states.
11. Responsive behavior.
12. Theme and token boundaries.
13. Forbidden patterns.
14. Codex implementation guidance.

## Design system rules

- Do not define a fixed brand recolor unless the user asks.
- Express color through theme tokens, tone props, and status props.
- Prefer structural rules over decorative instructions.
- Make the design system usable by Codex as direct implementation guidance.
- Keep app-specific patterns specific, and promote repeated patterns to Aurora kit candidates.

## Output naming

Use an app-specific name:

- `NEXUS_POCKET_DESIGN_SYSTEM.md`
- `AIS_DESIGN_SYSTEM.md`
- `MIA_DESIGN_SYSTEM.md`
- `SOCIALGENIE_DESIGN_SYSTEM.md`
- `APP_DESIGN_SYSTEM.md` for generic or unnamed apps.
