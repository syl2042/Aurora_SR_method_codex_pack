# Verificar uma instalação SR Method

Você está trabalhando em um repositório equipado com a Aurora SR Method.

Objetivo: verificar se a instalação ou upgrade está completo, coerente e utilizável antes de retomar o desenvolvimento.

Instruções:

1. Executar `python3 scripts/codex/verify_codex_pack.py`.
2. Executar `python3 scripts/codex/audit_codex_pack.py --root . --json`.
3. Executar `python3 scripts/codex/sr_post_install_check.py --root . --json` se disponível.
4. Validar contratos lot, loop e SR quando os scripts existirem.
5. Classificar warnings restantes como aceitáveis, a documentar, a corrigir com validação ou bloqueantes.
6. Relatar versão, verificações, erros, warnings e próxima ação recomendada.

Esta não é uma tarefa de desenvolvimento da aplicação.
