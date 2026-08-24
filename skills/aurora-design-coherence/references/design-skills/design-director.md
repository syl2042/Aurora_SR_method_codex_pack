# Design Director Review

Use this reference when reviewing a screenshot, prototype, generated UI, page, component, or visual direction.

## Goal

Judge whether the UI creates premium B2B trust and can be safely converted into Aurora patterns. This is not a beauty contest. Prefer clarity, hierarchy, density control, and maintainability over novelty.

## Review dimensions

1. **Product trust**: does the UI feel reliable enough for a business workflow?
2. **Hierarchy**: are primary actions, page title, data, and secondary actions clear?
3. **Density**: is the page readable without being empty or decorative?
4. **Navigation**: does the user know where they are and what to do next?
5. **Component coherence**: are cards, tables, badges, filters, and drawers structurally consistent?
6. **Status language**: are states explicit, stable, and token-friendly?
7. **Accessibility**: contrast, focus, keyboard, size, readable labels.
8. **Maintainability**: can the UI become reusable components, or is it one-off visual code?
9. **AI slop detection**: generic gradients, fake metrics, decorative noise, random icons, overused glassmorphism, arbitrary shadows, inconsistent spacing, and meaningless microcopy.
10. **Aurora fit**: can the retained idea map to Aurora component tiers?

## Output pattern

Produce:

- Summary verdict: keep / revise / reject / extract pattern.
- What works.
- What weakens premium B2B trust.
- What to remove.
- What to map to Aurora components.
- Risk if implemented as-is.
- Codex-ready next step.

## Hard rejection signals

Reject or heavily revise when the UI:

- uses marketing hero patterns inside operational workflows;
- hardcodes semantic colors instead of tone/status props;
- hides the main action behind decorative layout;
- uses fake data structure that does not match product flows;
- creates components that cannot be reused;
- changes theme behavior;
- clones another brand identity too closely;
- adds animation to core business actions without purpose.
