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
4. Explicar el plan de upgrade y esperar validación explícita antes de mutación.
5. Aplicar el upgrade con el instalador solo después de validación.
6. Ejecutar scripts de auditoría y validación.
7. Reportar commit fuente, archivos actualizados, archivos preservados, backups, warnings y próximos pasos.

No modifiques código de aplicación, dependencias, migraciones ni secretos.
