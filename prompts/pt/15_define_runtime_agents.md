# Definir agentes IA runtime da aplicação

Não codifique.

Objetivo: propor um mapa controlado de agentes IA runtime da aplicação sem ativá-los.

Instruções:

1. Ler `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
2. Inspecionar perfil do projeto, skill map, docs de domínio, schemas, rotas, modelos DB e documentação RAG/KG se disponível.
3. Propor no máximo cinco agentes candidatos.
4. Para cada agente, definir `agent_key`, `runtime_shape` (`micro_agent`, `workflow_agent`, `delegation_agent` ou `mini_agent`), ação de produto delimitada, representação interna estável, função de negócio, contrato de prompt, user message builder, bindings SQL/RAG controlados, runtime skills, tools/actions, routing/fallback, modelos tipados de entrada/saída, fonte do JSON schema, modo de validação, política de saída inválida, traces, testes, posição UI, riscos e requisitos de validação humana.
5. Parar após a proposta e pedir validação.

Restrições:
- o método é agnóstico de frameworks, providers, domínios e UI;
- o prompt não é a fonte da verdade, mas uma projeção do contrato runtime;
- distinguir tools de inspeção/preparação e ações comprometedoras;
- nenhum agente fica ativo sem validação.

Exigir um `output schema`, modelos Pydantic para saidas consumidas por aplicacoes Python (ou validador tipado estrito equivalente) e uma `invalid_output_policy` de rejeicao, retry unico, reparacao rastreada ou revisao humana. Uma saida invalida nunca pode acionar uma acao critica.

Nunca permita que um LLM gere e execute SQL livre. Ações críticas exigem validação humana.
