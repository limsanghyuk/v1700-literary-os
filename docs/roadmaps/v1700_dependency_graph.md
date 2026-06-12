# V1700 Dependency Graph

Status: ACTIVE_GRAPH
Created: 2026-06-12
Scope: human-readable dependency graph for the current V1700 planning and implementation sequence.

## 1. Purpose

Record upstream and downstream dependencies among current V1700 roadmap artifacts.

## 2. Current root chain

```text
formula_signal_mapping_result
  -> writer_ide_static_flow_result
  -> manual_static_review_result
  -> writer_ide_advisory_panel_render_packet
  -> writer_ide_render_packet_review_result
  -> frontend_renderer_blueprint_packet
  -> frontend_component_contracts
```

## 3. Writer IDE branch

| Node | Depends on | Enables |
|---|---|---|
| `formula_signal_mapping_result.json` | option_b_validator_result | writer_ide_static_flow |
| `writer_ide_static_flow_result.json` | formula_signal_mapping_result | manual_static_review |
| `manual_static_review_result.json` | writer_ide_static_flow_result | advisory_panel_renderer |
| `writer_ide_advisory_panel_render_packet.json` | static_flow + manual_review | render_packet_review |
| `writer_ide_render_packet_review_result.json` | render_packet | frontend_renderer_blueprint |
| `frontend_renderer_blueprint_packet.json` | render_packet_review | frontend_component_contracts |

## 4. Formula measurement branch

| Node | Depends on | Enables |
|---|---|---|
| `formula_measurement_lab_blueprint.md` | formula_signal_mapping_result | formula_measurement_plan |
| `formula_measurement_plan.json` | measurement blueprint | human_rating_dataset |
| `coefficient_candidate_registry.json` | measurement plan | shadow_eval |
| `shadow_eval_report` | coefficient candidates | bounded update decision |

## 5. DB / RAG branch

| Node | Depends on | Enables |
|---|---|---|
| `canonical_record_store_rag_blueprint.md` | deficiency registry | canonical record contract |
| `canonical_record_store_contract.md` | DB/RAG blueprint | minimum records fixture |
| `rag_retrieval_packet_contract.md` | DB/RAG blueprint | RAG cases fixture |
| `minimum_records.json` | record contract | store validator |
| `minimum_retrieval_cases.json` | RAG contract | retrieval validator |

## 6. Agent Board branch

| Node | Depends on | Enables |
|---|---|---|
| `agent_board_blueprint.md` | frontend renderer blueprint | agent action contract |
| `agent_action_record_contract.md` | agent board blueprint | minimum agent action fixture |
| `minimum_agent_actions.json` | agent action contract | agent board packet builder |

## 7. Claude / MultiWork absorption branch

| Node | Depends on | Enables |
|---|---|---|
| `claude_multiwork_absorption_matrix.md` | V1700 lineage policy | project isolation cases |
| `project_isolation_cases.json` | absorption matrix | multiwork isolation validator |
| `shared_character_readonly_cases.json` | absorption matrix | read-only shared character audit |
| `AuthorLicense boundary contract` | rights registry | cross-work retrieval gate |

## 8. Global blockers

The following block promotion from blueprint to implementation:

```text
missing contract
missing fixture
missing validator or review
missing result artifact
boundary violation
human approval missing where required
GitNexus evidence gap if marked release-critical
```

## 9. Current next node

```text
frontend_component_contracts
```
