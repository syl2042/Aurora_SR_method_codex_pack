# Migration rules

## Non-negotiables

- Preserve business logic, API calls, auth flows, route behavior, and data models.
- Preserve the user-selectable theme system. Do not hardcode a new Auroramind color theme.
- Prefer incremental PRs over broad redesigns.
- Never replace an app's working UI library wholesale.
- Document exceptions in the migration report.

## Migration order

1. **Shell**: align app shell, sidebar, topbar, user menu, app switcher, settings/support links.
2. **Page headers**: replace local headers with `AuroraPageHeader`.
3. **Sections**: use `AuroraSectionHeader` and `AuroraCard` for consistent hierarchy.
4. **Metrics**: replace local KPI/metric cards with `AuroraMetricCard` or analytics wrappers.
5. **Status**: replace custom status badges with `AuroraStatusBadge`.
6. **Lists/tables**: wrap with `AuroraDataTableShell`, `AuroraFilterBar`, pagination and empty states.
7. **Drawers/dialogs**: use `AuroraActionDrawer` and `AuroraConfirmDialog` for right-side workflows and critical actions.
8. **Analytics**: encapsulate Tremor in `aurora-analytics` wrappers.
9. **Advanced UX**: encapsulate Kibo in `aurora-advanced` wrappers.
10. **AI patterns**: add source/agent/trace/evidence/HITL components only where relevant.

## Migration plan format

For each proposed change, specify:

- target files;
- current pattern;
- target Aurora component;
- risk level;
- expected visual impact;
- whether it requires a kit update first;
- test checklist.

## Safe first PRs

Good first PRs are:

- add `AURORA_DESIGN_AUDIT.md`;
- add `aurora.config.ts` if missing;
- replace duplicated page headers;
- wrap local metric cards;
- standardize empty states;
- standardize status badges.

Avoid first PRs that:

- rewrite routing/layout from scratch;
- replace all table implementations at once;
- change theme tokens;
- introduce animation libraries;
- mix marketing blocks into production cockpits.
