# Aurora SR Method Codex Pack

SR Method 4.1 é um harness de execução enxuto para Codex: núcleo permanente curto, procedimentos condicionais, gatilhos exatos de skills, estado compacto e verificação final proporcional.

Estado: **4.1.0 (`released`)**, publicada em 2026-09-24.

[English](README.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · **PT**

[Instalação](INSTALLATION.pt.md) · [Changelog](CHANGELOG.md) · [Prompt de instalação](prompts/pt/00_install_codex_environment.md) · [Prompt de atualização](prompts/pt/05_upgrade_codex_environment.md) · [Verificar](prompts/pt/06_verify_sr_installation.md) · [Realinhar](prompts/pt/07_realign_sr_state_after_upgrade.md)

## Mudanças na 4.1

- `AGENTS.md` é reconciliado e reduzido em vez de acumular outro manual.
- O catálogo cognitivo padrão fica limitado a lotes, diagnóstico, arquitetura e QA visual de UI.
- TDD, planejamento em arquivos, compactação do terminal, revisão de diff e RepoMap são mecanismos do harness, não skills.
- Não há testes deliberadamente falhos, gates vermelhos artificiais ou ciclos de rollback de desenvolvimento.
- Scope, Verification e Activation são os únicos limites de execução.
- Novas tarefas podem usar um `task_state.yaml` compacto; contratos antigos continuam legíveis.
- O modo `core` não chama MCP. `nexus_kg` segue `MCP_POLICY.yaml`, com ativação tardia, allowlists, aprovações e limites de resultado.
- Entrada, leitura/escrita de cache, ocupação do contexto, saída e resultados de ferramentas são medidos separadamente.

## Operação e atualização

```text
AGENTS.md -> SR_ROUTES.json -> apenas o procedimento acionado
          -> 0 a 2 skills especializadas -> fontes reais
          -> verificação final proporcional
```

A atualização é agnóstica à versão anterior: essa versão serve apenas como proveniência. O conteúdo real é classificado como ausente, gerido, alterado localmente, externo, obsoleto, conflitante ou já alinhado. O estado do projeto é preservado; um artefato obsoleto só é removido quando seu conteúdo é reconhecido como gerido.

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Detalhes: [INSTALLATION.pt.md](INSTALLATION.pt.md). Histórico e migrações ficam somente em [CHANGELOG.md](CHANGELOG.md).
