# Realinhar o estado SR depois de um upgrade

Nao modifique codigo da aplicacao.

Objetivo: reconciliar a memoria SR com o codigo e todo o escopo validado antes de retomar o desenvolvimento.

Ler `AGENTS.md`, `docs/CURRENT_STATE.md`, metodo SR, `SR_LOTS.yaml`, `SR_PASSES.yaml`, ultimo `NEXT_SESSION_PROMPT.md`, task memories ativas, `sr_contract.json`, `loop_contract.json` e codigo/testes relevantes.

1. Executar auditorias do pack, documentacao de release, post-install, projeto e contratos de tarefa.
2. Preservar cada entrada de `validated_requests` com ID estavel, lote/passe original, `implementation_status`, `evidence_status`, testes pendentes e historico de feedback.
3. Reabrir o lote original quando um requisito validado estiver ausente, parcial, defeituoso, regressivo ou contradito por feedback.
4. Recarregar toda a checklist aberta do lote e da passe; nao isolar apenas o ultimo defeito.
5. Aplicar estados estritos: `done` apenas com implementacao e evidencias completas; `user_testing` apenas com implementacao tecnica completa e E2E/aceitacao pendente; `repair` com implementacao ausente, parcial, defeituosa ou falha; `blocked` apenas por autoridade, acesso, segredo, decisao ou mudanca externa realmente indisponivel.
6. Manter separadas as evidencias de codigo, build, runtime, E2E e deploy, ligadas ao mesmo requisito persistente.
7. Atualizar `CURRENT_STATE.md` e task memory apenas quando a evidencia sustentar o novo estado.

Comecar com `Pedido do usuario | Estado | Evidencia | Trabalho restante`, listar lotes reabertos e evidencias pendentes, e propor um escopo de reparacao consolidado. Novo lote apenas para escopo realmente novo.

Parar e pedir validacao humana exata antes de qualquer mutacao.
