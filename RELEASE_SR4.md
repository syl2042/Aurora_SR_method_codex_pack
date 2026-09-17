# SR 4.0.0 — progressive context and safer upgrades

Released on 2026-09-17.

- Smaller permanent instructions and explicit, progressive routing to canonical procedures.
- Content-based installation and upgrades, with previews, conflict detection, transaction backups and guarded restoration. A previous version number is not required; unknown customizations require reconciliation.
- Explicit session-resume selection and ambiguity handling, compact diagnostics and read-only requirement views.
- Installation, upgrade, verification and realignment prompts in English, French, German, Spanish and Portuguese.
- Existing SR Contract 3.1.0 / legacy 3.0.0 and Loop Contract 1.1 remain supported. Authorization, proof, completion and propagation requirements remain in place.

## Installation and upgrade

Use INSTALLATION.md or INSTALLATION.fr.md. Select the official v4.0.0 source explicitly and verify its metadata before applying it. Fresh projects follow prompts 00 -> 06; existing projects follow 05 -> 06 -> 07. Preview first, preserve local policies and open requirements, and require a green post-install check. Installing the method does not authorize application development.

## Qualification and limits

Release checkout qualification: 128 Python tests and 8 Node tests passed, including installation/upgrade fixtures, documentary regressions and the UI verification harness. Documentation, route and pack audits passed.

Static document-set measurements from the 3.7.0 baseline: approximately 62% less initial nontrivial context and 59% less resume context. Complete workflow savings vary; the declared agent workflow has a small regression (about 0.45%). These are character-based token estimates for selected documents, not measured model-session consumption, billing savings or App/CLI behavioral equivalence.

Publication does not upgrade any existing application, synchronize global skills or establish product/human acceptance for a deployment. Pilot real workflows before a broad rollout.
