# Codex UI Task - <App Name>

## 1. Objective

Apply one approved UI coherence task from the audit or migration plan.

## 2. Scope

**Phase:**  
**Target files:**  
**Target pages/components:**  
**Target Aurora components:**  

## 3. Allowed changes

- UI structure for the listed files.
- Component replacement with approved Aurora wrappers.
- Styling cleanup through theme tokens and component props.
- Local refactor only when needed to preserve behavior.

## 4. Forbidden changes

- No business logic rewrite.
- No API contract changes.
- No auth changes.
- No database/model changes.
- No route behavior changes unless explicitly approved.
- No theme system replacement.
- No decorative motion in cockpit workflows.

## 5. Implementation steps

1. Inspect current files.
2. Identify existing local patterns.
3. Replace only the approved pattern.
4. Keep props/data flow intact.
5. Run build/tests/lint where available.
6. Update exception notes if needed.

## 6. Test checklist

- [ ] Build passes.
- [ ] Existing page behavior preserved.
- [ ] Empty/loading/error states still work.
- [ ] Theme switcher still works.
- [ ] Responsive layout checked.
- [ ] No direct Tremor/Kibo imports introduced where wrappers exist.
- [ ] No hardcoded semantic colors introduced.

## 7. Rollback plan

Describe the minimal files to revert if the change creates regression.
