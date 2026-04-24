# Reliable Batch Job

Reliable Spark batch jobs should separate:

- configuration
- IO boundaries
- transformation logic
- operational error handling

## Recommended Pattern

- keep source reads isolated
- keep business transforms explicit
- make write behavior idempotent when possible
- surface metrics and failure points clearly
