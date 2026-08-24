# Instalar SR 3.7 en un proyecto destino nuevo

Objetivo verificable: instalar SR Pack 3.7.0 con `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 y `SR_PASSES` 0.2, verificarlo y detenerse antes de cualquier desarrollo de aplicación.

Instala `SR_PASSES.yaml` con `passes: []`. Este registro vacío es válido: una instalación nueva no debe inventar una pasada de producto. El prompt `08` propone las pasadas después de leer los lotes y obtener validación humana.

Usa únicamente `https://github.com/syl2042/Aurora_SR_method_codex_pack`.

Reglas estrictas:

- No modifiques código de aplicación, migraciones, dependencias, secretos, configuración ni reglas de negocio.
- Inspecciona primero el repositorio destino y el `AGENTS.md` más cercano.
- Si existe `docs/codex/SR_PACK_VERSION.json`, `docs/codex/SR_METHOD.md` o `docs/codex/SR_LOTS.yaml`, no es una instalación nueva. Detente y usa `05_upgrade_codex_environment.md`.
- Antes de mutar, informa de archivos nuevos, existentes y preservados, y de los controles previstos; espera la validación humana requerida.
- No inventes `validated_requests`, lotes validados ni pasadas ejecutables. Las plantillas no son alcance de producto validado.
- Nunca uses `--write` en un proyecto SR existente; usa `--upgrade` solo tras una auditoría por proyecto.

Tras la validación:

1. Registrar el clon local verificado y su commit; clasificar el destino como `fresh_install`.
2. Ejecutar el instalador con `--profile default --write`.
3. Verificar versión, lotes/pasadas, plantillas de tarea, validadores y prompts `01`, `05`, `06`, `07`, `08`, `09`.
4. Confirmar que `sr_contract.json` separa `implementation_status` y `evidence_status`, incluye `validated_requests` granulares y un Completion Gate derivado.
5. Verificar `CHANGELOG.md`, prompts publicos localizados y ejecutar `audit_codex_pack.py`, `sr_post_install_check.py`, `validate_release_docs.py` y los validadores de lote, pasada, loop y SR.
6. No generar `/goal`. Recomendar primero `09_define_sr_lots_from_scope.md` y después `08_define_sr_passes_from_lots.md`.
7. Informar clasificación, versión, commit, archivos, controles, warnings y confirmar que no cambió código de aplicación.

Final obligatorio: instalar el método no valida ningún alcance de producto.
