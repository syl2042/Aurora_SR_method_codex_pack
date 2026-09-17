# Atualizar uma instalacao SR existente para a fonte validada

## SR 4.0.0 — versao publicada

Fonte alvo: selecionar explicitamente `SR_PACK_SOURCE`, uma versao publicada identificada ou o candidato local SR 4.0.0 autorizado. Ler `core/SR_PACK_VERSION.json` (`version`, `release_status`); registrar `source_commit`, estado Git e, havendo alteracoes locais, uma impressao do conteudo incluindo arquivos fonte nao rastreados utilizados. Nao apresentar um candidato `unreleased` como release. Nao substituir o candidato por um clone da ultima versao publicada; se a fonte solicitada faltar, parar e esclarecer antes de instalar.

Para este alvo SR 4.0.0, a fonte deve declarar `version: 4.0.0`. Se nao houver release 4.0.0 publicada, usar somente o candidato local autorizado ou informar sua ausencia; nunca instalar outra versao silenciosamente.

Previsualizar com o comando abaixo antes da validacao; depois de `je valide`, escolher apenas o modo correspondente. `--plan-out` escreve um plano local e exige autorizacao; `--apply-plan` rejeita diagnosticos desatualizados. `--restore` e uma operacao separada com o diario exato da transacao e rejeita edicoes posteriores. Nao excluir arquivos para contornar conflitos.

Planos salvos contem arquivos: mante-los localmente. Definir `SR_TARGET` como caminho do repositorio alvo.

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

```bash
# je valide
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

Voce esta trabalhando em um repositorio de aplicacao que ja contem uma instalacao existente da Aurora SR Method, possivelmente antiga, parcial ou adaptada localmente.

Objetivo verificavel: atualizar a SR Method para a fonte alvo explicitamente selecionada, sem regressao, sem modificar codigo da aplicacao, sem sobrescrever adaptacoes do projeto, e deixando o projeto em um estado SR realinhado antes de retomar qualquer desenvolvimento.

Este prompt aceita um alvo ou uma lista explicita de repositorios. Com varias pastas, trate cada repositorio como alvo independente e produza antes da mutacao a matriz `repository | marcadores lidos | versao detectada | estado | fluxo | arquivos a preservar | validacao`. Nunca suponha versao comum; atualize e verifique alvo por alvo.

Se um alvo nao tiver marcador SR, classifique-o como `fresh_install`, retire-o do fluxo de upgrade e use `00_install_codex_environment.md` com validacao propria.

Fonte oficial da SR Method:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Fonte local do pack:

```text
SR_PACK_SOURCE
```

`SR_PACK_SOURCE` designa o caminho local do clone oficial no servidor atual. Nunca suponha um caminho absoluto especifico de uma maquina. Se o usuario nao forneceu esse caminho, detecte-o ou proponha um caminho local adequado, por exemplo `./.sr-method-pack`, `/opt/aurora/SR_Method` ou um diretorio de trabalho validado pelo usuario.

Se a fonte local nao existir ou nao for um clone do repositorio oficial, proponha cria-la ou atualiza-la a partir do repositorio GitHub oficial antes de aplicar o upgrade. Nao baixe de outra fonte sem validacao do usuario.

Regras estritas:

- Nao modifique codigo da aplicacao.
- Nao crie migracoes.
- Nao altere dependencias da aplicacao.
- Nao toque em segredos, variaveis de ambiente ou arquivos de configuracao sensiveis.
- Nao substitua cegamente `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `PROJECT_PROFILE.yaml`, `SKILL_MAP.md`, `docs/codex/SR_LOTS.yaml`, `docs/codex/SR_PASSES.yaml`, task memories, handoffs, decisoes ou skills do projeto.
- Preserve as adaptacoes locais do projeto.
- Preserve arquivos legacy de task memory; nao crie contratos retroativos em lote sem validacao explicita.
- Preserve `SR_LOTS.yaml`. Se `SR_PASSES.yaml` estiver ausente, adicione um registro valido `passes: []`; nao copie uma pass de exemplo nem converta automaticamente lotes antigos ou task memories em passes validadas.
- Nao converta lotes antigos em massa para adicionar `design_evidence`; adicione Lot Design Evidence Gate somente a lotes criados, promovidos ou retomados apos o upgrade.
- Adicione Pass Runtime Goal tooling de forma aditiva (`build_pass_runtime_goal.py`, template `pass_runtime_goal.md`, opcoes `sr_passes.pass_runtime_goal`) sem gerar um goal ate que uma pass esteja validada.
- Nunca lance `/goal` durante o upgrade. O upgrade prepara o metodo; a execucao por goal vem somente depois do realinhamento, pass planning e validacao do usuario.
- Nao feche, promova nem reclassifique nenhum lote ou pass de aplicacao como efeito colateral implicito do upgrade. Se o usuario pedir explicitamente para fechar um lote ou pass no mesmo trabalho, trate esse fechamento como uma subfase separada depois do upgrade, com escopo validado, contrato SR proprio, evidencias e relatorio distinto.
- Preserve task memories historicas sem `propagation_gate`: reporte-as como legacy warnings, nao como erros bloqueantes. Novos templates e contratos criados depois do upgrade devem incluir o Propagation Gate.
- Preserve leitura compativel de contratos `sr_contract` 3.0.0. Novas task memories e lotes reabertos usam 3.1.0 com `implementation_status` e `evidence_status` separados.
- Nao reescreva `validated_requests` antigos em massa. Sinalize contratos multi-lote reduzidos a uma exigencia global; normalize apenas escopo ativo ou reaberto apos ler fontes e obter validacao humana.
- O upgrade nao deve fechar, mover ou transformar em novo lote nenhuma exigencia aberta, parcial ou defeituosa.
- Em regime SR completo, toda alteracao de versao SR deve atualizar `docs/CURRENT_STATE.md` com versao instalada, data de revisao, checks executados, `NEXT_SESSION_PROMPT.md` pertinente selecionado, lotes significativos e proximo passo.
- Um `loop_contract.json` do tipo `upgrade` nao pode fechar como `done` com `memory_updates.current_state_updated=false`.
- Antes de qualquer modificacao de arquivo, apresente o plano de upgrade e aguarde validacao explicita do usuario.

Etapa 1 - Diagnostico de versao:

1. Leia os arquivos SR existentes:
   - `docs/codex/SR_PACK_VERSION.json` se existir;
   - `docs/codex/SR_LOTS.yaml` se existir;
   - `docs/codex/SR_PASSES.yaml` se existir;
   - `docs/CURRENT_STATE.md` se existir;
   - `AGENTS.md` se existir;
   - `docs/codex/tasks/` se existir.
2. Execute auditorias disponiveis sem modificar:
   - `python3 scripts/codex/audit_codex_pack.py --json` se disponivel;
   - `python3 scripts/codex/verify_codex_pack.py` se disponivel;
   - `python3 scripts/codex/sr_post_install_check.py --root .` se disponivel.
3. Se esses scripts nao existirem ou falharem porque a versao e muito antiga, classifique a versao como `unknown` ou `legacy`.

Etapa 2 - Classificacao:

Classificar pelos arquivos observados e pela previsualizacao, independentemente do numero anterior:

- `fresh_install`: sem marcadores SR; usar o prompt `00`.
- `managed_update`: arquivos gerenciados reconhecidos, substituicoes e adicoes propostas sem conflitos.
- `already_current`: nenhuma mudanca proposta; verificar sem reescrever.
- `reconciliation_required`: conteudo gerenciado desconhecido/personalizado ou instalacao parcial com conflitos; preservar arquivos, comparar e validar a conciliacao antes de aplicar.

Uma instalacao parcial sem conflitos pode seguir `managed_update`. Preservar arquivos do projeto, contratos historicos, lotes, memorias e skills locais. A versao detectada e informativa; nao seleciona uma ramificacao de migracao.

Layouts oficiais representativos SR 2.2.0, 2.3.0, 2.3.5, 2.4.1 e 3.0.0 possuem regressoes de upgrade. Unknown/partial ainda exige auditoria arquivo por arquivo: a fixture prova o caminho minimo, nao toda adaptacao local.

Etapa 3 - Fonte oficial:

1. Verifique se ja existe um clone local do pack oficial.
2. Se existir, verifique o remote e o estado git.
3. Se nao existir, proponha clonar:
   `git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git ./.sr-method-pack`
4. Use somente a fonte oficial ou um clone local verificado.
5. Registre o commit fonte usado no relatorio final.

Etapa 4 - Analise antes de mutacao:

Compare a instalacao atual com a fonte alvo validada e identifique:

- arquivos SR ausentes;
- arquivos SR antigos;
- arquivos do projeto a preservar;
- arquivos que exigem merge cuidadoso;
- presenca ou ausencia de `SR_PASSES.yaml`;
- presenca ou ausencia do tooling Pass Runtime Goal;
- presenca ou ausencia do Lot Design Evidence Gate;
- riscos de sobrescrita;
- lotes ou passes de aplicacao que possam precisar de retomada ou fechamento, a tratar somente como subfase separada se o usuario pediu explicitamente;
- contratos antigos ou task memories a manter como legacy warnings.

Importante: lotes antigos sem `design_evidence` nao devem ser modificados em lote. `design_evidence` deve ser adicionado somente a lotes criados, promovidos ou retomados apos o upgrade.

Etapa 5 - Plano para validar:

Antes de qualquer modificacao, apresente um plano curto com:

- versao detectada;
- fluxo de upgrade escolhido;
- arquivos a adicionar;
- arquivos a atualizar;
- arquivos a preservar;
- riscos identificados;
- comandos de verificacao previstos;
- impacto esperado em `SR_LOTS.yaml`, `SR_PASSES.yaml`, `AGENTS.md`, `CURRENT_STATE.md` e `docs/codex/tasks/`.
- confirmacao de que nenhum lote ou pass de aplicacao sera fechado implicitamente pelo upgrade; qualquer fechamento pedido deve ser isolado como subfase validada.

Aguarde validacao explicita do usuario antes de modificar.

Etapa 6 - Upgrade depois da validacao:

Somente depois da validacao:

1. Aplique o upgrade SR de forma aditiva.
2. Preserve arquivos do projeto e historicos.
3. Atualize scripts, templates, prompts e docs SR necessarios.
4. Adicione `SR_PASSES.yaml` com `passes: []` se estiver ausente. O prompt `08` o preenche somente depois de ler os lotes e obter validacao humana.
5. Adicione Pass Runtime Goal tooling se estiver ausente:
   - `build_pass_runtime_goal.py`
   - template `pass_runtime_goal.md`
   - opcoes `sr_passes.pass_runtime_goal`
6. Verifique se o Goal Length Gate esta presente:
   - `max_goal_command_chars: 1000`
   - `hard_limit: 4000`
7. Verifique se o Lot Design Evidence Gate esta documentado e ativo para lotes novos ou retomados.

Etapa 7 - Verificacao:

Execute os checks disponiveis e aplicaveis:

- `python3 scripts/codex/audit_codex_pack.py`
- `python3 scripts/codex/verify_codex_pack.py`
- `python3 scripts/codex/sr_post_install_check.py --root .`
- `python3 scripts/codex/validate_release_docs.py --root . --json` para verificar `CHANGELOG.md`, versao e prompts publicos localizados
- `python3 scripts/codex/find_next_session_prompt.py --root .`
- `python3 scripts/codex/audit_sr_project.py --root .`
- `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml` se o arquivo existir
- `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml` se `SR_PASSES.yaml` existir
- `python3 scripts/codex/validate_loop_contract.py --file docs/codex/tasks/_TEMPLATE/loop_contract.json` se existir
- `python3 scripts/codex/validate_sr_contract.py --file docs/codex/tasks/_TEMPLATE/sr_contract.json` se existir
- `python3 scripts/codex/audit_sr_task_contracts.py --root .`
- `python3 scripts/codex/context_budget_report.py --root . --compact`
- `python3 scripts/codex/validate_skills.py --path ~/.codex/skills` se as skills do metodo estiverem instaladas

Se alguns scripts estiverem ausentes antes do upgrade, reporte isso como normal para uma versao antiga e execute novamente depois do upgrade.

O codigo 0 do instalador nao basta para declarar sucesso. `sr_post_install_check.py` tambem deve ficar verde; caso contrario o alvo permanece em `repair`.

Etapa 8 - Realinhamento obrigatorio:

Depois do upgrade, atualize ou proponha atualizar `docs/CURRENT_STATE.md` com:

- versao SR anterior;
- versao SR posterior;
- data de atualizacao;
- commit fonte usado;
- arquivos adicionados ou atualizados;
- arquivos preservados;
- legacy warnings;
- status de `SR_LOTS.yaml`;
- status de `SR_PASSES.yaml`;
- status do Pass Runtime Goal;
- status do Lot Design Evidence Gate;
- proximo passo recomendado.

Etapa 9 - Continuacao recomendada:

Ao final, nao retome diretamente o desenvolvimento da aplicacao.

Proponha esta sequencia conforme o estado do projeto:

1. usar `07_realign_sr_state_after_upgrade.md` para realinhar o estado SR;
2. usar `09_define_sr_lots_from_scope.md` para criar ou promover lotes com analise previa dos arquivos impactados;
3. usar `08_define_sr_passes_from_lots.md` para propor automaticamente agrupamentos de lotes em passes;
4. gerar um `pass_runtime_goal.md` somente depois da validacao humana de uma pass;
5. lancar `/goal` somente para uma pass validada, nunca durante o upgrade.

Relatorio final esperado:

- versao anterior/posterior;
- fluxo de upgrade escolhido;
- commit fonte SR Method usado;
- arquivos modificados;
- arquivos preservados;
- validacoes bem-sucedidas;
- validacoes falhas ou nao aplicaveis;
- legacy warnings;
- lotes ou passes de aplicacao detectados como candidatos a fechamento ou retomada, e status de qualquer subfase de fechamento pedida explicitamente;
- proxima acao proposta.

Fim obrigatorio: aguarde validacao antes de qualquer modificacao da aplicacao ou execucao de pass.

Percursos: instalacao nova `00 -> 06`; instalacao existente `05 -> 06 -> 07`. O prompt `06` somente verifica; `07` propoe o realinhamento e espera `je valide` antes de alterar a memoria. Nenhum percurso autoriza desenvolvimento da aplicacao.
