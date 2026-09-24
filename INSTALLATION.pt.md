# Instalação — SR Method 4.1

Estado: versão publicada `4.1.0`. Selecionar explicitamente `SR_PACK_SOURCE` e registrar `release_status`, `source_commit` e o estado Git.

[English](INSTALLATION.md) · [Français](INSTALLATION.fr.md) · [Deutsch](INSTALLATION.de.md) · [Español](INSTALLATION.es.md)

## Escolher pelo estado observado

| Estado do destino | Prompt | Modo |
|---|---|---|
| Sem marcador SR | `prompts/pt/00_install_codex_environment.md` | `--write` |
| Com marcador SR, parcial ou desconhecido | `prompts/pt/05_upgrade_codex_environment.md` | `--upgrade` |

A versão anterior nunca define o algoritmo. Revisar a prévia, os conflitos e os arquivos preservados antes de aplicar:

```bash
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --json
python3 "$SR_PACK_SOURCE/scripts/install_codex_pack.py" --source "$SR_PACK_SOURCE" --target "$SR_TARGET" --upgrade
python3 "$SR_TARGET/scripts/codex/sr_post_install_check.py" --root "$SR_TARGET" --json
```

Para um destino novo, usar `--write` em vez de `--upgrade`. A transação salva os arquivos alterados, detecta mudanças concorrentes e permite `--restore` exato.

O post-check é somente leitura por padrão. Usar `--write-report` apenas quando um artefato de auditoria persistente for solicitado.

O conteúdo gerido converge, o estado do projeto é preservado, personalizações desconhecidas são reportadas como conflito e arquivos obsoletos só são removidos quando seu conteúdo é reconhecido como gerido. Código do produto, segredos, migrações, deploys, requisitos abertos e históricos de `SR_LOTS.yaml`/`SR_PASSES.yaml` não são alterados.

Uma instalação nova inclui `SR_PASSES.yaml` com `passes: []`, `MCP_POLICY.yaml` e `task_state.yaml`. Após verificação correta, usar `prompts/pt/07_realign_sr_state_after_upgrade.md` somente se o estado do projeto precisar de realinhamento. A definição de passes permanece em `08_define_sr_passes_from_lots.md`, os lotes em `09_define_sr_lots_from_scope.md`; `build_pass_runtime_goal.py` continua como ferramenta legacy opcional.
