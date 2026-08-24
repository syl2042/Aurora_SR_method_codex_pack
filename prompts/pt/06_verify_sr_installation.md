# Verificar uma instalacao da SR Method

Nao modifique arquivos.

Objetivo: provar que cada instalacao ou upgrade esta completa, coerente e utilizavel antes de retomar o desenvolvimento da aplicacao.

1. Ler os marcadores reais de `AGENTS.md`, `docs/codex/SR_PACK_VERSION.json`, metodo, contratos, lotes, passes e task memories. Nao inferir a versao de uma pasta a partir de outra.
2. Executar `python3 scripts/codex/verify_codex_pack.py`.
3. Executar `python3 scripts/codex/validate_release_docs.py --root . --json`.
4. Executar `python3 scripts/codex/audit_codex_pack.py --root . --json`.
5. Executar `python3 scripts/codex/sr_post_install_check.py --root . --json`.
6. Executar `python3 scripts/codex/audit_sr_task_contracts.py --root . --json`.
7. Validar `SR_LOTS.yaml`, `SR_PASSES.yaml`, loop contracts ativos e o SR Contract 3.1.0 ou contratos legacy 3.0.0 explicitamente identificados.
8. Verificar `docs/codex/CHANGELOG.md`, versao alvo, prompts publicos localizados e preservacao aditiva dos arquivos do projeto.

Classificar cada warning como estado legacy compativel, divida documental, `repair` ou bloqueio externo real. Codigo `0` do instalador nao basta.

Informar por repositorio versao, controles, erros, warnings, contratos, `validated_requests` abertas, evidencias pendentes e proxima acao. `user_testing` so vale para trabalho tecnicamente completo; implementacao ausente permanece `repair`.

Parar sem corrigir e pedir validacao exata para qualquer reparacao.
