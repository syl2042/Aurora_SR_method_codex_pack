# Define SR Passes From Existing Lots

You are working in a repository already equipped with the SR Method.

Objective: propose or update `docs/codex/SR_PASSES.yaml` from `docs/codex/SR_LOTS.yaml`, without modifying application code.

Prioritize `repair`/`reopened` lots, preserve every open `validated_request_id`, and consolidate repairs from the same product scope into one coherent pass.

Rules:

- Do not modify application code.
- Do not change any lot status without evidence and validation.
- Do not mark a pass `validated` without explicit user validation.
- A pass groups lots; it never replaces lot criteria or gates.

Sources to read:

1. `AGENTS.md`
2. `docs/codex/SR_HARNESS_METHOD.md`
3. `docs/codex/LOT_EXECUTION_METHOD.md`
4. `docs/CURRENT_STATE.md`
5. `docs/codex/SR_LOTS.yaml`
6. `docs/codex/SR_PASSES.yaml` if present
7. `docs/codex/CODEBASE_MAP.md`

Method:

1. Validate `SR_LOTS.yaml`.
2. Classify lots by status and dependencies.
3. Check the Lot Design Evidence Gate: exclude from executable passes any `planned`, `validated`, `in_progress`, `repair`, or `reopened` lot without `design_evidence.status: pass` or a justified `not_applicable`. A `proposed` lot may remain exploratory.
4. Build the `depends_on`, `blocked_by`, `impacts`, `impacted_by` graph.
5. Propose passes with order, rationale, preflight, human validations, migrations/external actions, shared sources, grouped E2E, and stop conditions.
6. Create or update `SR_PASSES.yaml` only after validation if the project enforces strict validation.
7. Validate with `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml`.

Expected output:

- proposed passes;
- excluded lots and reason;
- lots excluded because the Lot Design Evidence Gate is missing or incomplete;
- blocking questions;
- preflight per pass;
- recommended grouped E2E;
- modified SR files;
- validation result;
- recommended next pass.
