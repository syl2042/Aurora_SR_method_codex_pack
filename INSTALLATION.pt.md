# Instalação

[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

O fluxo recomendado é **prompt Codex primeiro**. Os scripts Python são ferramentas técnicas que o Codex pode executar após a inspeção.

## Escolher primeiro o percurso correto

- Sem marcador SR: prompt `00`, instalar SR 3.7.0 com `--write`.
- Marcador SR existente, antigo ou parcial: prompt `05`, auditar e atualizar de forma aditiva com `--upgrade`.
- Vários repositórios: ler versão e marcadores de cada alvo, criar uma matriz por repositório e executar um `--upgrade` por alvo. Nunca supor versão comum.

A instalação nova usa `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 e `SR_PASSES` 0.2. `implementation_status` e `evidence_status` ficam separados. A instalação não inventa `validated_requests` nem lotes de produto validados. O instalador recusa `--write` se detectar instalação SR existente.

## Instalar em um projeto alvo

1. Clone este repositório.
2. Abra o Codex no projeto alvo.
3. Cole [prompts/pt/00_install_codex_environment.md](prompts/pt/00_install_codex_environment.md).
4. Deixe o Codex instalar, verificar e relatar.

Fallback técnico:

Sem `--write` nem `--upgrade`, o instalador apenas mostra uma prévia somente leitura. Os dois modos de mutação são mutuamente exclusivos.

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target /path/to/project --profile default --write
```

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
