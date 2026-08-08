# Instalación

[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

El flujo recomendado es **prompt Codex primero**. Los scripts Python son herramientas técnicas que Codex puede ejecutar después de inspeccionar.

## Instalar en un proyecto destino

1. Clona este repositorio.
2. Abre Codex en el proyecto destino.
3. Pega [prompts/es/00_install_codex_environment.md](prompts/es/00_install_codex_environment.md).
4. Deja que Codex instale, verifique y reporte.

Fallback técnico:

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target /path/to/project --profile default --write
```

Las nuevas instalaciones incluyen `docs/codex/SR_PASSES.yaml`. SR Passes agrupa varios lotes SR en una pasada acotada con orden de dependencias, preflight compartido, validaciones humanas y pruebas E2E agrupadas. Los lotes siguen siendo la unidad atomica en `SR_LOTS.yaml`.

## Actualizar

En el proyecto destino, pega [prompts/es/05_upgrade_codex_environment.md](prompts/es/05_upgrade_codex_environment.md). Codex debe auditar, conservar archivos del proyecto, presentar el plan y solo entonces aplicar el upgrade.

## Verificar

Pega [prompts/es/06_verify_sr_installation.md](prompts/es/06_verify_sr_installation.md).

Codex tambien debe validar las pasadas si el archivo existe:

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

## Definir SR Passes

Despues de encuadrar una funcion, usa primero [prompts/es/09_define_sr_lots_from_scope.md](prompts/es/09_define_sr_lots_from_scope.md) para definir lotes con Lot Design Evidence Gate. Luego pega [prompts/es/08_define_sr_passes_from_lots.md](prompts/es/08_define_sr_passes_from_lots.md). Estos pasos solo actualizan la memoria SR y no deben modificar codigo de aplicacion.

## Iniciar sesión

Pega [prompts/es/01_start_sr_session.md](prompts/es/01_start_sr_session.md). Para agentes IA runtime, usa [prompts/es/15_define_runtime_agents.md](prompts/es/15_define_runtime_agents.md).
