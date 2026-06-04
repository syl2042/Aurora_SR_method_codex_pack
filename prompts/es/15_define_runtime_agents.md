# Definir agentes IA runtime de aplicación

No codifiques.

Objetivo: proponer un mapa controlado de agentes IA runtime de aplicación sin activarlos.

Instrucciones:

1. Leer `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
2. Inspeccionar perfil del proyecto, skill map, docs de dominio, schemas, rutas, modelos DB y documentación RAG/KG si está disponible.
3. Proponer como máximo cinco agentes candidatos.
4. Para cada agente, definir purpose, función de negocio, contrato de prompt, bindings SQL/RAG controlados, runtime skills, modelos tipados de entrada/salida, fuente JSON schema, modo de validación, política de salida inválida, traces, tests, ubicación UI, riesgos y requisitos de validación humana.
5. Detenerse después de la propuesta y pedir validación.

Nunca permitas que un LLM genere y ejecute SQL libre. Las acciones críticas requieren validación humana.
