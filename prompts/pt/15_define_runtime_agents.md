# Definir agentes IA runtime da aplicação

Não codifique.

Objetivo: propor um mapa controlado de agentes IA runtime da aplicação sem ativá-los.

Instruções:

1. Ler `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
2. Inspecionar perfil do projeto, skill map, docs de domínio, schemas, rotas, modelos DB e documentação RAG/KG se disponível.
3. Propor no máximo cinco agentes candidatos.
4. Para cada agente, definir purpose, função de negócio, contrato de prompt, bindings SQL/RAG controlados, runtime skills, modelos tipados de entrada/saída, fonte do JSON schema, modo de validação, política de saída inválida, traces, testes, posição UI, riscos e requisitos de validação humana.
5. Parar após a proposta e pedir validação.

Nunca permita que um LLM gere e execute SQL livre. Ações críticas exigem validação humana.
