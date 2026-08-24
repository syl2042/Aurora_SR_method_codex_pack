# Definir agentes IA runtime de aplicación

No codifiques.

Objetivo: proponer un mapa controlado de agentes IA runtime de aplicación sin activarlos.

Instrucciones:

1. Leer `docs/codex/AI_AGENT_RUNTIME_METHOD.md`.
2. Inspeccionar perfil del proyecto, skill map, docs de dominio, schemas, rutas, modelos DB y documentación RAG/KG si está disponible.
3. Proponer como máximo cinco agentes candidatos.
4. Para cada agente, definir `agent_key`, `runtime_shape` (`micro_agent`, `workflow_agent`, `delegation_agent` o `mini_agent`), acción de producto acotada, representación interna estable, función de negocio, contrato de prompt, user message builder, bindings SQL/RAG controlados, runtime skills, tools/actions, routing/fallback, modelos tipados de entrada/salida, fuente JSON schema, modo de validación, política de salida inválida, traces, tests, ubicación UI, riesgos y requisitos de validación humana.
5. Detenerse después de la propuesta y pedir validación.

Restricciones:
- el método es agnóstico de frameworks, providers, dominios y UI;
- el prompt no es la fuente de verdad, sino una proyección del contrato runtime;
- distinguir tools de inspección/preparación y acciones comprometedoras;
- ningún agente queda activo sin validación.

Exigir un `output schema`, modelos Pydantic para salidas consumidas por aplicaciones Python (o un validador tipado estricto equivalente) y una `invalid_output_policy` de rechazo, retry unico, reparacion trazada o revision humana. Una salida invalida nunca puede activar una accion critica.

Nunca permitas que un LLM genere y ejecute SQL libre. Las acciones críticas requieren validación humana.
