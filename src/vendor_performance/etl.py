from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

from .config import ProjectConfig
from .db import connect, execute_sql_file


def build_analytics_mart(config: ProjectConfig, logger) -> dict[str, int]:
    start_time = time.time()
    connection = connect(config)
    try:
        context = {
            "begin_inventory_csv": config.raw_files["begin_inventory"].as_posix(),
            "end_inventory_csv": config.raw_files["end_inventory"].as_posix(),
            "purchase_prices_csv": config.raw_files["purchase_prices"].as_posix(),
            "purchases_csv": config.raw_files["purchases"].as_posix(),
            "sales_csv": config.raw_files["sales"].as_posix(),
            "vendor_invoice_csv": config.raw_files["vendor_invoice"].as_posix(),
        }

        logger.info("Creating raw views from CSV files.")
        execute_sql_file(connection, config.sql_dir / "raw_views.sql", context)

        logger.info("Building staged summaries and mart table.")
        execute_sql_file(connection, config.sql_dir / "marts.sql")

        audit_queries = {
            "raw_purchases_rows": "SELECT COUNT(*) FROM raw_purchases",
            "raw_sales_rows": "SELECT COUNT(*) FROM raw_sales",
            "raw_vendor_invoice_rows": "SELECT COUNT(*) FROM raw_vendor_invoice",
            "mart_rows": "SELECT COUNT(*) FROM mart_vendor_performance",
            "distinct_vendors": "SELECT COUNT(DISTINCT vendor_number) FROM mart_vendor_performance",
            "distinct_brands": "SELECT COUNT(DISTINCT brand_id) FROM mart_vendor_performance",
        }
        metrics = {
            metric_name: int(connection.execute(query).fetchone()[0])
            for metric_name, query in audit_queries.items()
        }
        metrics["runtime_seconds"] = round(time.time() - start_time, 2)

        pd.DataFrame([metrics]).to_csv(config.table_dir / "etl_audit.csv", index=False)
        logger.info("ETL completed in %.2f seconds.", metrics["runtime_seconds"])
        return metrics
    finally:
        connection.close()


def export_powerbi_dataset(config: ProjectConfig, logger) -> Path:
    connection = connect(config)
    destination = config.powerbi_dir / "vendor_performance_powerbi.csv"
    dashboard_destination = config.powerbi_dir / "vendor_performance_dashboard_ready.csv"
    try:
        logger.info("Exporting Power BI dataset to %s", destination)
        connection.execute(
            f"""
            COPY (
                SELECT *
                FROM mart_vendor_performance
            ) TO '{destination.as_posix()}' (HEADER, DELIMITER ',');
            """
        )
        logger.info("Exporting dashboard-ready Power BI dataset to %s", dashboard_destination)
        connection.execute(
            f"""
            COPY (
                SELECT *
                FROM mart_vendor_performance
                WHERE gross_profit > 0
                  AND profit_margin > 0
                  AND total_sales_quantity > 0
            ) TO '{dashboard_destination.as_posix()}' (HEADER, DELIMITER ',');
            """
        )
    finally:
        connection.close()
    return dashboard_destination
