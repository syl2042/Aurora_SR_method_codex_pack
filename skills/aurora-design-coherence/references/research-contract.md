# Design Research Contract V2.1

Use this contract for every material redesign or new critical screen. It converts external inspiration into auditable product decisions.

## 1. Research question

State the product question before searching references.

Examples:

- How should a knowledge workspace expose sources, AI output, and citations without making technical metadata dominant?
- How should a multi-format content studio let a business user choose a deliverable without presenting a toolbox grid?
- How should an admin-heavy screen separate daily work from advanced configuration and diagnostics?

Do not search generic aesthetics until the product question is clear.

## 2. Research routing

For **in-app B2B product UI**, use this order:

1. `refero_search_screens` for concrete information architecture, hierarchy, interaction, and states.
2. `refero_get_screen` on promising candidates.
3. `refero_get_similar_screens` when one candidate strongly matches the problem.
4. `refero_search_flows` + `refero_get_flow` when the task spans several steps or state changes.
5. `refero_search_styles` + `refero_get_style` only after the product architecture is understood, when visual language, density, typography, surfaces, or craft direction need external evidence.

For **marketing pages, visual identity, or major art-direction work**, styles may come first, followed by screens/flows where relevant.

If Refero is unavailable, use Mobbin when connected. Otherwise use approved Aurora patterns and label the benchmark as limited.

## 3. Candidate set

For material redesigns, aim for at least 5 relevant candidates when the corpus supports it. Do not dump results into the final spec. Shortlist only the candidates that solve the actual user/job problem.

Record for each shortlisted candidate:

- source/product;
- screen/flow/style identifier or URL;
- problem solved;
- useful hierarchy/interaction/disclosure pattern;
- mismatch or risk;
- role in the final direction.

## 4. Reference Lock

Before creating the target, freeze the reference roles.

Use this structure:

```text
REFERENCE LOCK

Primary structural reference:
- [source]
- Preserve: [3–5 structural traits]

Secondary structural reference(s):
- [source]
- Borrow only: [specific bounded traits]

Visual/craft reference, if used:
- [source]
- Preserve: [density/type/surface/spacing/etc.]

Reject:
- [patterns that must not leak into the target]

Aurora constraints:
- [theme/component/brand/product constraints that override external references]
```

The lock prevents the renderer or implementer from drifting back to generic AI UI.

## 5. Anti-averaging rule

Do not average several strong references into a safe generic middle.

When references disagree:

1. choose one dominant structural direction for each major problem;
2. assign secondary references a narrow role;
3. keep source roles bounded;
4. explicitly reject conflicting traits.

Examples:

- A reference used for dense table behavior does not automatically own typography or color.
- A reference used for a contextual drawer does not justify copying its global shell.
- A style accent used for primary CTA must not become a generic status color.

## 6. Decision Ledger

Every major design decision must trace to one or more of:

- product intent;
- information triage;
- current rendered evidence;
- approved Aurora pattern;
- external screen/flow/style research;
- accessibility or platform constraint.

Use this table:

| Decision | Evidence/source | Source role | Why | Target consequence |
|---|---|---|---|---|

Examples:

| Move ingestion details to Diagnostics | Persona/job + current screenshot + 3 screened references | Product hierarchy | Normal user does not act on model/ID/log details | L3 diagnostics drawer |
| Keep source status in list row | Current job + screen references | Decision support | User must see whether source is usable | compact status badge at L0 |

A major choice with no evidence must be marked `UNSUPPORTED DECISION` and resolved before target approval.

## 7. Product/UX vs Visual Craft

Do not let visual polish hide a product-architecture problem.

Run two lenses separately:

### Product / UX Audit

Judge:

- persona/job fit;
- information priority;
- primary/secondary actions;
- navigation;
- progressive disclosure;
- workflow/state clarity;
- cognitive load;
- developer/admin leakage.

### Visual Craft Audit

Judge only after the product structure is credible:

- typography hierarchy;
- spacing rhythm;
- density consistency;
- surfaces/borders/elevation;
- iconography;
- alignment;
- motion;
- theme fidelity;
- perceived polish/trust.

A screen can pass craft and fail product UX. Product UX wins.

## 8. Research completion gate

Research is complete only when:

- the product question is explicit;
- the candidate set was broad enough for the risk;
- shortlisted references have bounded roles;
- the Reference Lock exists;
- the Decision Ledger covers all major structural decisions;
- no unsupported major decision remains;
- the target can be generated without asking the renderer to invent the design direction.
