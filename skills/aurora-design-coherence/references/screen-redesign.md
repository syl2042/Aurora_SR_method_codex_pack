# Screen redesign framework

A redesign is a product decision document, not a component shopping list.

## Required sequence

1. State the screen's job and primary decision/action.
2. Identify the current hierarchy and why it fails or succeeds.
3. Complete information triage.
4. Compare current patterns with relevant external/approved references.
5. Define target information architecture.
6. Define interaction/navigation behavior.
7. Define component mapping.
8. Define responsive and state behavior.
9. Define protected logic/non-goals.
10. Define measurable acceptance criteria.

## Target information architecture

Describe the order in which the user should encounter information, for example:

1. page identity + primary action;
2. business state or primary work object;
3. decision-supporting content;
4. contextual detail;
5. advanced/diagnostic access.

Avoid page designs whose hierarchy is effectively “header + grid of unrelated cards”.

## Component mapping

Only after information architecture is decided, map current → target components.

Example:

- repeated source cards → `AuroraDataTableShell` if comparison/filtering is the job;
- technical metadata card → `AuroraActionDrawer` or diagnostics panel;
- custom status chips → `AuroraStatusBadge`;
- persistent secondary controls → contextual menu or L1 drawer when frequency is low.

Use shadcn/Radix primitives directly when no Aurora wrapper defines product identity.

## Navigation decision

For each interaction decide one of:

- inline;
- popover/menu;
- drawer/sheet;
- dialog;
- dedicated page;
- advanced/diagnostics surface.

Choose based on task depth and continuity, not convenience for the developer.

## Reduction metric

Where the current interface is overloaded, record before/target estimates for:

- visible blocks/cards;
- immediately visible actions;
- technical fields at L0;
- competing primary-looking actions;
- navigation depth.

Reduction is not a goal by itself; reduction should improve task clarity without hiding frequently needed information.
