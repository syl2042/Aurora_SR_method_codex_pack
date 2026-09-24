# Instalación — SR Method 4.1

Estado: versión publicada `4.1.0`. Seleccionar `SR_PACK_SOURCE` de forma explícita y registrar `release_status`, `source_commit` y el estado Git.

[English](INSTALLATION.md) · [Français](INSTALLATION.fr.md) · [Deutsch](INSTALLATION.de.md) · [Português](INSTALLATION.pt.md)

## Elegir según el estado observado

| Estado del destino | Prompt | Modo |
|---|---|---|
| Sin marcador SR | `prompts/es/00_install_codex_environment.md` | `--write` |
| Con marcador SR, parcial o desconocido | `prompts/es/05_upgrade_codex_environment.md` | `--upgrade` |

La versión anterior nunca decide el algoritmo. Revisar la vista previa, los conflictos y los archivos preservados antes de aplicar:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Para un destino nuevo, usar `--write` en lugar de `--upgrade`. La transacción guarda los archivos modificados, detecta cambios concurrentes y admite un `--restore` exacto.

El post-check es de solo lectura por defecto. Usar `--write-report` solo cuando se solicite un artefacto de auditoría persistente.

El contenido gestionado converge, el estado del proyecto se preserva, las personalizaciones desconocidas se declaran como conflicto y los archivos obsoletos solo se eliminan si su contenido se reconoce como gestionado. No se modifican código de producto, secretos, migraciones, despliegues, requisitos abiertos ni históricos de `SR_LOTS.yaml`/`SR_PASSES.yaml`.

Una instalación nueva incluye `SR_PASSES.yaml` con `passes: []`, `MCP_POLICY.yaml` y `task_state.yaml`. Después de una verificación correcta, usar `prompts/es/07_realign_sr_state_after_upgrade.md` solo si el estado del proyecto necesita una realineación real. La definición de pases sigue en `08_define_sr_passes_from_lots.md`, los lotes en `09_define_sr_lots_from_scope.md`; `build_pass_runtime_goal.py` queda como herramienta legacy opcional.
