# Human validation gate

The human product owner is the final validator, not the manual designer.

## What the human receives

For a material redesign, show:

- current screenshot;
- target visual;
- concise explanation of the most important structural decisions;
- optionally the key trade-off if two directions remain plausible.

Do not require the human to inspect CSS, Figma layers, tokens, or component APIs.

## Approval states

Use exactly:

- `TARGET PROPOSED`
- `TARGET REVISION REQUESTED`
- `TARGET APPROVED`

Only explicit approval advances to implementation.

## Revision behavior

When feedback arrives:

1. update the redesign spec where the decision changed;
2. regenerate the target visual;
3. re-present only the meaningful changes;
4. do not modify production code during target iteration.

## Exception

If the human explicitly asks to skip the visual gate or directly implement a small visual correction, follow the request and record that the target gate was waived.
