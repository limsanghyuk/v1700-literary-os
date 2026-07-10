# Formula Signal Store Runtime Blueprint

Status: implementation-aligned blueprint  
Updated: 2026-06-16

## Purpose

This blueprint defines the first concrete runtime surface that sits on top of the corpus formula bridge.

The Formula Signal Store does not generate new story text.

It stores, validates, indexes, and exposes advisory formula signals so that later layers can query them deterministically.

## Inputs

- `release/current/corpus_formula_bridge_pack/formula_signal_registry.json`
- `release/current/corpus_formula_bridge_pack/corpus_formula_bridge_report.json`

## Outputs

- `release/current/formula_signal_store_pack/formula_signal_store_spec.json`
- `release/current/formula_signal_store_pack/formula_signal_validation_report.json`
- `release/current/formula_signal_store_pack/formula_signal_index.json`
- `release/current/formula_signal_store_pack/formula_signal_query_surface.json`
- `release/current/formula_signal_store_pack/writer_ide_advisory_cards.json`
- `release/current/formula_signal_store_pack/formula_signal_store_report.json`

## Runtime Meaning

The store is:

- read-only
- deterministic
- advisory-only
- canonical-state preserving

The store is not:

- a story mutation engine
- a hidden memory writer
- a live provider surface
- a training runtime

## Supported Query Filters

- `work_id`
- `formula_group`
- `review_status`
- `writer_ide_panel_ref`
- `min_confidence`

## First Consumers

- Value Proof Arm B guidance surfaces
- future LearnableCritic audited intake
- Writer IDE advisory cards

## Boundary Rule

The store may expose signals and summaries.

It may not mutate canonical story state.
