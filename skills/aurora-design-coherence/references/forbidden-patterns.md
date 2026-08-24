# Forbidden and discouraged patterns

## Forbidden in operational B2B product screens

- Letting the coding agent redesign an already human-approved target.
- Showing information merely because the backend/API provides it.
- Exposing UUIDs, raw provider configuration, collection IDs, debug payloads, or logs at normal-work level without a persona/job justification.
- Using card grids as the default answer to heterogeneous information.
- Creating a new sidebar when `AuroraAppShell` / `AuroraSidebar` can be used.
- Creating a new page header when `AuroraPageHeader` can be used.
- Creating custom KPI cards when Aurora metric wrappers fit.
- Creating custom status badges when `AuroraStatusBadge` fits.
- Importing Tremor/Kibo directly in final pages after Aurora wrappers exist.
- Hardcoding semantic colors instead of theme tokens or tone/status props.
- Adding marketing heroes, decorative 3D/glow/glass effects, or purposeless motion inside operational workflows.
- Changing user-selectable theme behavior without explicit request.
- Generating fake metrics/data to make a dashboard appear more complete.
- Copying another product's brand identity from Refero/Mobbin references.

## Discouraged unless justified

- One-off local components for repeated shells, tables, statuses, filters, empty states, and drawers.
- Large one-shot UI rewrites.
- Multiple equally prominent primary actions.
- Persistent advanced settings that are used rarely.
- Duplicated explanatory text around self-evident controls.
- Dense dashboard decoration above the actual work object.
- Multiple chart libraries without a reason.

## Exception rule

Document exceptions with file/path, reason, persona/job justification, expected lifespan, and follow-up/replacement plan.
