# Definir lotes SR desde alcance o inbox

Objetivo: convertir un encuadre, una solicitud de usuario o `docs/codex/SR_INBOX.yaml` en lotes SR explicitos en `docs/codex/SR_LOTS.yaml`, sin modificar codigo de aplicacion.

Reglas:

- No modifiques codigo de aplicacion.
- No crees un lote `planned`, `validated`, `in_progress` o `reopened` sin Lot Design Evidence Gate.
- Un lote `proposed` puede seguir exploratorio.
- Nunca marques un lote como `validated` sin validacion explicita del usuario.

Metodo:

1. Leer `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md`, `docs/codex/SR_HARNESS_METHOD.md`, `docs/codex/LOT_EXECUTION_METHOD.md`, `docs/CURRENT_STATE.md`, `docs/codex/SR_INBOX.yaml`, `docs/codex/SR_LOTS.yaml` y `docs/codex/CODEBASE_MAP.md` cuando existan.
2. Identificar superficies candidatas con `RepoMap/KG -> archivos candidatos -> lectura de codigo real -> tests/logs`.
3. Rellenar `design_evidence` para cada lote candidato.
4. Mantener en `proposed` cualquier lote cuyo encuadre dependa aun de una suposicion verificable.
5. Proponer los lotes para validacion antes de ejecutar.
6. Validar `SR_LOTS.yaml` con `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml`.
7. Recomendar despues `docs/codex/prompts/08_define_sr_passes_from_lots.md` si hay varios lotes ejecutables o casi ejecutables.

Salida esperada: lotes creados o modificados, estado del Lot Design Evidence Gate, archivos leidos, hipotesis restantes, preguntas bloqueantes, validacion de `SR_LOTS.yaml`, siguiente paso.
