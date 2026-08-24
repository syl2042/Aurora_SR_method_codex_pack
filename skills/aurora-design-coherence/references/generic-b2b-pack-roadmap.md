# Generic B2B Design Coherence Roadmap

Use this reference only when preparing a generic version of this Auroramind pack for external users.

## Goal

Convert `aurora-design-coherence` into a reusable `b2b-design-coherence` pack for SaaS teams, agencies, freelancers, and product builders using AI coding agents.

## Positioning

A design governance pack for AI coding agents. It prevents Codex, Claude Code, Cursor, or similar agents from creating inconsistent, unmaintainable, or generic B2B interfaces.

## What to keep

- New app workflow.
- Existing app audit workflow.
- Design review workflow.
- Codex task handoff.
- Visual QA.
- Component tier logic.
- Premium B2B principles.
- Scripts for UI inventory and first-pass scoring.

## What to generalize

| Auroramind term | Generic term |
|---|---|
| AuroraAppShell | ProductAppShell |
| AuroraPageHeader | ProductPageHeader |
| AuroraMetricCard | ProductMetricCard |
| AuroraStatusBadge | ProductStatusBadge |
| AuroraDataTableShell | ProductDataTableShell |
| aurora_kits_modules | product-ui-kit |
| AURORA_DESIGN_AUDIT.md | PRODUCT_DESIGN_AUDIT.md |
| AURORA_DESIGN_MIGRATION_PLAN.md | PRODUCT_DESIGN_MIGRATION_PLAN.md |
| Nexus / AIS / MIA / Compta-IA | product app / AI app / vertical app |

## Generic config idea

A future generic pack may support:

```yaml
product_name: "Example SaaS"
ui_kit_name: "product-ui-kit"
component_prefix: "Product"
framework: "nextjs"
primitive_layer: "shadcn/radix"
analytics_layer: "tremor"
advanced_ux_layer: "kibo"
theme_policy: "preserve user-selectable themes"
```

## Do not change in the generic version

- Do not become a visual generator.
- Do not require Open Design.
- Do not create a full UI framework.
- Do not encourage one-shot redesigns.
- Do not promote decorative motion in business workflows.
