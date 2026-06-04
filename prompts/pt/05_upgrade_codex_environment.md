# Atualizar um projeto para a SR Method mais recente

Você está trabalhando em um repositório que já possui uma versão antiga da Aurora SR Method.

Objetivo: auditar e atualizar o SR pack sem alterar código da aplicação nem sobrescrever adaptações do projeto.

Use o pacote fonte oficial:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Instruções:

1. Detectar a versão SR instalada.
2. Verificar ou clonar o pacote fonte oficial.
3. Identificar arquivos do projeto a preservar: `AGENTS.md`, `DESIGN.md`, `docs/CURRENT_STATE.md`, `docs/codex/tasks/`, skills do projeto e decisões locais.
4. Explicar o plano de upgrade e aguardar validação explícita antes de mutação.
5. Aplicar o upgrade com o instalador somente após validação.
6. Executar scripts de auditoria e validação.
7. Relatar commit fonte, arquivos atualizados, arquivos preservados, backups, warnings e próximos passos.

Não altere código da aplicação, dependências, migrações ou segredos.
