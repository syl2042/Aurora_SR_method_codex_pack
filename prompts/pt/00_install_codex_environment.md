# Instalar SR 4.0.0 em um projeto alvo novo

## SR 4.0.0 — versao publicada

Fonte alvo: selecionar explicitamente `SR_PACK_SOURCE`, uma versao publicada identificada ou o candidato local SR 4.0.0 autorizado. Ler `core/SR_PACK_VERSION.json` (`version`, `release_status`); registrar `source_commit`, estado Git e, havendo alteracoes locais, uma impressao do conteudo incluindo arquivos fonte nao rastreados utilizados. Nao apresentar um candidato `unreleased` como release. Nao substituir o candidato por um clone da ultima versao publicada; se a fonte solicitada faltar, parar e esclarecer antes de instalar.

Para este alvo SR 4.0.0, a fonte deve declarar `version: 4.0.0`. Se nao houver release 4.0.0 publicada, usar somente o candidato local autorizado ou informar sua ausencia; nunca instalar outra versao silenciosamente.

Previsualizar com o comando abaixo antes da validacao; depois de `je valide`, escolher apenas o modo correspondente. `--plan-out` escreve um plano local e exige autorizacao; `--apply-plan` rejeita diagnosticos desatualizados. `--restore` e uma operacao separada com o diario exato da transacao e rejeita edicoes posteriores. Nao excluir arquivos para contornar conflitos.

Planos salvos contem arquivos: mante-los localmente. Definir `SR_TARGET` como caminho do repositorio alvo.

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
```

Objetivo verificável: instalar SR Pack 4.0.0 com `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 e `SR_PASSES` 0.2, verificar e parar antes de qualquer desenvolvimento da aplicação.

Instale `SR_PASSES.yaml` com `passes: []`. Esse registro vazio é válido: uma instalação nova não deve inventar uma passagem de produto. O prompt `08` propõe as passagens depois de ler os lotes e obter validação humana.

Use somente `https://github.com/syl2042/Aurora_SR_method_codex_pack`.

Regras estritas:

- Não altere código da aplicação, migrações, dependências, segredos, configuração ou regras de negócio.
- Inspecione primeiro o repositório alvo e o `AGENTS.md` mais próximo.
- Se `docs/codex/SR_PACK_VERSION.json`, `docs/codex/SR_METHOD.md` ou `docs/codex/SR_LOTS.yaml` existir, não é instalação nova. Pare e use `05_upgrade_codex_environment.md`.
- Antes da mutação, informe arquivos novos, existentes e preservados, além dos checks previstos; aguarde a validação humana exigida.
- Não invente `validated_requests`, lotes validados ou passes executáveis. Templates não são escopo de produto validado.
- Nunca use `--write` em projeto SR existente; use `--upgrade` somente após auditoria por projeto.

Após validação:

1. Registrar o clone local verificado e seu commit; classificar o alvo como `fresh_install`.
2. Executar o instalador com `--profile default --write`.
3. Verificar versão, lotes/passes, templates de tarefa, validadores e prompts `01`, `05`, `06`, `07`, `08`, `09`.
4. Confirmar que `sr_contract.json` separa `implementation_status` de `evidence_status`, inclui `validated_requests` granulares e Completion Gate derivado.
5. Verificar `CHANGELOG.md`, prompts publicos localizados e executar `audit_codex_pack.py`, `sr_post_install_check.py`, `validate_release_docs.py` e os validadores de lote, pass, loop e SR.
6. Não gerar `/goal`. Recomendar primeiro `09_define_sr_lots_from_scope.md` e depois `08_define_sr_passes_from_lots.md`.
7. Informar classificação, versão, commit, arquivos, checks, warnings e confirmar que nenhum código da aplicação mudou.

Fim obrigatório: instalar o método não valida nenhum escopo de produto.

Percursos: instalacao nova `00 -> 06`; instalacao existente `05 -> 06 -> 07`. O prompt `06` somente verifica; `07` propoe o realinhamento e espera `je valide` antes de alterar a memoria. Nenhum percurso autoriza desenvolvimento da aplicacao.
