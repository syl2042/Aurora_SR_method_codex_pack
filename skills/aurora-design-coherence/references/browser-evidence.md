# Browser evidence protocol

Use rendered evidence whenever the environment provides a browser or Playwright capability.

## Preferred evidence order

1. rendered live/dev application with target persona;
2. rendered local application;
3. supplied screenshots/video;
4. source code plus styles;
5. verbal description only.

Never label a code-only judgment as visually observed.

## Auroramind Codex setup

When Codex App has Remote SSH access to the OVH host and a Playwright MCP/browser server is available:

- inspect code on the remote repository;
- inspect the deployed/dev app through its normal HTTPS URL when reachable;
- use the existing authenticated browser/session when possible;
- do not add an SSH tunnel merely for UI inspection if the app is already reachable over HTTPS;
- do not bypass Authentik/OAuth security controls.

If authentication requires human action, ask the human to complete the legitimate login/MFA in the controlled browser, then continue from the authenticated session. Do not request passwords in prompts or persist secrets in project files.

## Capture set

For each material screen, capture as relevant:

- desktop current state (prefer 1440x900 or the product's reference viewport);
- mobile current state (prefer 390x844 for responsive products);
- important open state such as drawer/dialog/menu when it affects the redesign;
- empty/loading/error/permission state when available or safely reproducible.

Record route, persona, viewport, and state next to evidence.

## Evidence language

Use precise qualifiers:

- `Observed (rendered)` — visually inspected.
- `Observed (measured)` — measured in rendered UI.
- `Observed (code)` — found in source/config.
- `Observed (design reference)` — found in Refero/Mobbin/reference artifact.
- `Inferred` — plausible but not directly observed.

Do not inflate confidence to make the report look complete.
