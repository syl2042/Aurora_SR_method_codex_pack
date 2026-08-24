# Define application runtime agents

Do not code.

Objective: propose a controlled map of application runtime AI agents without activating them.

Instructions:

1. Read `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
2. Inspect project profile, skill map, domain docs, schemas, routes, database models, and RAG/KG documentation if available.
3. Propose at most five candidate agents.
4. For each agent, define `agent_key`, `runtime_shape` (`micro_agent`, `workflow_agent`, `delegation_agent`, or `mini_agent`), bounded product action, stable internal representation, business function, prompt contract, user message builder, controlled SQL/RAG bindings, runtime skills, tools/actions, routing/fallback, typed input/output models, JSON schema source, validation mode, invalid output policy, traces, tests, UI placement, risks, and human validation requirements.
5. Stop after the proposal and ask for validation.

Constraints:
- the method is framework-, provider-, domain-, and UI-agnostic;
- the prompt is not the source of truth, but a projection of the runtime contract;
- distinguish inspection/preparation tools from committing actions;
- no agent is active before validation.

Require an explicit `output schema`, Pydantic models for Python application-consumed output (or an equivalent strict typed validator elsewhere), and an `invalid_output_policy` such as reject, retry once, traced repair, or human review. Invalid output must never trigger a critical action.

Never let an LLM generate and execute free SQL. Critical actions require human validation.
