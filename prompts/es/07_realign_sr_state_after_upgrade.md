# Realinear el estado SR despues de un upgrade

## SR 4.0.0 — version publicada

Empezar en solo lectura. Las reaperturas y actualizaciones siguientes son propuestas hasta la validacion exacta `je valide` del alcance de realineamiento; aplicarlas despues solo en ese alcance. La aprobacion de instalacion no autoriza reparaciones de la aplicacion.

No modifiques codigo aplicativo.

Objetivo: reconciliar la memoria SR con el codigo y todo el alcance validado antes de reanudar el desarrollo.

Leer `AGENTS.md` y despues `docs/codex/SR_BOOTSTRAP.md`. Ejecutar `python3 scripts/codex/find_next_session_prompt.py --root . --json`: usar `selected`; si `ambiguous`, pedir la ruta y usar `--prompt`. Nunca elegir `latest` solo por fecha. Leer el `NEXT_SESSION_PROMPT.md` seleccionado y sus `sr_contract.json`/`loop_contract.json`, conservando todas las `validated_requests` abiertas heredadas. Sin handoff, inventariar lotes abiertos y proponer el alcance. Para este realineamiento leer tambien `docs/CURRENT_STATE.md` y los registros de lotes/pasadas para detectar discrepancias globales. Cargar despues solo memorias detalladas, procedimientos, RepoMap/KG y codigo/tests necesarios para los lotes afectados; ampliar cuando una evidencia, gate o dependencia lo exija.

1. Ejecutar auditorias del pack, documentacion de release, post-install, proyecto y contratos de tarea.
2. Conservar cada entrada de `validated_requests` con ID estable, lote/pasada original, `implementation_status`, `evidence_status`, tests pendientes e historial de feedback.
3. Reabrir el lote original cuando un requisito validado falte, sea parcial, defectuoso, regresivo o contradicho por feedback.
4. Recargar toda la checklist abierta del lote y de la pasada; no aislar solo el ultimo defecto.
5. Aplicar estados estrictos: `done` solo con implementacion y evidencias completas; `user_testing` solo con implementacion tecnica completa y E2E/aceptacion pendiente; `repair` con implementacion ausente, parcial, defectuosa o fallida; `blocked` solo por autoridad, acceso, secreto, decision o cambio externo realmente no disponible.
6. Mantener separadas las evidencias de codigo, build, runtime, E2E y despliegue, unidas al mismo requisito persistente.
7. Actualizar `CURRENT_STATE.md` y task memory solo cuando la evidencia soporte el nuevo estado.

Comenzar con `Solicitud de usuario | Estado | Evidencia | Trabajo restante`, listar lotes reabiertos y evidencias pendientes, y proponer un alcance de reparacion consolidado. Nuevo lote solo para alcance realmente nuevo.

Detenerse y pedir validacion humana exacta antes de mutar.

Recorridos: instalacion nueva `00 -> 06`; instalacion existente `05 -> 06 -> 07`. El prompt `06` solo verifica; `07` propone el realineamiento y espera `je valide` antes de modificar la memoria. Ningun recorrido autoriza desarrollo aplicativo.
