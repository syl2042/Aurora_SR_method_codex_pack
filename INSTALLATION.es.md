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

## Actualizar

En el proyecto destino, pega [prompts/es/05_upgrade_codex_environment.md](prompts/es/05_upgrade_codex_environment.md). Codex debe auditar, conservar archivos del proyecto, presentar el plan y solo entonces aplicar el upgrade.

## Verificar

Pega [prompts/es/06_verify_sr_installation.md](prompts/es/06_verify_sr_installation.md).

## Iniciar sesión

Pega [prompts/es/01_start_sr_session.md](prompts/es/01_start_sr_session.md). Para agentes IA runtime, usa [prompts/es/15_define_runtime_agents.md](prompts/es/15_define_runtime_agents.md).
