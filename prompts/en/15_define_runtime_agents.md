# Define application runtime agents

Do not code.

Objective: propose a controlled map of application runtime AI agents without activating them.

Instructions:

1. Read `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
2. Inspect project profile, skill map, domain docs, schemas, routes, database models, and RAG/KG documentation if available.
3. Propose at most five candidate agents.
4. For each agent, define purpose, business function, prompt contract, controlled SQL/RAG bindings, runtime skills, typed input/output models, JSON schema source, validation mode, invalid output policy, traces, tests, UI placement, risks, and human validation requirements.
5. Stop after the proposal and ask for validation.

Never let an LLM generate and execute free SQL. Critical actions require human validation.
