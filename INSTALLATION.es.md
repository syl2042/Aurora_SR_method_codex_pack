# Instalación

[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

El flujo recomendado es **prompt Codex primero**. Los scripts Python son herramientas técnicas que Codex puede ejecutar después de inspeccionar.

## Elegir primero el recorrido correcto

- Sin marcador SR: prompt `00`, instalar SR 3.7.0 con `--write`.
- Marcador SR existente, antiguo o parcial: prompt `05`, auditar y actualizar de forma aditiva con `--upgrade`.
- Varios repositorios: leer versión y marcadores de cada uno, crear una matriz por destino y ejecutar un `--upgrade` por repositorio. Nunca asumir una versión común.

La instalación nueva usa `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 y `SR_PASSES` 0.2. `implementation_status` y `evidence_status` permanecen separados. La instalación no inventa `validated_requests` ni lotes de producto validados. El instalador rechaza `--write` si detecta una instalación SR previa.

## Instalar en un proyecto destino

1. Clona este repositorio.
2. Abre Codex en el proyecto destino.
3. Pega [prompts/es/00_install_codex_environment.md](prompts/es/00_install_codex_environment.md).
4. Deja que Codex instale, verifique y reporte.

Fallback técnico:

Sin `--write` ni `--upgrade`, el instalador solo muestra una vista previa de lectura. Los dos modos de mutación son mutuamente excluyentes.

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target /path/to/project --profile default --write
```

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
