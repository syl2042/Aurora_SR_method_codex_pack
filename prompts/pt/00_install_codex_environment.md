# Instalar a SR Method em um projeto alvo

Você está trabalhando em um repositório de software que deve receber a Aurora SR Method.

Objetivo: instalar a SR Method sem alterar código da aplicação, migrações, dependências, segredos ou regras de negócio.

Use o pacote fonte oficial:

```text
https://github.com/syl2042/Aurora_SR_method_codex_pack
```

Instruções:

1. Identificar ou clonar uma cópia local do pacote oficial.
2. Inspecionar o repositório alvo antes de qualquer mudança.
3. Explicar o escopo da instalação e aguardar validação explícita do usuário se houver mutação.
4. Executar o instalador com o perfil `default` após validação.
5. Executar scripts de verificação após a instalação, incluindo `validate_pass_contract.py` para `SR_PASSES.yaml`.
6. Verificar que `SR_PASSES.yaml` foi instalado e recomendar `prompts/pt/08_define_sr_passes_from_lots.md` depois que os lotes forem definidos.
7. Relatar arquivos adicionados, verificações executadas, warnings e próximos passos.

Não altere código da aplicação. Não crie migrações. Não toque em segredos. Não invente regras do projeto.
