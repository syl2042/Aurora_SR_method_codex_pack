# Instalação

[English](INSTALLATION.md) |
[Francais](INSTALLATION.fr.md) |
[Deutsch](INSTALLATION.de.md) |
[Portugues](INSTALLATION.pt.md) |
[Espanol](INSTALLATION.es.md)

O fluxo recomendado é **prompt Codex primeiro**. Os scripts Python são ferramentas técnicas que o Codex pode executar após a inspeção.

## Instalar em um projeto alvo

1. Clone este repositório.
2. Abra o Codex no projeto alvo.
3. Cole [prompts/pt/00_install_codex_environment.md](prompts/pt/00_install_codex_environment.md).
4. Deixe o Codex instalar, verificar e relatar.

Fallback técnico:

```bash
export SR_PACK_SOURCE="$HOME/aurora-sr-method-pack"
git clone https://github.com/syl2042/Aurora_SR_method_codex_pack.git "$SR_PACK_SOURCE"
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target /path/to/project --profile default --write
```

## Atualizar

No projeto alvo, cole [prompts/pt/05_upgrade_codex_environment.md](prompts/pt/05_upgrade_codex_environment.md). O Codex deve auditar, preservar arquivos do projeto, apresentar o plano e só então aplicar o upgrade.

## Verificar

Cole [prompts/pt/06_verify_sr_installation.md](prompts/pt/06_verify_sr_installation.md).

## Iniciar sessão

Cole [prompts/pt/01_start_sr_session.md](prompts/pt/01_start_sr_session.md). Para agentes IA runtime, use [prompts/pt/15_define_runtime_agents.md](prompts/pt/15_define_runtime_agents.md).
