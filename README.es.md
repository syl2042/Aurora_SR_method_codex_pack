# Aurora SR Method Codex Pack

SR Method 4.1 es un harness de ejecución ligero para Codex: núcleo permanente corto, procedimientos condicionales, activadores exactos de skills, estado compacto y verificación final proporcional.

Estado: **4.1.0 (`released`)**, publicada el 2026-09-24.

[English](README.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · **ES** · [Português](README.pt.md)

[Instalación](INSTALLATION.es.md) · [Changelog](CHANGELOG.md) · [Prompt de instalación](prompts/es/00_install_codex_environment.md) · [Prompt de actualización](prompts/es/05_upgrade_codex_environment.md) · [Verificar](prompts/es/06_verify_sr_installation.md) · [Realinear](prompts/es/07_realign_sr_state_after_upgrade.md)

## Cambios en 4.1

- `AGENTS.md` se reconcilia y reduce en lugar de acumular otro manual.
- El catálogo cognitivo predeterminado se limita a lotes, diagnóstico, arquitectura y QA visual de UI.
- TDD, planificación en archivos, compactación del terminal, revisión del diff y RepoMap son mecanismos del harness, no skills.
- No hay tests deliberadamente fallidos, gates rojos artificiales ni bucles de rollback de desarrollo.
- Scope, Verification y Activation son los únicos límites de ejecución.
- Las tareas nuevas pueden usar un `task_state.yaml` compacto; los contratos antiguos siguen siendo legibles.
- El modo `core` no llama a MCP. `nexus_kg` sigue `MCP_POLICY.yaml`, con activación diferida, allowlists, aprobaciones y presupuestos de resultados.
- Entrada, lectura/escritura de caché, ocupación de contexto, salida y resultados de herramientas se miden por separado.

## Operación y actualización

```text
AGENTS.md -> SR_ROUTES.json -> solo el procedimiento activado
          -> 0 a 2 skills especializadas -> fuentes reales
          -> verificación final proporcional
```

La actualización es agnóstica de la versión anterior: esa versión solo aporta procedencia. El contenido real se clasifica como ausente, gestionado, modificado localmente, externo, obsoleto, en conflicto o ya alineado. El estado del proyecto se conserva; un artefacto obsoleto solo se elimina si su contenido se reconoce como gestionado.

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Detalles: [INSTALLATION.es.md](INSTALLATION.es.md). El historial y las migraciones viven únicamente en [CHANGELOG.md](CHANGELOG.md).
