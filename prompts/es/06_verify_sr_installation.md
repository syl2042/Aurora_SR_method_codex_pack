# Verificar una instalación SR Method

Estás trabajando en un repositorio equipado con la Aurora SR Method.

Objetivo: verificar que la instalación o upgrade esté completo, coherente y utilizable antes de retomar el desarrollo.

Instrucciones:

1. Ejecutar `python3 scripts/codex/verify_codex_pack.py`.
2. Ejecutar `python3 scripts/codex/audit_codex_pack.py --root . --json`.
3. Ejecutar `python3 scripts/codex/sr_post_install_check.py --root . --json` si está disponible.
4. Validar contratos lot, pass, loop y SR cuando existan los scripts.
5. Ejecutar `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` si existe `SR_PASSES.yaml`.
6. Clasificar warnings restantes como aceptables, a documentar, a corregir con validación o bloqueantes.
7. Reportar versión, verificaciones, errores, warnings, estado de `SR_PASSES.yaml` y próxima acción recomendada.

Esto no es una tarea de desarrollo de aplicación.
