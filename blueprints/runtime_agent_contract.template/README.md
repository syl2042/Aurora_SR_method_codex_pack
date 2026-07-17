# Runtime Agent Contract Template

This blueprint describes an application runtime AI agent before implementation.
It is intentionally framework-agnostic: the same contract can be implemented
with a single LLM call, a custom backend service, an agent SDK, or a workflow
framework.

Core rule:

```text
The prompt is not the source of truth.
The source of truth is the runtime contract validated by the application.
```

Use `agent_contract.yaml` to define:

- the bounded product action served by the agent;
- the stable internal representation it reads or writes;
- typed input and output contracts;
- the prompt contract and message builder;
- tools versus committing actions;
- routing and fallback policy;
- validation, failure and human-review policies;
- traces and tests required before activation.
