# Premium B2B selection

## What premium B2B means for Auroramind

Premium B2B is not luxury decoration. It is operational trust. Favor:

- calm layouts;
- clear hierarchy;
- readable density;
- consistent spacing;
- predictable actions;
- strong data affordances;
- restrained motion;
- professional empty/loading/error states;
- standardized status language.

## Keep as primitives

Keep shadcn/Radix primitives as the internal foundation:

- button, card, badge, dialog, drawer/sheet, dropdown-menu, popover, tooltip, tabs;
- form, field, input, textarea, select, checkbox, switch, radio-group, calendar;
- table, pagination, command, sidebar, scroll-area, separator, skeleton, sonner.

Do not expose the primitive catalog as the main product API. Wrap identity-defining components in Aurora components.

## Promote to Aurora wrappers

Always prefer Aurora wrappers for:

- shell/navigation;
- page headers;
- section headers;
- KPI/metric cards;
- chart cards;
- tables/list shells;
- filter bars;
- status badges;
- empty states;
- action drawers;
- command palettes;
- agent/source/trace/evidence patterns.

## Use carefully

Use animated or decorative components only for:

- marketing website sections;
- login/onboarding screens;
- product empty states when subtle;
- demo/showcase pages.

Never make decorative animation central to a cockpit workflow.

## Good extraction candidates from existing apps

From Compta-IA style patterns, generalize:

- `ComptaPageHeader` → `AuroraPageHeader`;
- `ComptaSectionHeader` → `AuroraSectionHeader`;
- `ComptaMetricCard` → `AuroraMetricCard`;
- `ComptaChartCard` → `AuroraChartCard`;
- `ComptaDataTableShell` → `AuroraDataTableShell`;
- `ComptaActionDrawer` → `AuroraActionDrawer`;
- `ComptaEmptyState` → `AuroraEmptyState`;
- `ComptaStatusRail` → `AuroraStatusRail`;
- `ComptaStatusItem` → `AuroraStatusItem`.
