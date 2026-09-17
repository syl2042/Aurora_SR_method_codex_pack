# Instalação

## SR 4.0.0 — versao publicada

Fonte alvo: selecionar explicitamente `SR_PACK_SOURCE`, uma versao publicada identificada ou o candidato local SR 4.0.0 autorizado. Ler `core/SR_PACK_VERSION.json` (`version`, `release_status`); registrar `source_commit`, estado Git e, havendo alteracoes locais, uma impressao do conteudo incluindo arquivos fonte nao rastreados utilizados. Nao apresentar um candidato `unreleased` como release. Nao substituir o candidato por um clone da ultima versao publicada; se a fonte solicitada faltar, parar e esclarecer antes de instalar.

Para este alvo SR 4.0.0, a fonte deve declarar `version: 4.0.0`. Se nao houver release 4.0.0 publicada, usar somente o candidato local autorizado ou informar sua ausencia; nunca instalar outra versao silenciosamente.

Percursos: instalacao nova `00 -> 06`; instalacao existente `05 -> 06 -> 07`. O prompt `06` somente verifica; `07` propoe o realinhamento e espera `je valide` antes de alterar a memoria. Nenhum percurso autoriza desenvolvimento da aplicacao.

SR 4 carrega procedimentos conforme a tarefa usando `SR_BOOTSTRAP.md` e `SR_ROUTES.json`. Gates, HITL, requisitos abertos e esquemas de contratos permanecem preservados. A versao do pacote nao exige converter contratos antigos.

### Primeira instalacao
Inspecionar regras locais; obter `je valide` para o escopo; previsualizar, aplicar `--write` e verificar. Preservar ou mesclar explicitamente arquivos do projeto. Nenhuma alteracao no codigo da aplicacao.

### Atualizacao independente da versao
Usar `--upgrade` depois da inspecao dos arquivos reais. A versao anterior e informativa, nunca obrigatoria. Classificar por conteudo instalacoes antigas, sem versao, parciais ou mistas. Arquivos desconhecidos/personalizados bloqueiam substituicao: nao remover para contornar conflitos. Revisar e autorizar a conciliacao. Preservar contratos, lotes abertos, memoria, handoffs e skills de dominio.

A previsualizacao so escreve com `--plan-out` solicitado. Planos contem arquivos e devem ficar locais. `--apply-plan` rejeita alteracoes posteriores. Transacoes guardam copias; `--restore` nao sobrescreve edicoes posteriores. Nunca forcar upgrades com `--write`. A versao gravada nao prova sucesso: o postcheck deve passar.

Previsualizar com o comando abaixo antes da validacao; depois de `je valide`, escolher apenas o modo correspondente. `--plan-out` escreve um plano local e exige autorizacao; `--apply-plan` rejeita diagnosticos desatualizados. `--restore` e uma operacao separada com o diario exato da transacao e rejeita edicoes posteriores. Nao excluir arquivos para contornar conflitos.

Somente previsualizacao:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Instalacao nova apos validacao:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --write
```

Instalacao existente apos validacao:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
```

Somente verificacao:

```bash
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Plano local opcional apos autorizacao:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --plan-out "$SR_PLAN_FILE"
```

Aplicar o plano validado, alternativa aos comandos diretos:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --apply-plan "$SR_PLAN_FILE"
```

Restauracao separada, somente se necessaria e autorizada:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --restore "$SR_JOURNAL_FILE"
```


[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

O fluxo recomendado é **prompt Codex primeiro**. Os scripts Python são ferramentas técnicas que o Codex pode executar após a inspeção.

## Escolher primeiro o percurso correto

- Sem marcador SR: prompt `00`, instalar SR 4.0.0 com `--write`.
- Marcador SR existente, antigo ou parcial: prompt `05`, auditar e atualizar de forma aditiva com `--upgrade`.
- Vários repositórios: ler versão e marcadores de cada alvo, criar uma matriz por repositório e executar um `--upgrade` por alvo. Nunca supor versão comum.

A instalação nova usa `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 e `SR_PASSES` 0.2. `implementation_status` e `evidence_status` ficam separados. A instalação não inventa `validated_requests` nem lotes de produto validados. O instalador recusa `--write` se detectar instalação SR existente.

## Instalar em um projeto alvo

1. Selecionar a fonte local verificada conforme Fonte alvo.
2. Abra o Codex no projeto alvo.
3. Cole [prompts/pt/00_install_codex_environment.md](prompts/pt/00_install_codex_environment.md).
4. Deixe o Codex instalar, verificar e relatar.

Fallback técnico:

Sem opcao de mutacao nem `--plan-out`, o instalador oferece uma previsualizacao somente leitura. `--write`, `--upgrade`, `--apply-plan` e `--restore` sao mutuamente exclusivos.

Usar o clone `SR_PACK_SOURCE` ja selecionado e verificado. Para uma versao publicada, clonar a fonte oficial se necessario e selecionar a referencia publicada validada; clonar nao seleciona o candidato SR 4. O candidato exige o conteudo local explicitamente autorizado. Definir `SR_TARGET` como caminho do projeto alvo antes dos comandos.

Novas instalacoes incluem `docs/codex/SR_PASSES.yaml`. SR Passes agrupa varios lotes SR em uma passagem limitada com ordem de dependencias, preflight compartilhado, validacoes humanas e testes E2E agrupados. Os lotes continuam sendo a unidade atomica em `SR_LOTS.yaml`.

O registro comeca com `passes: []`. Esse estado e valido: a instalacao nao inventa uma passagem de produto. O prompt `08` e usado depois de ler e validar os lotes.

## Atualizar

No projeto alvo, cole [prompts/pt/05_upgrade_codex_environment.md](prompts/pt/05_upgrade_codex_environment.md). O Codex deve auditar, preservar arquivos do projeto, apresentar o plano e só então aplicar o upgrade.

Contratos históricos `sr_contract` 3.0.0 continuam legíveis. Não reescreva task memories em massa: normalize apenas escopo ativo ou reaberto após ler sua fonte, preserve requirement IDs abertos e reabra o lote original por padrão. Um resultado verde em uma pasta não oculta problemas nas demais.

Layouts oficiais representativos SR 2.2.0, 2.3.0, 2.3.5, 2.4.1 e 3.0.0 sao cobertos por regressoes de upgrade. Se `SR_PASSES.yaml` estiver ausente, um registro valido `passes: []` e criado. Unknown/partial ou adaptacoes locais ainda exigem auditoria arquivo por arquivo. Codigo 0 do instalador nao basta: `sr_post_install_check.py` tambem deve ficar verde; caso contrario o alvo permanece em `repair`.

## Verificar

Cole [prompts/pt/06_verify_sr_installation.md](prompts/pt/06_verify_sr_installation.md).

Verifique tambem a documentacao de release e os prompts publicos:

```bash
python3 scripts/codex/validate_release_docs.py --root . --json
```

O Codex tambem deve validar as passagens se o arquivo existir:

```bash
python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml
```

## Definir lotes SR

Depois de enquadrar uma funcionalidade, use [prompts/pt/09_define_sr_lots_from_scope.md](prompts/pt/09_define_sr_lots_from_scope.md) para definir `SR_LOTS.yaml` com Lot Design Evidence Gate.

## Definir SR Passes

Depois use [prompts/pt/08_define_sr_passes_from_lots.md](prompts/pt/08_define_sr_passes_from_lots.md) para propor uma passe coerente em `SR_PASSES.yaml`. Estas etapas atualizam apenas a memoria SR e nao devem modificar codigo da aplicacao.

## Gerar um Pass Runtime Goal

Para uma passe validada, o Codex pode gerar o goal runtime limitado:

```bash
python3 scripts/codex/build_pass_runtime_goal.py --pass-id <PASS_ID> --output docs/codex/tasks/YYYY-MM-DD_<pass-id>/pass_runtime_goal.md
```

## Iniciar sessão

Cole [prompts/pt/01_start_sr_session.md](prompts/pt/01_start_sr_session.md). Para agentes IA runtime, use [prompts/pt/15_define_runtime_agents.md](prompts/pt/15_define_runtime_agents.md).
