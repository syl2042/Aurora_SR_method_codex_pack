# Instalación

## SR 4.0.0 — version publicada

Fuente objetivo: seleccionar explicitamente `SR_PACK_SOURCE`, una version publicada identificada o el candidato local SR 4.0.0 autorizado. Leer `core/SR_PACK_VERSION.json` (`version`, `release_status`); registrar `source_commit`, estado Git y, si hay cambios locales, una huella del contenido que incluya los archivos fuente no seguidos utilizados. No presentar un candidato `unreleased` como release. No sustituir el candidato por un clon de la ultima version publicada; si falta la fuente solicitada, detenerse y aclarar antes de instalar.

Para este objetivo SR 4.0.0, la fuente debe declarar `version: 4.0.0`. Si no hay release 4.0.0 publicada, usar solo el candidato local autorizado o informar su ausencia; nunca instalar otra version silenciosamente.

Recorridos: instalacion nueva `00 -> 06`; instalacion existente `05 -> 06 -> 07`. El prompt `06` solo verifica; `07` propone el realineamiento y espera `je valide` antes de modificar la memoria. Ningun recorrido autoriza desarrollo aplicativo.

SR 4 carga procedimientos segun la tarea mediante `SR_BOOTSTRAP.md` y `SR_ROUTES.json`. Conserva gates, HITL, requisitos abiertos y esquemas de contratos. La version del paquete no obliga a convertir contratos antiguos.

### Primera instalacion
Revisar reglas locales; obtener `je valide` para el alcance; previsualizar, aplicar `--write` y verificar. Conservar o fusionar explicitamente los archivos del proyecto. No modificar codigo de la aplicacion.

### Actualizacion independiente de version
Usar `--upgrade` tras revisar los archivos reales. La version anterior es informativa, nunca obligatoria. Clasificar por contenido instalaciones antiguas, sin version, parciales o mixtas. Un archivo desconocido/personalizado bloquea su sustitucion: no borrarlo para evitar el conflicto. Revisar y autorizar la conciliacion. Conservar contratos, lotes abiertos, memoria, handoffs y skills de dominio.

La previsualizacion solo escribe con `--plan-out` solicitado. Los planes contienen archivos y deben permanecer locales. `--apply-plan` rechaza cambios posteriores al diagnostico. La transaccion guarda copias; `--restore` no sobrescribe cambios posteriores. No forzar upgrades con `--write`. La version escrita no demuestra exito: debe pasar el postcheck.

Previsualizar con el comando siguiente antes de validar; despues de `je valide`, elegir solo el modo correspondiente. `--plan-out` escribe un plan local y requiere autorizacion; `--apply-plan` rechaza diagnosticos obsoletos. `--restore` es una operacion separada con el diario exacto de la transaccion y rechaza cambios posteriores. No borrar archivos para eludir conflictos.

Solo previsualizacion:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Instalacion nueva tras validacion:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --write
```

Instalacion existente tras validacion:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

Solo verificacion:

```bash
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Plan local opcional tras autorizacion:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --plan-out "$SR_PLAN_FILE"
```

Aplicar el plan validado, alternativa a comandos directos:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --apply-plan "$SR_PLAN_FILE"
```

Restauracion separada, solo si es necesaria y autorizada:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --restore "$SR_JOURNAL_FILE"
```


[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

El flujo recomendado es **prompt Codex primero**. Los scripts Python son herramientas técnicas que Codex puede ejecutar después de inspeccionar.

## Elegir primero el recorrido correcto

- Sin marcador SR: prompt `00`, instalar SR 4.0.0 con `--write`.
- Marcador SR existente, antiguo o parcial: prompt `05`, auditar y actualizar de forma aditiva con `--upgrade`.
- Varios repositorios: leer versión y marcadores de cada uno, crear una matriz por destino y ejecutar un `--upgrade` por repositorio. Nunca asumir una versión común.

La instalación nueva usa `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 y `SR_PASSES` 0.2. `implementation_status` y `evidence_status` permanecen separados. La instalación no inventa `validated_requests` ni lotes de producto validados. El instalador rechaza `--write` si detecta una instalación SR previa.

## Instalar en un proyecto destino

1. Seleccionar la fuente local verificada segun Fuente objetivo.
2. Abre Codex en el proyecto destino.
3. Pega [prompts/es/00_install_codex_environment.md](prompts/es/00_install_codex_environment.md).
4. Deja que Codex instale, verifique y reporte.

Fallback técnico:

Sin opcion de mutacion ni `--plan-out`, el instalador ofrece una previsualizacion de solo lectura. `--write`, `--upgrade`, `--apply-plan` y `--restore` son mutuamente excluyentes.

Usar el clon `SR_PACK_SOURCE` ya seleccionado y verificado. Para una version publicada, clonar la fuente oficial si hace falta y seleccionar la referencia publicada validada; clonar no selecciona el candidato SR 4. El candidato requiere el contenido local explicitamente autorizado. Definir `SR_TARGET` como ruta del proyecto destino antes de los comandos.

Las nuevas instalaciones incluyen `docs/codex/SR_PASSES.yaml`. SR Passes agrupa varios lotes SR en una pasada acotada con orden de dependencias, preflight compartido, validaciones humanas y pruebas E2E agrupadas. Los lotes siguen siendo la unidad atomica en `SR_LOTS.yaml`.

El registro empieza con `passes: []`. Este estado es valido: la instalacion no inventa una pasada de producto. El prompt `08` se usa despues de leer y validar los lotes.

## Actualizar

En el proyecto destino, pega [prompts/es/05_upgrade_codex_environment.md](prompts/es/05_upgrade_codex_environment.md). Codex debe auditar, conservar archivos del proyecto, presentar el plan y solo entonces aplicar el upgrade.

Los contratos históricos `sr_contract` 3.0.0 siguen legibles. No se reescriben task memories en masa: solo se normaliza alcance activo o reabierto tras revisar su fuente, se conservan requirement IDs abiertos y se reabre el lote original por defecto. Un resultado verde en una carpeta no oculta problemas en otras.

Los layouts oficiales representativos SR 2.2.0, 2.3.0, 2.3.5, 2.4.1 y 3.0.0 estan cubiertos por regresiones de upgrade. Si falta `SR_PASSES.yaml`, se crea un registro valido `passes: []`. Unknown/partial o adaptaciones locales siguen exigiendo auditoria archivo por archivo. El codigo 0 del instalador no basta: `sr_post_install_check.py` tambien debe estar verde; si no, el destino queda en `repair`.

## Verificar

Pega [prompts/es/06_verify_sr_installation.md](prompts/es/06_verify_sr_installation.md).

Verifica tambien documentacion de release y prompts publicos:

```bash
python3 scripts/codex/validate_release_docs.py --root . --json
```

Codex tambien debe validar las pasadas si el archivo existe:

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

## Definir lotes SR

Despues de encuadrar una funcion, usa [prompts/es/09_define_sr_lots_from_scope.md](prompts/es/09_define_sr_lots_from_scope.md) para definir `SR_LOTS.yaml` con Lot Design Evidence Gate.

## Definir SR Passes

Luego usa [prompts/es/08_define_sr_passes_from_lots.md](prompts/es/08_define_sr_passes_from_lots.md) para proponer una pasada coherente en `SR_PASSES.yaml`. Estos pasos solo actualizan la memoria SR y no deben modificar codigo de aplicacion.

## Generar un Pass Runtime Goal

Para una pasada validada, Codex puede generar el goal runtime acotado:

```bash
python3 scripts/codex/build_pass_runtime_goal.py --pass-id <PASS_ID> --output docs/codex/tasks/YYYY-MM-DD_<pass-id>/pass_runtime_goal.md
```

## Iniciar sesión

Pega [prompts/es/01_start_sr_session.md](prompts/es/01_start_sr_session.md). Para agentes IA runtime, usa [prompts/es/15_define_runtime_agents.md](prompts/es/15_define_runtime_agents.md).
