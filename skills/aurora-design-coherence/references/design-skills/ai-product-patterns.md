# AI Product Patterns

Use for products exposing RAG, knowledge sources, agents, traces, citations, evidence, HITL, MCP/API publication, runs, evaluations, or automations.

## Principle

AI interfaces must be trustworthy and inspectable, but **inspectable does not mean permanently visible**. Apply persona/job analysis and information triage before exposing technical metadata.

## Sources and knowledge

Normal-work level usually favors:

- source identity/title/type when useful;
- sync/indexing state in user language;
- recency when it affects trust;
- document/content count when decision-relevant;
- clear next action.

Move implementation details such as raw connector IDs, vector-store IDs, embedding/model configuration, ingestion internals, and logs to L2/L3 unless the persona needs them routinely.

Candidate components include `AuroraSourceCard`, `AuroraConnectorCard`, `AuroraDataTableShell`, and `AuroraKnowledgeGraphPreview`; choose the pattern based on the job. Use a table/list when comparison/filtering is the primary job rather than defaulting to cards.

## Agents

Normal-work views should emphasize role, scope, enabled capability, business state, latest meaningful activity, and human action. Provider/model/tool internals belong in advanced/diagnostics unless essential to the target user.

Candidate components: `AuroraAgentCard`, `AuroraPublicationStatus`, `AuroraActionDrawer`.

## Runs, traces, evidence

A traceability surface can expose timeline, tools, retrieved evidence, outputs, retries/errors, cost/latency, and human validation. Decide which belong at L0 versus a dedicated trace/detail surface.

Candidate components: `AuroraAgentRunTimeline`, `AuroraTraceDrawer`, `AuroraToolCallViewer`, `AuroraEvidencePanel`, `AuroraCitationList`, `AuroraHumanValidationPanel`.

## Human-in-the-loop

Make approve/reject/revise/assign/comment and audit trail explicit when they drive the workflow. Do not hide consequential human decisions behind generic menus.

## Anti-patterns

- magic chat bubbles with no evidence path;
- hidden uncertainty or publication state;
- source/evidence overload in the main reading path;
- developer terminology in user-facing status text;
- one-off UI per agent type;
- displaying every model/tool parameter as proof of “AI transparency”.
