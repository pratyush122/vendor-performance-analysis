# Resume-Ready Wording

## One-Line Project Title

Vendor Performance Analysis | SQL, Python, DuckDB, Power BI

## Resume Summary Version

Built an end-to-end vendor performance analytics project on large retail/wholesale data using SQL, Python, DuckDB, and Power BI. Designed a script-based ETL workflow, created a reusable vendor-brand analytics mart, quantified procurement concentration and unsold inventory risk, and produced dashboard-ready outputs with statistical validation.

## Resume Bullets

- Built a production-style analytics pipeline on `12.8M+` sales rows and `2.37M+` purchase rows using SQL, Python, and DuckDB, avoiding notebook-based large-data instability.
- Designed and materialized a vendor-brand analytics mart with `10,692` rows to support profitability, pricing, inventory, and vendor-dependency analysis.
- Identified `198` low-sales / high-margin brands for pricing and promotion opportunities and quantified `$9.55M` in unsold inventory exposure.
- Measured procurement concentration and found the top 10 vendors accounted for `65.69%` of purchase dollars, highlighting supply-chain concentration risk.
- Validated business insights with statistical testing, including a significant profit-margin difference between top and low performing vendor groups.
- Packaged the project with Power BI-ready datasets, DAX measures, dashboard specifications, automated tests, and stakeholder-facing reporting.

## GitHub Repo Description

End-to-end vendor performance analytics project using SQL, Python, DuckDB, and Power BI on large retail datasets.

## GitHub About Topics

- data-analytics
- sql
- python
- duckdb
- power-bi
- business-analysis
- etl
- data-visualization
- portfolio-project

## Interview Talking Points

1. I intentionally replaced notebook-heavy processing with a script-based pipeline because the dataset was large and needed a more stable workflow.
2. I separated raw views, staging summaries, and the final analytics mart so the downstream analysis and dashboard layer stayed fast and reproducible.
3. I focused the dashboard on business actions, not just charts: target brands, vendor concentration, pricing efficiency, and inventory risk.
4. I added validation layers recruiters care about: logging, tests, reproducibility, CI, and stakeholder-ready reporting.
