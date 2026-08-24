# Codex implementation handoff V2

Codex implements an approved design contract.

## Required inputs

- `TARGET APPROVED` visual;
- `SCREEN_REDESIGN_SPEC.md`;
- target repo/ref;
- target files/components;
- allowed and forbidden changes;
- tests and QA criteria.

## Prime directive

Do not ask Codex to “modernize”, “make premium”, “clean up”, or decide the UX. Replace subjective prompts with explicit target behavior.

## Task rules

Every task states:

- objective;
- target files;
- exact structural changes;
- current → target component mapping;
- what moves/hides/removes;
- responsive behavior;
- preserved states;
- protected business logic;
- tests;
- screenshot requirements;
- rollback guidance when risk is non-trivial.

## Protected areas

Unless explicitly approved, do not change:

- business logic;
- API contracts;
- database models;
- authentication/authorization;
- route semantics;
- data meaning;
- user-selectable themes.

## Deviation rule

If the approved design is technically impossible or conflicts with product behavior, stop that part, identify the exact conflict, and propose the smallest design adjustment. Do not silently reinterpret the target.
