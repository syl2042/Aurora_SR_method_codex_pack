# Realinear el estado SR despues de un upgrade

No modifiques codigo aplicativo.

Objetivo: reconciliar la memoria SR con el codigo y todo el alcance validado antes de reanudar el desarrollo.

Leer `AGENTS.md`, `docs/CURRENT_STATE.md`, metodo SR, `SR_LOTS.yaml`, `SR_PASSES.yaml`, ultimo `NEXT_SESSION_PROMPT.md`, task memories activas, `sr_contract.json`, `loop_contract.json` y codigo/tests relevantes.

1. Ejecutar auditorias del pack, documentacion de release, post-install, proyecto y contratos de tarea.
2. Conservar cada entrada de `validated_requests` con ID estable, lote/pasada original, `implementation_status`, `evidence_status`, tests pendientes e historial de feedback.
3. Reabrir el lote original cuando un requisito validado falte, sea parcial, defectuoso, regresivo o contradicho por feedback.
4. Recargar toda la checklist abierta del lote y de la pasada; no aislar solo el ultimo defecto.
5. Aplicar estados estrictos: `done` solo con implementacion y evidencias completas; `user_testing` solo con implementacion tecnica completa y E2E/aceptacion pendiente; `repair` con implementacion ausente, parcial, defectuosa o fallida; `blocked` solo por autoridad, acceso, secreto, decision o cambio externo realmente no disponible.
6. Mantener separadas las evidencias de codigo, build, runtime, E2E y despliegue, unidas al mismo requisito persistente.
7. Actualizar `CURRENT_STATE.md` y task memory solo cuando la evidencia soporte el nuevo estado.

Comenzar con `Solicitud de usuario | Estado | Evidencia | Trabajo restante`, listar lotes reabiertos y evidencias pendientes, y proponer un alcance de reparacion consolidado. Nuevo lote solo para alcance realmente nuevo.

Detenerse y pedir validacion humana exacta antes de mutar.
