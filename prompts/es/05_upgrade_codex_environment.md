# Actualizar un proyecto a la SR Method más reciente

Estás trabajando en un repositorio que ya tiene una versión antigua de la Aurora SR Method.

Objetivo: auditar y actualizar el SR pack sin modificar código de aplicación ni sobrescribir adaptaciones del proyecto.

Usa el paquete fuente oficial:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Instrucciones:

1. Detectar la versión SR instalada.
2. Verificar o clonar el paquete fuente oficial.
3. Identificar archivos del proyecto a preservar: `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `docs/codex/tasks/`, skills del proyecto y decisiones locales.
4. Preservar `SR_LOTS.yaml` y agregar `SR_PASSES.yaml` de forma aditiva si falta, sin convertir automáticamente lotes antiguos ni task memories.
5. No convertir masivamente lotes antiguos para agregar `design_evidence`; agregar Lot Design Evidence Gate solo a lotes creados, promovidos o retomados despues del upgrade.
6. Explicar el plan de upgrade y esperar validación explícita antes de mutación.
7. Aplicar el upgrade con el instalador solo después de validación.
8. Ejecutar scripts de auditoría y validación, incluido `validate_pass_contract.py` si existe `SR_PASSES.yaml`.
9. Reportar commit fuente, archivos actualizados, archivos preservados, backups, warnings, estado de `SR_PASSES.yaml` y próximos pasos.
10. Recomendar `prompts/es/09_define_sr_lots_from_scope.md` para crear o promover lotes con Lot Design Evidence Gate antes de ejecutar.
11. Recomendar `prompts/es/08_define_sr_passes_from_lots.md` si el proyecto tiene varios lotes y ninguna pasada válida.

No modifiques código de aplicación, dependencias, migraciones ni secretos.
