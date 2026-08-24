# Definir SR Passes a partir dos lotes existentes

Voce esta trabalhando em um repositorio ja equipado com a SR Method.

Objetivo: propor ou atualizar `docs/codex/SR_PASSES.yaml` a partir de `docs/codex/SR_LOTS.yaml`, sem modificar codigo da aplicacao.

Priorize lotes `repair`/`reopened`, preserve todos os `validated_request_ids` abertos e consolide reparos do mesmo escopo de produto em uma passagem coerente.

Regras:

- Nao modifique codigo da aplicacao.
- Nao altere nenhum status de lote sem evidencia e validacao.
- Nao marque uma passagem como `validated` sem validacao explicita do usuario.
- Uma passagem agrupa lotes; ela nunca substitui criterios ou gates dos lotes.

Fontes a ler:

1. `AGENTS.md`
2. `docs/codex/SR_HARNESS_METHOD.md`
3. `docs/codex/LOT_EXECUTION_METHOD.md`
4. `docs/CURRENT_STATE.md`
5. `docs/codex/SR_LOTS.yaml`
6. `docs/codex/SR_PASSES.yaml` se existir
7. `docs/codex/CODEBASE_MAP.md`

Metodo:

1. Validar `SR_LOTS.yaml`.
2. Classificar lotes por status e dependencias.
3. Verificar o Lot Design Evidence Gate: excluir de passagens executaveis qualquer lote `planned`, `validated`, `in_progress`, `repair` ou `reopened` sem `design_evidence.status: pass` ou `not_applicable` justificado. Um lote `proposed` pode permanecer exploratorio.
4. Construir o grafo `depends_on`, `blocked_by`, `impacts`, `impacted_by`.
5. Propor passagens com ordem, rationale, preflight, validacoes humanas, migracoes/acoes externas, fontes compartilhadas, E2E agrupado e stop conditions.
6. Criar ou atualizar `SR_PASSES.yaml` somente apos validacao se o projeto impuser validacao estrita.
7. Validar com `python3 scripts/codex/validate_pass_contract.py --file docs/codex/SR_PASSES.yaml --lots-file docs/codex/SR_LOTS.yaml`.

Saida esperada:

- passagens propostas;
- lotes excluidos e razao;
- lotes excluidos por Lot Design Evidence Gate ausente ou incompleto;
- perguntas bloqueantes;
- preflight por passagem;
- E2E agrupado recomendado;
- arquivos SR modificados;
- resultado de validacao;
- proxima passagem recomendada.
