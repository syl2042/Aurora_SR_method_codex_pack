# Tremor and Kibo policy

## Tremor policy

Use Tremor for analytics and dashboard primitives only. Tremor is useful for KPI cards, charts, dashboard cards, trend panels, and data cockpit views.

Allowed through wrappers:

- `AuroraKpiGrid`
- `AuroraMetricCard`
- `AuroraChartCard`
- `AuroraAreaChart`
- `AuroraBarChart`
- `AuroraDonutChart`
- `AuroraTrendCard`
- `AuroraInsightPanel`

Avoid direct page imports such as:

```tsx
import { Card, Text, Title } from "@tremor/react"
```

Prefer:

```tsx
import { AuroraChartCard, AuroraMetricCard } from "@auroramind/aurora-analytics"
```

If direct Tremor imports already exist, do not necessarily remove them in the first migration. Report them, group them, then replace them behind wrappers in a controlled PR.

## Kibo policy

Use Kibo for advanced UX where rebuilding logic would create repetitive code or inconsistent interactions.

Good candidates:

- command palette;
- combobox / smart select;
- tag input;
- stepper;
- resizable panels;
- code/snippet display;
- keyboard shortcuts;
- complex selectors.

Avoid making Kibo a second visual system. Wrap selected components behind `aurora-advanced`.

Prefer:

```tsx
import { AuroraCommandPalette, AuroraCombobox } from "@auroramind/aurora-advanced"
```

Do not import Kibo directly in final business pages unless the wrapper does not exist and the migration plan explicitly documents the exception.

## Integration rule

Tremor and Kibo are accelerators, not the product identity. The product identity is Aurora wrappers, page patterns, and AI/data workflow components.
