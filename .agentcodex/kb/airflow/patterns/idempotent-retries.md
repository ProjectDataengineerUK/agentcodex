# Idempotent Retries

Retries only help when repeated execution is safe.

## Recommended Pattern

- define task side effects clearly
- isolate writes where possible
- make duplicate execution behavior explicit
