# Instalar SR 3.7 em um projeto alvo novo

Objetivo verificável: instalar SR Pack 3.7.0 com `sr_contract` 3.1.0, `loop_contract` 1.1, `SR_LOTS` 0.4 e `SR_PASSES` 0.2, verificar e parar antes de qualquer desenvolvimento da aplicação.

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
