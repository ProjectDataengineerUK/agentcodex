# Key And Freshness Checks

A small number of well-chosen checks often creates more trust than a large noisy suite.

## Recommended Starting Set

- primary key uniqueness where the model promises it
- not-null on critical business keys
- freshness on time-sensitive published assets
- row-count or volume anomaly checks where appropriate
