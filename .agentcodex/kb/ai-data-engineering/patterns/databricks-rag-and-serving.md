# Databricks RAG And Serving

## Purpose

Capture `data-agents` Databricks AI serving and retrieval guidance in the
AgentCodex AI data engineering KB.

## RAG Building Blocks

- documents stored in Unity Catalog Volumes
- parse/chunk pipeline
- Delta table with text, metadata, and embedding fields
- Vector Search endpoint and index
- retrieval query with filters
- serving endpoint or app layer
- evaluation dataset and trace review

## Vector Search Decisions

| Decision | Options |
|---|---|
| endpoint type | standard vs storage optimized |
| index source | Delta Sync vs Direct Access |
| embedding ownership | managed embeddings vs self-managed embeddings |
| retrieval mode | vector, hybrid, full-text where supported |
| update mode | triggered, continuous, or manual |

## Serving Decisions

- classic ML model vs custom pyfunc vs GenAI agent
- endpoint permission model
- request/response schema
- dependency packaging
- logging and trace capture
- evaluation and rollback plan

## Source Notes

- Enriched from `data-agents/skills/databricks/databricks-vector-search/`
- Enriched from `data-agents/skills/databricks/databricks-model-serving/`
- Enriched from `data-agents/skills/databricks/databricks-mlflow-evaluation/`
