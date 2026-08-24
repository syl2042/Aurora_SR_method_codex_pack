# Codex New App UI Tasks - <App Name>

## 1. Objective

Create the initial UI foundation for <App Name> using Aurora design patterns. Build product structure first, not decorative mockups.

## 2. Non-goals

- Do not change backend contracts unless explicitly listed.
- Do not invent database models beyond placeholders requested by the user.
- Do not hardcode a fixed color theme.
- Do not add decorative animation to cockpit workflows.
- Do not create one-off replacements for existing Aurora components.

## 3. Inputs

- `APP_DESIGN_BRIEF.md`
- `APP_DESIGN_SYSTEM.md`
- `APP_SCREEN_BLUEPRINT.md`
- Existing repo conventions, if any

## 4. PR plan

### PR 1 - Shell and navigation

| Task | Files | Components | Tests |
|---|---|---|---|
| Create app shell |  | `AuroraAppShell`, `AuroraSidebar`, `AuroraTopbar` | build, responsive smoke test |

### PR 2 - Page skeletons

| Task | Files | Components | Tests |
|---|---|---|---|
| Add route pages |  | `AuroraPageHeader`, `AuroraSectionHeader`, `AuroraCard` | route smoke test |

### PR 3 - Lists, cards, and states

| Task | Files | Components | Tests |
|---|---|---|---|
| Add list/table structure |  | `AuroraDataTableShell`, `AuroraFilterBar`, `AuroraEmptyState` | empty/loading/error states |

### PR 4 - Analytics and dashboards

| Task | Files | Components | Tests |
|---|---|---|---|
| Add dashboard widgets |  | `AuroraKpiGrid`, `AuroraChartCard`, `AuroraInsightPanel` | no raw chart library leaks when wrappers exist |

### PR 5 - AI/data patterns

| Task | Files | Components | Tests |
|---|---|---|---|
| Add agent/source/run patterns |  | Tier 4 components | trace/evidence/HITL states |

### PR 6 - Visual QA

| Task | Files | Components | Tests |
|---|---|---|---|
| Fix visual inconsistencies |  | existing wrappers | responsive, theme, a11y smoke test |

## 5. Codex execution rules

- Implement one PR phase at a time.
- Keep business logic isolated.
- Preserve theme behavior.
- Use Aurora wrappers for product identity.
- Use shadcn/Radix as primitives, not the visible product API.
- Document any exception with path, reason, lifespan, replacement plan.

## 6. Acceptance checklist

- [ ] Shell consistent.
- [ ] Page headers consistent.
- [ ] Cards and metrics consistent.
- [ ] Lists/tables have states.
- [ ] Status badges standardized.
- [ ] AI/data patterns inspectable where relevant.
- [ ] Responsive behavior checked.
- [ ] Themes preserved.
- [ ] No business logic regression.
