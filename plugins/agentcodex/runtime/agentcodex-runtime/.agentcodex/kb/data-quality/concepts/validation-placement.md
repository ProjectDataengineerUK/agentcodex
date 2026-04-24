# Validation Placement

Quality validation is most effective when placed at the layer where a failure is most actionable.

## Guidance

- source-shape checks belong near ingestion
- semantic model checks belong near marts or published datasets
- consumer-specific expectations should not always be global defaults

## Anti-Pattern

Applying every possible check at every layer and creating alert fatigue.
