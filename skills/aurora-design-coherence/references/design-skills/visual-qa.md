# Visual QA Skill

Use this reference after Codex implements a UI task or when reviewing a PR.

## Review levels

### Level 1: structural QA

- Shell/navigation is stable.
- Page headers follow the agreed structure.
- Sections have clear hierarchy.
- Primary actions are visible and predictable.
- Empty/loading/error states exist.

### Level 2: component QA

- Cards are consistent.
- Metric cards use the approved pattern.
- Status badges use standard language and tokens.
- Tables/lists have search/filter/pagination where needed.
- Drawers/dialogs follow Aurora behavior.
- Direct Tremor/Kibo imports are wrapped when wrappers exist.

### Level 3: theme and accessibility QA

- Theme switcher behavior is preserved.
- Hardcoded semantic colors are avoided.
- Focus states are visible.
- Contrast is acceptable.
- Keyboard navigation is not broken.
- Responsive layouts do not overflow.

### Level 4: AI/data QA

- Sources, citations, evidence, runs, traces, and HITL states are inspectable.
- No fake AI magic replaces explainability.
- Errors and uncertain states are visible.
- Publication or deployment states are explicit.

## Output

Produce:

- pass/fail summary;
- blocking issues;
- non-blocking improvements;
- screenshots or files inspected if available;
- recommended next Codex task.
