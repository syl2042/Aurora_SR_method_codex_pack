# Report templates

## AURORA_DESIGN_AUDIT.md

```markdown
# Aurora Design Audit — <App Name>

## 1. Executive summary

**Score:** XX / 100
**Level:** weak / acceptable / good / premium
**Main risk:** <one sentence>
**Recommended next step:** <one action>

## 2. Scope and evidence

- Repository:
- Branch/ref:
- Date:
- Files inspected:
- Scripts run, if any:

## 3. Stack and UI inventory

| Area | Detected | Notes |
|---|---|---|
| Framework |  |  |
| Routing |  |  |
| shadcn/Radix |  |  |
| Tremor |  |  |
| Kibo |  |  |
| Theme system |  |  |
| Shared UI |  |  |
| Chart libraries |  |  |
| Animation libraries |  |  |

## 4. Scorecard

| Area | Score / 10 | Findings |
|---|---:|---|
| Shell and navigation |  |  |
| Page headers and hierarchy |  |  |
| Cards, metrics, and KPIs |  |  |
| Tables, lists, filters |  |  |
| Badges and status language |  |  |
| Analytics/dashboard quality |  |  |
| Advanced UX |  |  |
| AI/data patterns |  |  |
| Theme/token discipline |  |  |
| Technical maintainability |  |  |

## 5. Component coherence matrix

| Current component/pattern | Files/examples | Issue | Target Aurora component | Priority |
|---|---|---|---|---|

## 6. Page-pattern coherence

| Page type | Current state | Gap | Recommendation |
|---|---|---|---|
| Dashboard |  |  |  |
| List/table |  |  |  |
| Detail |  |  |  |
| Settings |  |  |  |
| Source/data |  |  |  |
| Agent/trace/HITL |  |  |  |

## 7. Tremor / Kibo / shadcn review

## 8. Premium B2B gaps

## 9. Quick wins

1.
2.
3.

## 10. Migration backlog

| Priority | Task | Risk | Expected impact |
|---|---|---|---|

## 11. Components to extract or add to aurora_kits_modules

## 12. Final recommendation
```

## AURORA_DESIGN_MIGRATION_PLAN.md

```markdown
# Aurora Design Migration Plan — <App Name>

## 1. Objective

## 2. Non-goals

- No color theme redesign.
- No business logic rewrite.
- No API/auth/database changes unless explicitly listed.

## 3. Migration phases

### Phase 1 — Low-risk unification

| Task | Files | Target component | Tests |
|---|---|---|---|

### Phase 2 — Analytics and tables

| Task | Files | Target component | Tests |
|---|---|---|---|

### Phase 3 — AI/product patterns

| Task | Files | Target component | Tests |
|---|---|---|---|

## 4. Required updates to aurora_kits_modules

## 5. Risks and rollback

## 6. Acceptance checklist

- [ ] App shell consistent
- [ ] Page headers consistent
- [ ] KPI cards consistent
- [ ] Status badges consistent
- [ ] Tables/lists consistent
- [ ] Tremor wrapped where applicable
- [ ] Kibo wrapped where applicable
- [ ] Themes preserved
- [ ] No business logic regression
```
