# Verificar una instalacion de SR Method

No modifiques archivos.

Objetivo: demostrar que cada instalacion o upgrade es completa, coherente y utilizable antes de reanudar el desarrollo aplicativo.

1. Leer los marcadores reales de `AGENTS.md`, `docs/codex/SR_PACK_VERSION.json`, metodo, contratos, lotes, pasadas y task memories. No inferir la version de una carpeta desde otra.
2. Ejecutar `python3 scripts/codex/verify_codex_pack.py`.
3. Ejecutar `python3 scripts/codex/validate_release_docs.py --root . --json`.
4. Ejecutar `python3 scripts/codex/audit_codex_pack.py --root . --json`.
5. Ejecutar `python3 scripts/codex/sr_post_install_check.py --root . --json`.
6. Ejecutar `python3 scripts/codex/audit_sr_task_contracts.py --root . --json`.
7. Validar `SR_LOTS.yaml`, `SR_PASSES.yaml`, loop contracts activos y el SR Contract 3.1.0 o contratos legacy 3.0.0 explicitamente identificados.
8. Verificar `docs/codex/CHANGELOG.md`, version objetivo, prompts publicos localizados y preservacion aditiva de archivos del proyecto.

Clasificar cada warning como estado legacy compatible, deuda documental, `repair` o bloqueo externo real. El codigo `0` del instalador no basta.

Informar por repositorio version, controles, errores, warnings, contratos, `validated_requests` abiertas, evidencias pendientes y siguiente accion. `user_testing` solo es valido para trabajo tecnicamente completo; implementacion faltante permanece `repair`.

Detenerse sin corregir y pedir validacion exacta para cualquier reparacion.
