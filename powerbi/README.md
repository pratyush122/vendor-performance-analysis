# Power BI Dashboard

This folder is the GitHub-facing home for the final Power BI dashboard deliverables.

## Recommended Structure

```text
powerbi/
  pbix/
    vendor_performance_dashboard.pbix
  screenshots/
    page-1-executive-control-tower.png
    page-2-vendor-performance-matrix.png
    page-3-pricing-and-promotion-lab.png
    page-4-inventory-and-risk-monitor.png
    page-5-vendor-drillthrough.png
  README.md
```

## What To Upload Here

1. Your final `.pbix` file in `powerbi/pbix/`
2. One exported screenshot per page in `powerbi/screenshots/`
3. Optional:
   - Power BI Service public/share link
   - a short demo GIF or screen recording

## Suggested README Section For Screenshots

### Dashboard Pages

#### Executive Control Tower

![Executive Control Tower](./screenshots/page-1-executive-control-tower.png)

#### Vendor Performance Matrix

![Vendor Performance Matrix](./screenshots/page-2-vendor-performance-matrix.png)

#### Pricing and Promotion Lab

![Pricing and Promotion Lab](./screenshots/page-3-pricing-and-promotion-lab.png)

#### Inventory and Risk Monitor

![Inventory and Risk Monitor](./screenshots/page-4-inventory-and-risk-monitor.png)

#### Vendor Drillthrough

![Vendor Drillthrough](./screenshots/page-5-vendor-drillthrough.png)

## Suggested Power BI Link Section

If you publish the dashboard to Power BI Service, add this near the top:

`Live Dashboard: [View on Power BI](PASTE_YOUR_LINK_HERE)`

## Notes

- The build inputs for this dashboard live in [`../vendor_powerbi`](../vendor_powerbi).
- The dashboard-ready dataset is [`../outputs/powerbi/vendor_performance_dashboard_ready.csv`](../outputs/powerbi/vendor_performance_dashboard_ready.csv).
