# Query Grain

Analytical SQL becomes fragile when the intended grain is implicit.

## Guidance

- state the row meaning before optimizing the query
- make deduplication and aggregation boundaries obvious
- review join logic through the lens of grain changes
