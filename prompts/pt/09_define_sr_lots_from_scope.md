# Definir lotes SR a partir do escopo ou inbox

Objetivo: transformar um enquadramento, pedido do usuario ou `docs/codex/SR_INBOX.yaml` em lotes SR explicitos em `docs/codex/SR_LOTS.yaml`, sem modificar codigo da aplicacao.

Antes de criar um lote, verifique objetivos, criterios de aceitacao, `validated_requests`, lotes `user_testing` e passagens validadas. Escopo existente e por padrao `existing_requirement_repair` e reabre o lote original. Um lote novo exige justificativa explicita fora do escopo; nao crie um micro-lote por criterio.

Regras:

- Nao modifique codigo da aplicacao.
- Nao crie um lote `planned`, `validated`, `in_progress`, `repair` ou `reopened` sem Lot Design Evidence Gate.
- Um lote `proposed` pode permanecer exploratorio.
- Nunca marque um lote como `validated` sem validacao explicita do usuario.

Metodo:

1. Ler `AGENTS.md`, `docs/codex/SR_BOOTSTRAP.md`, `docs/codex/SR_HARNESS_METHOD.md`, `docs/codex/LOT_EXECUTION_METHOD.md`, `docs/CURRENT_STATE.md`, `docs/codex/SR_INBOX.yaml`, `docs/codex/SR_LOTS.yaml` e `docs/codex/CODEBASE_MAP.md` quando existirem.
2. Identificar superficies candidatas com `RepoMap/KG -> arquivos candidatos -> leitura do codigo real -> testes/logs`.
3. Preencher `design_evidence` para cada lote candidato.
4. Manter em `proposed` qualquer lote cujo enquadramento ainda dependa de uma suposicao verificavel.
5. Propor os lotes para validacao antes da execucao.
6. Validar `SR_LOTS.yaml` com `python3 scripts/codex/validate_lot_contract.py --file docs/codex/SR_LOTS.yaml`.
7. Recomendar depois `docs/codex/prompts/08_define_sr_passes_from_lots.md` se houver varios lotes executaveis ou quase executaveis.

Saida esperada: lotes criados ou modificados, status do Lot Design Evidence Gate, arquivos lidos, hipoteses restantes, perguntas bloqueantes, validacao de `SR_LOTS.yaml`, proxima etapa.
