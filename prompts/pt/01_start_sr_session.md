# Iniciar uma sessao SR governada

Nao programe.

Objetivo: reconstruir todo o escopo validado e propor a proxima acao coerente antes de qualquer mutacao.

1. Ler `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md` e `docs/CURRENT_STATE.md` quando existir.
2. Executar `python3 scripts/codex/find_next_session_prompt.py --root . --json` e ler o ultimo `NEXT_SESSION_PROMPT.md` encontrado.
3. Ler o `sr_contract.json` ligado (SR Contract 3.1.0 ou legacy 3.0.0), `loop_contract.json`, task memory, lotes e passes necessarios.
4. Recarregar todas as entradas abertas herdadas de `validated_requests`; nao retomar apenas pelo ultimo feedback.
5. Separar requisitos feitos, parciais, nao feitos, defeituosos, bloqueados ou aguardando evidencia.
6. Aplicar estados estritos: implementacao incompleta significa `repair`; `user_testing` exige implementacao tecnica completa e apenas E2E real ou aceitacao humana pendente.
7. Se o feedback tratar de um requisito existente, reabrir por padrao o lote original com sua checklist consolidada. Nao criar micro-lote.
8. Executar validadores de contratos e de orcamento de contexto disponiveis sem modificar o projeto.

Informar versao SR, memoria usada, pedidos validados, estados de implementacao/evidencia, lotes reabertos, bloqueios, evidencias pendentes, proximo escopo coerente e validacao humana exata necessaria.

Parar e aguardar validacao.
