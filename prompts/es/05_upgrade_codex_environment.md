# Actualizar un proyecto a la SR Method mas reciente

Estas trabajando en un repositorio de aplicacion que ya contiene una instalacion existente de Aurora SR Method, posiblemente antigua, parcial o adaptada localmente.

Objetivo verificable: actualizar la SR Method a la ultima version oficial disponible, sin regresion, sin modificar codigo de aplicacion, sin sobrescribir adaptaciones del proyecto, y dejando el proyecto en un estado SR realineado antes de reanudar cualquier desarrollo.

Fuente oficial de SR Method:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Fuente local del pack:

```text
SR_PACK_SOURCE
```

`SR_PACK_SOURCE` designa la ruta local del clon oficial en el servidor actual. Nunca supongas una ruta absoluta especifica de una maquina. Si el usuario no dio esta ruta, detectala o propone una ruta local adecuada, por ejemplo `./.sr-method-pack`, `/opt/aurora/SR_Method` o un directorio de trabajo validado por el usuario.

Si la fuente local no existe o no es un clon del repositorio oficial, propone crearla o actualizarla desde el repositorio GitHub oficial antes de aplicar el upgrade. No descargues desde otra fuente sin validacion del usuario.

Reglas estrictas:

- No modifiques codigo de aplicacion.
- No crees migraciones.
- No cambies dependencias de aplicacion.
- No toques secretos, variables de entorno ni archivos de configuracion sensibles.
- No reemplaces a ciegas `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `PROJECT_PROFILE.yaml`, `SKILL_MAP.md`, `docs/codex/SR_LOTS.yaml`, `docs/codex/SR_PASSES.yaml`, task memories, handoffs, decisiones o skills del proyecto.
- Preserva las adaptaciones locales del proyecto.
- Preserva los archivos legacy de task memory; no crees contratos retroactivos en lote sin validacion explicita.
- Preserva `SR_LOTS.yaml`. Agrega `SR_PASSES.yaml` de forma aditiva si falta, pero no conviertas automaticamente lotes antiguos o task memories en pasadas validadas.
- No conviertas masivamente lotes antiguos para agregar `design_evidence`; agrega Lot Design Evidence Gate solo a lotes creados, promovidos o retomados despues del upgrade.
- Agrega Pass Runtime Goal tooling de forma aditiva (`build_pass_runtime_goal.py`, template `pass_runtime_goal.md`, opciones `sr_passes.pass_runtime_goal`) sin generar un goal hasta que una pasada este validada.
- Nunca lances `/goal` durante el upgrade. El upgrade prepara el metodo; la ejecucion por goal solo viene despues del realineamiento, pass planning y validacion del usuario.
- Preserva task memories historicas sin `propagation_gate`: reportalas como legacy warnings, no como errores bloqueantes. Los nuevos templates y contratos creados despues del upgrade deben incluir el Propagation Gate.
- En regimen SR completo, todo cambio de version SR debe actualizar `docs/CURRENT_STATE.md` con version instalada, fecha de revision, checks ejecutados, ultimo `NEXT_SESSION_PROMPT.md`, lotes significativos y siguiente paso.
- Un `loop_contract.json` de tipo `upgrade` no puede cerrarse como `done` con `memory_updates.current_state_updated=false`.
- Antes de modificar cualquier archivo, presenta el plan de upgrade y espera validacion explicita del usuario.

Paso 1 - Diagnostico de version:

1. Lee los archivos SR existentes:
   - `docs/codex/SR_PACK_VERSION.json` si existe;
   - `docs/codex/SR_LOTS.yaml` si existe;
   - `docs/codex/SR_PASSES.yaml` si existe;
   - `docs/CURRENT_STATE.md` si existe;
   - `AGENTS.md` si existe;
   - `docs/codex/tasks/` si existe.
2. Ejecuta auditorias disponibles sin modificar:
   - `python3 scripts/codex/audit_codex_pack.py --json` si esta disponible;
   - `python3 scripts/codex/verify_codex_pack.py` si esta disponible;
   - `python3 scripts/codex/sr_post_install_check.py --root .` si esta disponible.
3. Si estos scripts no existen o fallan porque la version es demasiado antigua, clasifica la version como `unknown` o `legacy`.

Paso 2 - Clasificacion:

Clasifica el proyecto en un flujo:

- `upgrade_minor_3x` si la version instalada ya es `3.x`;
- `upgrade_standard_235_plus` si la version es `2.3.5+`;
- `upgrade_legacy_unknown` si la version falta, no se puede leer, es inferior a `2.3.5`, o la instalacion SR es parcial.

Paso 3 - Fuente oficial:

1. Verifica si ya existe un clon local del pack oficial.
2. Si existe, verifica su remote y su estado git.
3. Si no existe, propone clonar:
   `git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git ./.sr-method-pack`
4. Usa solo la fuente oficial o un clon local verificado.
5. Anota el commit fuente usado en el informe final.

Paso 4 - Analisis antes de mutacion:

Compara la instalacion actual con la ultima version del pack e identifica:

- archivos SR faltantes;
- archivos SR antiguos;
- archivos del proyecto a preservar;
- archivos que requieren merge cuidadoso;
- presencia o ausencia de `SR_PASSES.yaml`;
- presencia o ausencia del tooling Pass Runtime Goal;
- presencia o ausencia del Lot Design Evidence Gate;
- riesgos de sobrescritura;
- contratos antiguos o task memories a conservar como legacy warnings.

Importante: los lotes antiguos sin `design_evidence` no deben modificarse en lote. `design_evidence` debe agregarse solo a lotes creados, promovidos o retomados despues del upgrade.

Paso 5 - Plan para validar:

Antes de cualquier modificacion, presenta un plan corto con:

- version detectada;
- flujo de upgrade elegido;
- archivos a agregar;
- archivos a actualizar;
- archivos a preservar;
- riesgos identificados;
- comandos de verificacion previstos;
- impacto esperado en `SR_LOTS.yaml`, `SR_PASSES.yaml`, `AGENTS.md`, `CURRENT_STATE.md` y `docs/codex/tasks/`.

Espera validacion explicita del usuario antes de modificar.

Paso 6 - Upgrade despues de validacion:

Solo despues de validacion:

1. Aplica el upgrade SR de forma aditiva.
2. Preserva archivos del proyecto e historicos.
3. Actualiza scripts, templates, prompts y docs SR necesarios.
4. Agrega `SR_PASSES.yaml` si falta, sin declarar automaticamente una pasada ejecutable.
5. Agrega Pass Runtime Goal tooling si falta:
   - `build_pass_runtime_goal.py`
   - template `pass_runtime_goal.md`
   - opciones `sr_passes.pass_runtime_goal`
6. Verifica que el Goal Length Gate este presente:
   - `max_goal_command_chars: 1000`
   - `hard_limit: 4000`
7. Verifica que el Lot Design Evidence Gate este documentado y activo para lotes nuevos o retomados.

Paso 7 - Verificacion:

Ejecuta los checks disponibles y aplicables:

- `python3 scripts/codex/audit_codex_pack.py`
- `python3 scripts/codex/verify_codex_pack.py`
- `python3 scripts/codex/sr_post_install_check.py --root .`
- `python3 scripts/codex/find_next_session_prompt.py --root .`
- `python3 scripts/codex/audit_sr_project.py --root .`
- `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` si el archivo existe
- `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` si `SR_PASSES.yaml` existe
- `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json` si existe
- `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json` si existe
- `python3 scripts/codex/audit_sr_task_contracts.py --root .`
- `python3 scripts/codex/context_budget_report.py --root . --compact`
- `python3 scripts/codex/validate_skills.py --path ~/.codex/skills` si las skills del metodo estan instaladas

Si algunos scripts faltan antes del upgrade, reportalo como normal para una version antigua y vuelve a ejecutarlos despues del upgrade.

Paso 8 - Realineamiento obligatorio:

Despues del upgrade, actualiza o propone actualizar `docs/CURRENT_STATE.md` con:

- version SR anterior;
- version SR posterior;
- fecha de actualizacion;
- commit fuente usado;
- archivos agregados o actualizados;
- archivos preservados;
- legacy warnings;
- estado de `SR_LOTS.yaml`;
- estado de `SR_PASSES.yaml`;
- estado de Pass Runtime Goal;
- estado de Lot Design Evidence Gate;
- siguiente paso recomendado.

Paso 9 - Continuacion recomendada:

Al final, no reanudes directamente el desarrollo de aplicacion.

Propone esta secuencia segun el estado del proyecto:

1. usar `07_realign_sr_state_after_upgrade.md` para realinear el estado SR;
2. usar `09_define_sr_lots_from_scope.md` para crear o promover lotes con analisis previo de archivos impactados;
3. usar `08_define_sr_passes_from_lots.md` para proponer automaticamente agrupaciones de lotes en pasadas;
4. generar un `pass_runtime_goal.md` solo despues de validacion humana de una pasada;
5. lanzar `/goal` solo para una pasada validada, nunca durante el upgrade.

Informe final esperado:

- version anterior/posterior;
- flujo de upgrade elegido;
- commit fuente SR Method usado;
- archivos modificados;
- archivos preservados;
- validaciones exitosas;
- validaciones fallidas o no aplicables;
- legacy warnings;
- accion siguiente propuesta.

Fin obligatorio: espera validacion antes de cualquier modificacion de aplicacion o ejecucion de pasada.
