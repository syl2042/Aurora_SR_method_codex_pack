# App Screen Blueprint - <App Name>

## 1. Global shell

| Element | Component | Notes |
|---|---|---|
| App shell | `AuroraAppShell` |  |
| Sidebar | `AuroraSidebar` |  |
| Topbar | `AuroraTopbar` |  |
| Theme switcher | `AuroraThemeSwitcher` |  |

## 2. Routes and screens

| Route | Screen | Purpose | Components | Data objects |
|---|---|---|---|---|
| `/` | Dashboard |  |  |  |
| `/items` | List |  |  |  |
| `/items/[id]` | Detail |  |  |  |
| `/settings` | Settings |  |  |  |

## 3. Dashboard blueprint

- `AuroraPageHeader`
- `AuroraKpiGrid`
- `AuroraChartCard`
- `AuroraInsightPanel`
- `AuroraStatusRail`

## 4. List page blueprint

- `AuroraPageHeader`
- `AuroraFilterBar`
- `AuroraDataTableShell`
- `AuroraEmptyState`
- `AuroraActionDrawer`

## 5. Detail page blueprint

- `AuroraPageHeader`
- `AuroraSectionHeader`
- `AuroraCard`
- `AuroraStatusBadge`
- `AuroraActionDrawer`

## 6. AI/data screen blueprint

Use only if relevant.

- `AuroraSourceCard`
- `AuroraConnectorCard`
- `AuroraAgentCard`
- `AuroraAgentRunTimeline`
- `AuroraTraceDrawer`
- `AuroraToolCallViewer`
- `AuroraEvidencePanel`
- `AuroraCitationList`
- `AuroraHumanValidationPanel`
- `AuroraKnowledgeGraphPreview`
- `AuroraPublicationStatus`

## 7. State matrix

| Screen | Empty | Loading | Error | Permission | Partial data |
|---|---|---|---|---|---|
| Dashboard |  |  |  |  |  |
| List |  |  |  |  |  |
| Detail |  |  |  |  |  |

## 8. Implementation order

1. Shell and navigation.
2. Page headers and static screen skeletons.
3. Cards, tables, empty states.
4. Data binding without changing contracts.
5. AI/data patterns.
6. Responsive and visual QA.
