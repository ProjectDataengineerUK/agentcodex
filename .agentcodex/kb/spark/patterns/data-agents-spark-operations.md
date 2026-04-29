# Data Agents Spark Operations

## Purpose

Add Spark operating guidance from `data-agents` where it complements existing
AgentSpec-derived Spark KB pages.

## Performance Review Points

- check partitioning and shuffle behavior before changing cluster size
- avoid wide transformations without understanding data skew
- inspect query plan for repeated scans, unnecessary joins, and expensive UDFs
- prefer built-in Spark SQL functions over Python UDFs where possible
- cache only when reuse is clear and memory pressure is understood

## Streaming Review Points

- define checkpoint location and retention
- bound stream-stream joins by event time
- account for late-arriving data
- isolate side effects in `foreachBatch`
- document trigger choice and cost implication

## Delta Review Points

- define table ownership and retention
- enable change data feed only when downstream consumers need it
- use schema evolution deliberately, not as a blanket setting
- prefer modern clustering/layout strategy over legacy tuning by habit

## Source Notes

- Enriched from `data-agents/kb/spark-patterns/`
- Enriched from `data-agents/skills/patterns/spark-patterns/`
