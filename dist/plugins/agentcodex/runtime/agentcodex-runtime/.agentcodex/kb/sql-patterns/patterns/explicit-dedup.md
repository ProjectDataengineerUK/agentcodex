# Explicit Dedup

Deduplication should be visible and testable.

## Recommended Pattern

- choose the business rule for selecting the winning row
- encode that rule explicitly
- validate the result with data-quality checks where the contract matters
