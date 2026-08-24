# Product Cockpit Design Skill

Use this reference for SaaS dashboards, admin panels, management cockpits, internal tools, and vertical business apps.

## Intent

A cockpit is not a marketing page. It must help users understand state, decide, and act with confidence.

## Core layout rules

- Use a stable shell with sidebar/topbar/user menu/settings/support/app switcher when relevant.
- Use a consistent page header: title, description, primary action, secondary actions.
- Use sections with clear titles and scoped actions.
- Put primary work objects near the top, not decorative panels.
- Use cards to group decisions, not to create visual noise.
- Use tables and lists with filters, search, pagination, empty states, and bulk actions when needed.
- Use drawers for contextual actions and details that do not deserve full navigation.

## Dashboard rules

- KPIs must have consistent size, label, value, helper text, trend, and status logic.
- Charts must answer a business question and include a readable title and timeframe.
- Avoid dashboards that are only decoration above the real workflow.
- Use insight panels for interpreted signals, not random generated advice.

## State rules

Every cockpit page should handle:

- empty state;
- loading state;
- error state;
- partial data state;
- permission-denied state when relevant;
- disabled or pending actions.

## Motion rules

Use restrained motion only for orientation or feedback. Do not use decorative motion in operational dashboards.

## Codex guidance

When implementing a cockpit, first build:

1. shell;
2. page headers;
3. primary work pages;
4. reusable cards/tables/badges;
5. analytics wrappers;
6. advanced UX only when repeated.
