# Aurora SR Method Codex Pack

[English](README.md) |
[Francais](README.fr.md) |
[Deutsch](README.de.md) |
[Portugues](README.pt.md) |
[Espanol](README.es.md)

[Dar uma estrela ao repositório](https://github.com/syl2042/Aurora_SR_method_codex_pack/stargazers) |
[Documentação](https://docs.auroramind.fr/docs/SR_Method) |
[Instalar com Codex](INSTALLATION.pt.md) |
[Atualizar projeto](prompts/pt/05_upgrade_codex_environment.md) |
[Verificar instalação](prompts/pt/06_verify_sr_installation.md)

## O que é

Aurora SR Method Codex Pack é um pacote fonte público para instalar um método de trabalho Codex governado em projetos de software.

SR significa **Specification Runtime**. O método fornece ao Codex um quadro operacional local ao projeto: regras de bootstrap, modelos de memória de tarefa, evidence gates, repo maps, prompts controlados, scripts de validação e method skills reutilizáveis.

```text
Clonar pacote -> Colar prompt Codex -> Instalar SR Method -> Verificar -> Desenvolver com governança
```

## Política de idioma

O núcleo da SR Method é mantido em inglês como idioma técnico canônico.

Os pontos de entrada para desenvolvedores estão disponíveis em vários idiomas: READMEs, guias de instalação e prompts Codex copiáveis.

Um projeto instalado pode instruir o Codex a falar com o usuário em português. O núcleo técnico permanece em inglês.

## Início rápido

1. Clone este repositório.
2. Abra o Codex no projeto alvo.
3. Cole o prompt de instalação em português.
4. Deixe o Codex inspecionar, instalar, verificar e relatar.

Prompts principais:

| Ação | Prompt |
| --- | --- |
| Instalar | [00](prompts/pt/00_install_codex_environment.md) |
| Iniciar sessão | [01](prompts/pt/01_start_sr_session.md) |
| Atualizar | [05](prompts/pt/05_upgrade_codex_environment.md) |
| Verificar | [06](prompts/pt/06_verify_sr_installation.md) |
| Definir agentes runtime | [15](prompts/pt/15_define_runtime_agents.md) |

Os comandos Python são ferramentas técnicas ou fallback. O fluxo recomendado é prompt-first com Codex.

## Conteúdo público

```text
core/             núcleo canônico em inglês e templates
prompts/          prompts raiz e entradas multilíngues
scripts/          instalação, auditoria e validação
skills-method/    method skills Codex reutilizáveis
blueprints/       templates de lots, inbox, tasks e skills
profiles/         perfis genéricos
project-skills/   espaço para skills locais do projeto
adr/              template ADR
```

O repositório público não publica estado de projeto, tasks históricas, `.docx`, handoffs locais, caminhos de clientes ou dados de projetos.

## Licença

MIT License. Veja [LICENSE](LICENSE).
