# Aurora component tiers

## Tier 1 — Core B2B, mandatory in apps

Use these for every Auroramind webapp/cockpit unless a repo has a documented exception.

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

## Tier 2 — Analytics / dashboard

Use for data-heavy pages and management cockpits.

- `AuroraKpiGrid`
- `AuroraChartCard`
- `AuroraAreaChart`
- `AuroraBarChart`
- `AuroraDonutChart`
- `AuroraTrendCard`
- `AuroraScoreGauge`
- `AuroraInsightPanel`
- `AuroraStatusRail`

## Tier 3 — Advanced UX

Use for productivity interactions that would otherwise be fragile or duplicated.

- `AuroraCommandPalette`
- `AuroraCombobox`
- `AuroraSmartSelect`
- `AuroraTagInput`
- `AuroraStepper`
- `AuroraResizablePanels`
- `AuroraKeyboardShortcuts`
- `AuroraCodeBlock`

## Tier 4 — AI product patterns

Use where apps expose sources, agents, traces, RAG, evidence, citations, MCP/API publication, or HITL flows.

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

## Tier 5 — Marketing/onboarding only

Use only for landing pages, product tours, login, onboarding, or website sections.

- `AuroraHero`
- `AuroraBentoGrid`
- `AuroraLogoCloud`
- `AuroraFeatureGrid`
- `AuroraPricingSection`
- `AuroraTestimonialSection`
- `AuroraAnimatedBackground`

## Decision rule

If a component appears in three apps or in three pages of the same app, promote it to the kit or document why it remains local.
