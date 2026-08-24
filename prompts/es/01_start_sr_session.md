# Iniciar una sesion SR gobernada

No programes.

Objetivo: reconstruir todo el alcance validado y proponer la siguiente accion coherente antes de cualquier mutacion.

1. Leer `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md` y `docs/CURRENT_STATE.md` cuando exista.
2. Ejecutar `python3 scripts/codex/find_next_session_prompt.py --root . --json` y leer el ultimo `NEXT_SESSION_PROMPT.md` encontrado.
3. Leer el `sr_contract.json` enlazado (SR Contract 3.1.0 o legacy 3.0.0), `loop_contract.json`, task memory, lotes y pasadas necesarios.
4. Recargar todas las entradas abiertas heredadas de `validated_requests`; no reanudar solo desde el ultimo feedback.
5. Separar requisitos hechos, parciales, no hechos, defectuosos, bloqueados o pendientes de evidencia.
6. Aplicar estados estrictos: implementacion incompleta significa `repair`; `user_testing` exige implementacion tecnica completa y solo E2E real o aceptacion humana pendiente.
7. Si el feedback corresponde a un requisito existente, reabrir por defecto el lote original con su checklist consolidada. No crear un micro-lote.
8. Ejecutar validadores de contratos y presupuesto de contexto disponibles sin modificar el proyecto.

Informar version SR, memoria usada, solicitudes validadas, estados de implementacion/evidencia, lotes reabiertos, bloqueos, evidencias pendientes, siguiente alcance coherente y validacion humana exacta requerida.

Detenerse y esperar validacion.
