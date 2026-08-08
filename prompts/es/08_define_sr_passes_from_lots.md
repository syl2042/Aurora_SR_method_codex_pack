# Definir SR Passes desde lotes existentes

Estas trabajando en un repositorio ya equipado con la SR Method.

Objetivo: proponer o actualizar `docs/codex/SR_PASSES.yaml` a partir de `docs/codex/SR_LOTS.yaml`, sin modificar codigo de aplicacion.

Reglas:

- No modifiques codigo de aplicacion.
- No cambies ningun estado de lote sin evidencia y validacion.
- No marques una pasada como `validated` sin validacion explicita del usuario.
- Una pasada agrupa lotes; nunca reemplaza criterios o gates de los lotes.

Fuentes a leer:

1. `AGENTS.md`
2. `docs/codex/SR_HARNESS_METHOD.md`
3. `docs/codex/LOT_EXECUTION_METHOD.md`
4. `docs/CURRENT_STATE.md`
5. `docs/codex/SR_LOTS.yaml`
6. `docs/codex/SR_PASSES.yaml` si existe
7. `docs/codex/CODEBASE_MAP.md`

Metodo:

1. Validar `SR_LOTS.yaml`.
2. Clasificar lotes por estado y dependencias.
3. Verificar el Lot Design Evidence Gate: excluir de pasadas ejecutables cualquier lote `planned`, `validated`, `in_progress` o `reopened` sin `design_evidence.status: pass` o `not_applicable` justificado. Un lote `proposed` puede seguir exploratorio.
4. Construir el grafo `depends_on`, `blocked_by`, `impacts`, `impacted_by`.
5. Proponer pasadas con orden, rationale, preflight, validaciones humanas, migraciones/acciones externas, fuentes compartidas, E2E agrupado y stop conditions.
6. Crear o actualizar `SR_PASSES.yaml` solo despues de validacion si el proyecto impone validacion estricta.
7. Validar con `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml`.

Salida esperada:

- pasadas propuestas;
- lotes excluidos y razon;
- lotes excluidos por Lot Design Evidence Gate ausente o incompleto;
- preguntas bloqueantes;
- preflight por pasada;
- E2E agrupado recomendado;
- archivos SR modificados;
- resultado de validacion;
- siguiente pasada recomendada.
