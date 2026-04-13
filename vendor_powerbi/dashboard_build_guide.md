# Power BI Build Guide

## 1. Import the Right Dataset

Use:

- Main model: `outputs/powerbi/vendor_performance_dashboard_ready.csv`
- Optional helper tables:
  - `outputs/tables/top_vendor_purchase_contribution.csv`
  - `outputs/tables/target_brands.csv`
  - `outputs/tables/low_inventory_turnover_vendors.csv`
  - `outputs/tables/unsold_inventory_exposure.csv`

If you want a cleaner model, start only with `vendor_performance_dashboard_ready.csv`.

## 2. Apply the Theme

In Power BI Desktop:

1. Go to `View`
2. Select `Browse for themes`
3. Import `vendor_powerbi/theme_modern.json`
4. Optional but recommended: set `vendor_powerbi/dashboard_background.svg` as the page wallpaper for all report pages

## 3. Load the Measures

Create a new measure table and paste the DAX from:

- `vendor_powerbi/measures.dax`

Recommended measure table name:

- `Measures`

## 4. Format the Data Model

Set these data categories/formats:

- `total_sales_dollars`: Currency
- `total_purchase_dollars`: Currency
- `gross_profit`: Currency
- `gross_profit_after_freight`: Currency
- `vendor_freight_cost_total`: Currency
- `freight_cost`: Currency
- `unsold_inventory_value`: Currency
- `profit_margin`: Percentage with 2 decimals
- `net_profit_margin`: Percentage with 2 decimals
- `stock_turnover`: Decimal with 2 decimals
- `sales_to_purchase_ratio`: Decimal with 2 decimals

Sort fields:

- sort visuals by metric descending unless the page calls for bottom performers

## 5. Build Page 1: Executive Control Tower

Layout:

- top row: title band
- second row: 6 KPI cards
- bottom left: Top Vendors by Sales
- bottom middle: Top Brands by Sales
- bottom right: Purchase Contribution combo chart + donut

Cards:

- `[Total Sales Dollars]`
- `[Total Purchase Dollars]`
- `[Gross Profit]`
- `[Gross Profit After Freight]`
- `[Net Profit Margin]`
- `[Unsold Inventory Value]`

Formatting:

- card background: white
- corner radius: 12
- callout font: 24 to 30
- category label: small uppercase style
- add subtle shadow only

## 6. Build Page 2: Vendor Performance Matrix

Scatter visual:

- X axis: `[Total Purchase Dollars]`
- Y axis: `[Gross Profit After Freight]`
- Size: `[Total Sales Dollars]`
- Legend: `performance_flag`
- Details: `vendor_name`

Add a ranked table on the right with:

- vendor_name
- `[Total Sales Dollars]`
- `[Gross Profit After Freight]`
- `[Net Profit Margin]`
- `[Average Stock Turnover]`
- `[Purchase Contribution %]`

Add two bars at the bottom:

- lowest stock turnover vendors
- highest unsold inventory value vendors

## 7. Build Page 3: Pricing and Promotion Lab

Scatter visual:

- X: `total_sales_dollars`
- Y: `profit_margin`
- Details: `description`
- Legend: `performance_flag`

Add filters:

- exclude extreme outliers visually if needed using visual-level filters

Add:

- Top Brands by Sales bar chart
- Unit Purchase Cost by Order Size box plot or custom visual
- table of target brands with:
  - description
  - total_sales_dollars
  - profit_margin
  - gross_profit

## 8. Build Page 4: Inventory and Risk Monitor

Add:

- donut: top 10 vendor purchase contribution vs others
- waterfall: `[Gross Profit]` to `[Gross Profit After Freight]`
- bar chart: unsold inventory by vendor
- KPI mini-cards:
  - `[Top 10 Purchase Contribution %]`
  - `[Vendor HHI]`
  - `[Low Sales High Margin Brand Count]`
  - `[Distinct Vendors]`
  - `[Distinct Brands]`

## 9. Build Page 5: Vendor Drillthrough

Create a drillthrough page filtered by `vendor_name`.

Include:

- KPI strip for selected vendor
- brand-level table
- brand sales vs margin scatter
- unsold inventory by brand

This page is a strong interview feature because it shows interactive thoughtfulness beyond a single static dashboard.

## 10. Build Tooltips

Create a report page tooltip with:

- `[Total Sales Dollars]`
- `[Gross Profit After Freight]`
- `[Net Profit Margin]`
- `[Average Stock Turnover]`
- `[Unsold Inventory Value]`

Assign it to:

- vendor bar charts
- brand scatter plots
- vendor scatter plots

## 11. Finishing Touches

- keep titles short
- remove unnecessary gridlines
- use navy for core charts and coral only for risk states
- do not overuse donuts
- use aligned spacing and equal card widths
- keep slicers in a slim header band, not floating randomly

## 12. Final Recruiter Checklist

- 5 pages max
- drillthrough works
- tooltips work
- KPIs are formatted consistently
- no default Power BI blue everywhere
- charts answer business questions directly
- every page has a clear purpose
