# Codex UI Migration Skill

Use this reference when converting a design audit, design review, prototype, or new app blueprint into Codex tasks.

## Prime directive

Codex must improve UI coherence without breaking the product.

Do not change:

- business logic;
- API calls;
- auth flows;
- production routing;
- database models;
- data contracts;
- user-selectable theme behavior.

## Task format

Every Codex task must specify:

- objective;
- target files;
- allowed changes;
- forbidden changes;
- target Aurora components;
- required tests;
- visual QA checklist;
- rollback plan.

## Safe task size

Prefer one small phase per task:

1. shell/navigation;
2. page headers;
3. cards/metrics;
4. status badges;
5. tables/lists/filters;
6. drawers/dialogs;
7. analytics wrappers;
8. AI product patterns;
9. visual QA cleanup.

Do not ask Codex to redesign the entire app in one task.

## Prototype intake rule

When using a generated prototype or screenshot:

- retain intent and hierarchy;
- discard raw implementation unless clean and compatible;
- map patterns to Aurora components;
- create missing kit components only when the pattern repeats or defines product identity.

## Acceptance criteria

A Codex UI task is complete only when:

- app builds;
- relevant tests pass or are documented as unavailable;
- responsive behavior is checked;
- no business logic regression is introduced;
- themes still work;
- exceptions are documented.
