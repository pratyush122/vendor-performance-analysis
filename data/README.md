# Data Folder

Raw source datasets are intentionally kept out of the GitHub repository because of file-size limits.

The project expects the original CSV files to be present locally in this folder with these names:

- `begin_inventory.csv`
- `end_inventory.csv`
- `purchase_prices.csv`
- `purchases.csv`
- `sales.csv`
- `vendor_invoice.csv`

Once those files are placed here, run:

```powershell
& .\.venv\Scripts\python.exe main.py all
```

This will rebuild the analytics mart, analysis outputs, and Power BI-ready exports locally.
