# App Design System - <App Name>

## 1. Design promise

Describe the product feeling in operational terms: trust, clarity, speed, control, explainability, density.

## 2. Theme policy

- Preserve user-selectable themes.
- Do not hardcode a fixed brand recolor unless explicitly approved.
- Express status through tone/status props.
- Use tokens for surfaces, borders, text, muted text, destructive, warning, success, info.

## 3. Layout language

- Shell:
- Sidebar:
- Topbar:
- Page header:
- Section header:
- Card density:
- Page max width:
- Spacing rhythm:

## 4. Component selection

### Tier 1 - Core B2B

- `AuroraAppShell`
- `AuroraSidebar`
- `AuroraTopbar`
- `AuroraPageHeader`
- `AuroraSectionHeader`
- `AuroraCard`
- `AuroraMetricCard`
- `AuroraStatusBadge`
- `AuroraDataTableShell`
- `AuroraEmptyState`
- `AuroraActionDrawer`
- `AuroraFilterBar`
- `AuroraThemeSwitcher`

### Tier 2 - Analytics / dashboard

List selected analytics components.

### Tier 3 - Advanced UX

List selected advanced UX components.

### Tier 4 - AI product patterns

List selected AI/data components.

### Tier 5 - Marketing/onboarding only

List selected marketing components, if any.

## 5. Page patterns

| Page type | Structure | Required states |
|---|---|---|
| Dashboard |  | empty/loading/error/partial |
| List |  | empty/loading/error/filter zero-result |
| Detail |  | loading/error/missing item |
| Settings |  | validation/saved/error |
| AI run/trace |  | pending/running/success/error/retry |

## 6. Cards and metrics

- Card anatomy:
- Metric anatomy:
- Trend display:
- Helper text:
- Empty card behavior:

## 7. Tables, lists, filters

- Toolbar rules:
- Search/filter rules:
- Pagination rules:
- Empty state rules:
- Bulk action rules:

## 8. Status language

| Meaning | Label | Tone | Notes |
|---|---|---|---|
| Active | Active | success |  |
| Pending | Pending | warning |  |
| Failed | Failed | destructive |  |
| Draft | Draft | muted |  |

## 9. AI/data patterns

- Sources:
- Agents:
- Runs:
- Tool calls:
- Evidence:
- Citations:
- HITL:
- Publication:

## 10. Responsive rules

- Mobile:
- Tablet:
- Desktop:
- Overflow:
- Touch targets:

## 11. Forbidden patterns

- No decorative marketing motion in cockpit workflows.
- No one-off common shell/header/card/table components.
- No raw Tremor/Kibo imports in final pages after wrappers exist.
- No hardcoded semantic colors.
- No route/API/auth/data model changes for UI work.

## 12. Codex implementation notes

- Build incrementally.
- Keep business logic unchanged.
- Use Aurora wrappers for product identity.
- Document exceptions.
