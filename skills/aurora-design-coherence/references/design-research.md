# Current design research protocol — V2.1

Use live external product-reference corpora to prevent stale, generic, or model-invented design decisions. Research supports the Design Director; it does not replace product reasoning.

## Preferred sources

1. **Refero MCP** — primary live source for Auroramind pilots.
2. **Mobbin MCP** — complementary breadth when connected.
3. Approved Aurora patterns.

Do not require both paid services for a task.

## Refero tool routing

For in-app product UI:

- `refero_search_screens` → concrete screen patterns;
- `refero_get_screen` → inspect strong candidates deeply;
- `refero_get_similar_screens` → expand from a particularly good match;
- `refero_get_screen_image` → inspect the raw screenshot only for shortlisted references when metadata is insufficient;
- `refero_search_flows` / `refero_get_flow` → multi-step journeys and state transitions;
- `refero_search_styles` / `refero_get_style` → visual language and craft, usually after information architecture is established.

For marketing or art-direction work, style research may precede screen research.

## Query construction

Search by user job and interaction pattern first.

Good screen queries:

- knowledge workspace with document sources citations and AI chat;
- enterprise SaaS data table with filters and contextual actions;
- document library with search filters status and detail panel;
- creation workflow with progressive disclosure;
- dense B2B settings with advanced configuration;
- multi-format content studio;
- AI assistant with sources and evidence;
- agent activity or run history.

Good flow queries:

- adding sources to knowledge workspace;
- creating document from AI response;
- publish content workflow;
- onboarding knowledge base;
- configuring advanced workspace settings.

Use aesthetic queries only when visual language is the question.

## Research depth

For a material screen:

1. establish the research question;
2. search at least 5 candidates when possible;
3. inspect 2–4 strong candidates in detail;
4. if one is unusually relevant, expand with `refero_get_similar_screens`;
5. research flows only when sequencing matters;
6. research styles when craft/visual language needs an external direction;
7. synthesize into a Reference Lock + Decision Ledger.

Load `references/research-contract.md` for the mandatory contract.

## Anti-copy and anti-averaging

- Extract design logic, not another product's identity.
- Do not clone wording, brand colors, iconography, or distinctive signature treatments.
- Do not average incompatible references into generic SaaS styling.
- Assign every retained reference a bounded role.
- Aurora product constraints and validated user intent override external references.

## Freshness

Treat design research as a live source. Re-query for significant redesigns rather than relying only on remembered examples or old static guidance.
