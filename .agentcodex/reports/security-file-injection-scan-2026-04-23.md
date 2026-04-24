# Security Scan Report

- generated_at: 2026-04-23
- scope: varredura manual focada em injecao/manipulacao insegura de arquivos
- repository: agentcodex
- analyst: Codex

## Objetivo

Verificar vetores de injeção e manipulação insegura de arquivos, com foco em:

- path traversal
- leitura/escrita com caminho controlado por entrada
- operações destrutivas em diretórios derivados de input
- fluxos de archive/copy/move/rmtree sem contenção de raiz

## Achados

### 1. Alto: path traversal via `workflow_run_id`

Status atual: corrigido

Arquivo: `scripts/workflow_orchestrator.py`

Trechos originais relevantes:

- `workflow_root_path()` construía caminhos com `WORKFLOWS_ROOT / workflow_run_id`
- `workflow_state_path()` derivava `state.json` a partir desse caminho
- `load_state()` e `save_state()` consumiam esse path sem validação adicional

Referências:

- `scripts/workflow_orchestrator.py:107`
- `scripts/workflow_orchestrator.py:117`
- `scripts/workflow_orchestrator.py:121`
- `scripts/workflow_orchestrator.py:128`

Risco original:

Um `workflow_run_id` contendo segmentos como `../` pode escapar da árvore `.agentcodex/workflows` e atingir leitura/escrita fora da área esperada, dependendo do comando acionado.

Superfície impactada:

- `workflow-status`
- `resume-workflow`
- `workflow-note`
- `workflow-handoff`
- `start-stage`
- `complete-stage`
- `advance-stage`
- `workflow-next`
- `workflow-close`
- `workflow-archive`

Referências:

- `scripts/workflow_orchestrator.py:455`
- `scripts/workflow_orchestrator.py:461`
- `scripts/workflow_orchestrator.py:480`
- `scripts/workflow_orchestrator.py:509`
- `scripts/workflow_orchestrator.py:540`
- `scripts/workflow_orchestrator.py:567`
- `scripts/workflow_orchestrator.py:609`
- `scripts/workflow_orchestrator.py:625`
- `scripts/workflow_orchestrator.py:642`

### 2. Medio: sink destrutivo herdando o mesmo problema no fluxo de archive

Status atual: corrigido

Arquivo: `scripts/workflow_orchestrator.py`

Trechos originais relevantes:

- `source_root = workflow_root_path(workflow_run_id)`
- `target_root = ARCHIVE_ROOT / workflow_run_id`
- `shutil.rmtree(target_root)` quando o destino existe
- `shutil.move(str(source_root), str(target_root))`

Referências:

- `scripts/workflow_orchestrator.py:623`
- `scripts/workflow_orchestrator.py:624`
- `scripts/workflow_orchestrator.py:629`
- `scripts/workflow_orchestrator.py:631`

Risco original:

Se o identificador do workflow for aceito sem normalização/containment, o fluxo de archive pode operar sobre caminhos fora da área gerenciada e ampliar o impacto com remoção de diretório e movimentação de árvore.

## Correcao aplicada

Arquivo: `scripts/workflow_orchestrator.py`

Controles adicionados:

- `validate_workflow_run_id()` restringe `workflow_run_id` a caracteres seguros e rejeita `/`, `\\`, `..` e caminhos absolutos
- `ensure_within_root()` resolve o caminho final e exige contenção explícita dentro do root gerenciado
- `workflow_dir_for_root()` centraliza a construção segura de caminhos para `WORKFLOWS_ROOT` e `ARCHIVE_ROOT`
- `workflow_root_path()` e `workflow_archive()` passaram a usar os helpers seguros antes de leitura, escrita, `rmtree` e `move`
- `main()` trata `ValueError` e retorna erro limpo no CLI para IDs inválidos

Referências:

- `scripts/workflow_orchestrator.py:77`
- `scripts/workflow_orchestrator.py:91`
- `scripts/workflow_orchestrator.py:101`
- `scripts/workflow_orchestrator.py:155`
- `scripts/workflow_orchestrator.py:642`
- `scripts/workflow_orchestrator.py:718`

## Validacao executada

Cobertura adicionada:

- `.agentcodex/tests/test_workflow_orchestrator.py:20` valida rejeição de path traversal em `workflow_run_id`
- `.agentcodex/tests/test_workflow_orchestrator.py:27` valida listagem com runs apenas arquivados
- `.agentcodex/tests/test_workflow_orchestrator.py:56` valida geração de `workflow_run_id` com sufixo incremental em colisão

Execuções realizadas:

- `python3 -m unittest discover -s .agentcodex/tests -p 'test_workflow_orchestrator.py'` -> `OK`
- `python3 scripts/agentcodex.py workflow-status ../escape` -> bloqueado por validação de `workflow_run_id`
- teste operacional completo de `workflow-close` + `workflow-archive` em workflow `wf-pipeline`
- teste operacional completo de `workflow-close` + `workflow-archive` em workflow `wf-backlog-to-define`

Evidência operacional:

- após `workflow-archive`, `spec_path` e `state_path` passaram a resolver sob `.agentcodex/archive/workflows/<workflow-run-id>/`
- `list-workflows` passou a listar runs arquivados mesmo quando apenas o root de archive contém estado

## Pontos revisados sem achado relevante

Os arquivos abaixo apresentaram validação de raiz/escopo melhor definida na superfície revisada:

- `scripts/promote_kb_update.py`
- `scripts/memory_candidate_flow.py`

Observação:

Esses fluxos usam `resolve()` e checagem com `relative_to()` para restringir caminhos a roots aprovadas.

## Recomendação

Manter os controles atuais e acrescentar:

- testes adicionais para fluxos de erro do CLI e colisões repetidas acima de `-2`
- revisão futura para concorrência entre criações simultâneas do mesmo prompt, caso o orquestrador passe a operar em ambiente multi-processo
- revisão periódica de outras superfícies que derivem caminhos a partir de identificadores externos

## Status

- correção aplicada e validada
- risco principal de traversal e sink destrutivo mitigado no orquestrador atual
- repositório sem `.git` acessível no diretório analisado, então não houve comparação com histórico local
