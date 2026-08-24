# Product intent model

Use before redesigning any screen.

## Screen contract

For each screen, state:

- **Persona** — who is using it now, with what level of expertise.
- **Job to be done** — what outcome they came to achieve.
- **Primary question/decision** — what they must understand or decide.
- **Primary action** — the action that completes or advances the job.
- **Secondary actions** — useful but not dominant.
- **Frequency** — many times/day, weekly, rare setup, exception handling.
- **Business criticality** — cost of misunderstanding or error.
- **Required information** — minimum evidence needed to decide/act.
- **Expert-only information** — useful to admins/support/developers but not required in the normal path.

## Design test

A screen is structurally weak when any of these are true:

- the primary action is visually weaker than secondary controls;
- the user must understand implementation details to complete a business task;
- the first viewport explains the system rather than the user's work;
- multiple unrelated jobs compete at the same hierarchy level;
- the screen is organized around backend entities rather than user decisions;
- every capability is visible because it exists.

## Decision rule

When product intent and component consistency conflict, fix product intent first. A perfectly consistent bad workflow is still bad UX.
