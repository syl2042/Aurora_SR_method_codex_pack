# Realinhar o estado SR depois de um upgrade

## SR 4.0.0 — versao publicada

Comecar em somente leitura. As reaberturas e atualizacoes abaixo sao propostas ate a validacao exata `je valide` do escopo de realinhamento; aplica-las depois apenas nesse escopo. Autorizacao de instalacao nao autoriza reparos da aplicacao.

Nao modifique codigo da aplicacao.

Objetivo: reconciliar a memoria SR com o codigo e todo o escopo validado antes de retomar o desenvolvimento.

Ler `AGENTS.md` e depois `docs/codex/SR_BOOTSTRAP.md`. Executar `python3 scripts/codex/find_next_session_prompt.py --root . --json`: usar `selected`; se `ambiguous`, pedir o caminho e usar `--prompt`. Nunca escolher `latest` apenas pela data. Ler o `NEXT_SESSION_PROMPT.md` selecionado e seus `sr_contract.json`/`loop_contract.json`, preservando todas as `validated_requests` abertas herdadas. Sem handoff, inventariar lotes abertos e propor o escopo. Para este realinhamento ler tambem `docs/CURRENT_STATE.md` e os registros de lotes/passes para identificar divergencias globais. Depois carregar apenas memorias detalhadas, procedimentos, RepoMap/KG e codigo/testes necessarios aos lotes afetados; ampliar quando uma evidencia, gate ou dependencia exigir.

1. Executar auditorias do pack, documentacao de release, post-install, projeto e contratos de tarefa.
2. Preservar cada entrada de `validated_requests` com ID estavel, lote/passe original, `implementation_status`, `evidence_status`, testes pendentes e historico de feedback.
3. Reabrir o lote original quando um requisito validado estiver ausente, parcial, defeituoso, regressivo ou contradito por feedback.
4. Recarregar toda a checklist aberta do lote e da passe; nao isolar apenas o ultimo defeito.
5. Aplicar estados estritos: `done` apenas com implementacao e evidencias completas; `user_testing` apenas com implementacao tecnica completa e E2E/aceitacao pendente; `repair` com implementacao ausente, parcial, defeituosa ou falha; `blocked` apenas por autoridade, acesso, segredo, decisao ou mudanca externa realmente indisponivel.
6. Manter separadas as evidencias de codigo, build, runtime, E2E e deploy, ligadas ao mesmo requisito persistente.
7. Atualizar `CURRENT_STATE.md` e task memory apenas quando a evidencia sustentar o novo estado.

Comecar com `Pedido do usuario | Estado | Evidencia | Trabalho restante`, listar lotes reabertos e evidencias pendentes, e propor um escopo de reparacao consolidado. Novo lote apenas para escopo realmente novo.

Parar e pedir validacao humana exata antes de qualquer mutacao.

Percursos: instalacao nova `00 -> 06`; instalacao existente `05 -> 06 -> 07`. O prompt `06` somente verifica; `07` propoe o realinhamento e espera `je valide` antes de alterar a memoria. Nenhum percurso autoriza desenvolvimento da aplicacao.
