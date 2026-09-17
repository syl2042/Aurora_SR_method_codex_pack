# Instalar SR 4.0.0 en un proyecto destino nuevo

## SR 4.0.0 — version publicada

Fuente objetivo: seleccionar explicitamente `SR_PACK_SOURCE`, una version publicada identificada o el candidato local SR 4.0.0 autorizado. Leer `core/SR_PACK_VERSION.json` (`version`, `release_status`); registrar `source_commit`, estado Git y, si hay cambios locales, una huella del contenido que incluya los archivos fuente no seguidos utilizados. No presentar un candidato `unreleased` como release. No sustituir el candidato por un clon de la ultima version publicada; si falta la fuente solicitada, detenerse y aclarar antes de instalar.

Para este objetivo SR 4.0.0, la fuente debe declarar `version: 4.0.0`. Si no hay release 4.0.0 publicada, usar solo el candidato local autorizado o informar su ausencia; nunca instalar otra version silenciosamente.

Previsualizar con el comando siguiente antes de validar; despues de `je valide`, elegir solo el modo correspondiente. `--plan-out` escribe un plan local y requiere autorizacion; `--apply-plan` rechaza diagnosticos obsoletos. `--restore` es una operacion separada con el diario exacto de la transaccion y rechaza cambios posteriores. No borrar archivos para eludir conflictos.

Los planes guardados contienen archivos: conservarlos localmente. Definir `SR_TARGET` como ruta del repositorio destino.

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Objetivo verificable: instalar SR Pack 4.0.0 con `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 y `SR_PASSES` 0.2, verificarlo y detenerse antes de cualquier desarrollo de aplicación.

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

Recorridos: instalacion nueva `00 -> 06`; instalacion existente `05 -> 06 -> 07`. El prompt `06` solo verifica; `07` propone el realineamiento y espera `je valide` antes de modificar la memoria. Ningun recorrido autoriza desarrollo aplicativo.
