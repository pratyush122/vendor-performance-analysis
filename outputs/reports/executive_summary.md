# Vendor Performance Analysis

Generated at: `2026-04-11 19:41`

## Business Goal

Assess vendor performance across sales, profitability, purchasing efficiency, and inventory risk so the business can:

- identify low-sales / high-margin brands that need pricing or promotion changes
- understand which vendors drive most sales and procurement dependency
- verify whether bulk buying reduces unit cost
- flag slow-moving inventory and capital locked in unsold stock

## KPI Snapshot

- Total sales: `441,408,069.45`
- Total purchases: `307,338,437.47`
- Gross profit: `134,069,631.98`
- Average profit margin: `38.72%`
- Unsold inventory value: `9,553,539.19`
- Top-10 vendor purchase contribution: `65.69%`

## Executive Findings

1. `198` brands sit in the low-sales / high-margin zone, making them strong candidates for pricing experiments, promotion, and distribution support.
2. The highest selling vendor is `DIAGEO NORTH AMERICA INC` with `$67.99M` in sales, while the strongest brand is `Jack Daniels No 7 Black` at `$7.96M`.
3. Vendor concentration is material: the top 10 vendors contribute `65.69%` of purchase dollars.
4. The lowest observed inventory-turnover vendor in the bottom-10 slice is `ALISA CARR BEVERAGES` with an average turnover of `0.62`.
5. Capital locked in unsold inventory is `$9.55M`.

## Statistical Validation

- Bulk purchasing vs unit cost Spearman correlation: `-0.29`
- Bulk purchasing p-value: `0.0`
- Top-vendor profit margin 95% CI: `38.42` to `39.43`
- Low-vendor profit margin 95% CI: `30.06` to `36.23`
- Profit margin difference p-value: `0.00035255`

## Recommendations

1. Prioritize the low-sales / high-margin brands for promotional campaigns and controlled price tests.
2. Reduce vendor concentration risk by diversifying procurement away from the top concentration cluster where practical.
3. Use bulk-purchase agreements selectively on brands with proven sell-through to capture lower unit cost without inflating unsold inventory.
4. Review slow-moving vendors and brands for markdowns, bundle offers, or reduced replenishment cadence.
5. Use the exported Power BI dataset and DAX measures to track these KPIs continuously.