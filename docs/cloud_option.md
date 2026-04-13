# Cloud Upgrade Path

If the local machine still feels constrained, keep the same business logic and move only the compute layer:

1. Load the CSV files into BigQuery or Cloud SQL for PostgreSQL.
2. Reuse the SQL transformations from `sql/` with only minor syntax adjustments.
3. Run the Python analysis step in Google Colab against the exported mart or against the cloud database.
4. Keep Power BI connected only to the final mart, not to raw tables.

The project structure in this folder is already split cleanly enough to support that migration.
