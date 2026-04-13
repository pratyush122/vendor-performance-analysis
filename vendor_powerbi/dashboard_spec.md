# Power BI Dashboard Spec

## Design Direction

This dashboard should feel like an executive control room, not a default BI canvas.

- Background: soft slate `#F4F7FB`
- Primary ink: deep navy `#12344D`
- Accent: teal `#1F7A8C`
- Highlight: amber `#F4B942`
- Positive: emerald `#1A936F`
- Risk: coral `#D95D39`
- Font: `Segoe UI Semibold` for titles, `Segoe UI` for body
- Borders: minimal
- Shadows: subtle only on KPI cards
- Shapes: rounded rectangles with clean spacing

## Recommended Canvas

- Page size: `16:9`
- Outer margin: `18px`
- Visual spacing: `12px`
- Use a top title bar for each page

## Page 1: Executive Control Tower

Purpose: immediate business state in under 10 seconds.

Visuals:
- 6 KPI cards
  - Total Sales Dollars
  - Total Purchase Dollars
  - Gross Profit
  - Gross Profit After Freight
  - Net Profit Margin
  - Unsold Inventory Value
- Horizontal bar chart: Top 10 Vendors by Sales
- Horizontal bar chart: Top 10 Brands by Sales
- Line + column combo: Purchase Contribution % and cumulative contribution
- Donut: Top 10 Vendors vs All Others

Slicers:
- Vendor Name
- Description
- Performance Flag
- Size

## Page 2: Vendor Performance Matrix

Purpose: compare vendor scale, profitability, and dependency.

Visuals:
- Scatter plot
  - X: Total Purchase Dollars
  - Y: Gross Profit After Freight
  - Size: Total Sales Dollars
  - Legend: Performance Flag
  - Details: Vendor Name
- Ranked table
  - Vendor Name
  - Total Sales Dollars
  - Gross Profit After Freight
  - Net Profit Margin
  - Stock Turnover
  - Purchase Contribution %
- Bar chart: Lowest Inventory Turnover Vendors
- Bar chart: Unsold Inventory Exposure by Vendor

## Page 3: Pricing and Promotion Lab

Purpose: surface brand-level opportunities.

Visuals:
- Scatter plot: Low-Sales / High-Margin brands
  - X: Total Sales Dollars
  - Y: Profit Margin
  - Details: Description
  - Tooltips: Vendor Name, Gross Profit, Stock Turnover
- Clustered bar chart: Top Brands by Sales
- Box plot or custom visual: Unit Purchase Cost by Order Size Bucket
- Table: Target Brands for Promotion/Pricing

## Page 4: Inventory and Risk Monitor

Purpose: show operational drag and concentration risk.

Visuals:
- Donut: Vendor Concentration
- Waterfall: Gross Profit to Gross Profit After Freight
- Bar chart: Unsold Inventory Exposure
- Card strip:
  - Vendor HHI
  - Top 10 Purchase Contribution %
  - Low Sales / High Margin Brand Count
  - Distinct Vendors
  - Distinct Brands

## Page 5: Vendor Drillthrough

Purpose: give recruiters and interviewers one page that feels analytical and interactive.

Visuals:
- Large vendor KPI strip
- Brand-level table for selected vendor
- Scatter: Brand Sales vs Margin for selected vendor
- Inventory exposure by brand
- Slicer synced to vendor

## Tooltip Strategy

Create one report-page tooltip for:
- vendor summary
- brand summary

Tooltip fields:
- Vendor Name
- Description
- Total Sales Dollars
- Gross Profit After Freight
- Net Profit Margin
- Stock Turnover
- Unsold Inventory Value

## What Makes This Recruiter-Friendly

- multiple pages with a clear executive narrative
- KPI cards plus decision visuals
- drillthrough page
- tooltip design
- concentration/risk lens, not just descriptive charts
- margin after freight, not just raw profit
