from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

from .config import ProjectConfig
from .db import connect
from .metrics import confidence_interval, format_currency, herfindahl_hirschman_index


plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("Blues_r")


def _save_dataframe(data_frame: pd.DataFrame, path: Path) -> None:
    data_frame.to_csv(path, index=False)


def _save_json(payload: dict, path: Path) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _get_filtered_analysis_frame(data_frame: pd.DataFrame) -> pd.DataFrame:
    filtered = data_frame[
        (data_frame["gross_profit"] > 0)
        & (data_frame["profit_margin"] > 0)
        & (data_frame["total_sales_quantity"] > 0)
    ].copy()
    filtered["volume_ml"] = pd.to_numeric(filtered["volume_ml"], errors="coerce")
    return filtered


def _build_data_quality_summary(data_frame: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    for column_name in data_frame.columns:
        series = data_frame[column_name]
        summary_rows.append(
            {
                "column_name": column_name,
                "dtype": str(series.dtype),
                "null_count": int(series.isna().sum()),
                "null_pct": round(float(series.isna().mean() * 100), 2),
                "distinct_count": int(series.nunique(dropna=True)),
            }
        )
    return pd.DataFrame(summary_rows).sort_values(["null_count", "column_name"], ascending=[False, True])


def _summary_statistics(data_frame: pd.DataFrame) -> pd.DataFrame:
    numeric_summary = data_frame.select_dtypes(include=["number"]).describe().T.reset_index()
    return numeric_summary.rename(columns={"index": "metric"})


def _plot_top_vendors(top_vendors: pd.DataFrame, chart_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_vendors, x="total_sales_dollars", y="vendor_name", ax=axis)
    axis.set_title("Top Vendors by Sales")
    axis.set_xlabel("Total Sales Dollars")
    axis.set_ylabel("Vendor")
    for patch, value in zip(axis.patches, top_vendors["total_sales_dollars"]):
        axis.text(patch.get_width(), patch.get_y() + patch.get_height() / 2, f" {format_currency(value)}", va="center")
    figure.tight_layout()
    figure.savefig(chart_path, dpi=200)
    plt.close(figure)


def _plot_top_brands(top_brands: pd.DataFrame, chart_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_brands, x="total_sales_dollars", y="description", ax=axis)
    axis.set_title("Top Brands by Sales")
    axis.set_xlabel("Total Sales Dollars")
    axis.set_ylabel("Brand")
    for patch, value in zip(axis.patches, top_brands["total_sales_dollars"]):
        axis.text(patch.get_width(), patch.get_y() + patch.get_height() / 2, f" {format_currency(value)}", va="center")
    figure.tight_layout()
    figure.savefig(chart_path, dpi=200)
    plt.close(figure)


def _plot_target_brands(brand_performance: pd.DataFrame, target_brands: pd.DataFrame, chart_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(11, 7))
    subset = brand_performance[brand_performance["total_sales_dollars"] <= 10_000].copy()
    sns.scatterplot(
        data=subset,
        x="total_sales_dollars",
        y="profit_margin",
        alpha=0.25,
        s=40,
        ax=axis,
        label="All brands",
    )
    target_subset = target_brands[target_brands["total_sales_dollars"] <= 10_000].copy()
    if not target_subset.empty:
        sns.scatterplot(
            data=target_subset,
            x="total_sales_dollars",
            y="profit_margin",
            color="#d62728",
            s=55,
            ax=axis,
            label="Target brands",
        )
    axis.set_title("Low-Sales / High-Margin Brands")
    axis.set_xlabel("Total Sales Dollars")
    axis.set_ylabel("Average Profit Margin (%)")
    figure.tight_layout()
    figure.savefig(chart_path, dpi=200)
    plt.close(figure)


def _plot_vendor_purchase_concentration(top_vendor_contribution: pd.DataFrame, chart_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(12, 6))
    cumulative_axis = axis.twinx()
    sns.barplot(data=top_vendor_contribution, x="vendor_name", y="purchase_contribution_pct", ax=axis)
    cumulative_axis.plot(
        range(len(top_vendor_contribution)),
        top_vendor_contribution["cumulative_contribution_pct"],
        color="#d62728",
        marker="o",
        linewidth=2,
    )
    axis.set_title("Top Vendor Purchase Contribution")
    axis.set_xlabel("Vendor")
    axis.set_ylabel("Purchase Contribution (%)")
    cumulative_axis.set_ylabel("Cumulative Contribution (%)")
    axis.tick_params(axis="x", rotation=45)
    figure.tight_layout()
    figure.savefig(chart_path, dpi=200)
    plt.close(figure)


def _plot_bulk_pricing(order_size_frame: pd.DataFrame, chart_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=order_size_frame, x="order_size", y="unit_purchase_cost", order=["Small", "Medium", "Large"], ax=axis)
    axis.set_title("Bulk Purchasing vs Unit Cost")
    axis.set_xlabel("Order Size Bucket")
    axis.set_ylabel("Unit Purchase Cost")
    figure.tight_layout()
    figure.savefig(chart_path, dpi=200)
    plt.close(figure)


def _plot_low_turnover(low_turnover: pd.DataFrame, chart_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(12, 6))
    sns.barplot(data=low_turnover, x="stock_turnover", y="vendor_name", ax=axis)
    axis.set_title("Lowest Inventory Turnover Vendors")
    axis.set_xlabel("Average Stock Turnover")
    axis.set_ylabel("Vendor")
    figure.tight_layout()
    figure.savefig(chart_path, dpi=200)
    plt.close(figure)


def _plot_profit_margin_distribution(top_profit_margins: pd.Series, low_profit_margins: pd.Series, chart_path: Path) -> None:
    figure, axis = plt.subplots(figsize=(10, 6))
    sns.kdeplot(top_profit_margins, fill=True, alpha=0.35, linewidth=2, label="Top performers", ax=axis)
    sns.kdeplot(low_profit_margins, fill=True, alpha=0.35, linewidth=2, label="Low performers", ax=axis)
    axis.set_title("Profit Margin Distribution by Vendor Tier")
    axis.set_xlabel("Profit Margin (%)")
    axis.set_ylabel("Density")
    axis.legend()
    figure.tight_layout()
    figure.savefig(chart_path, dpi=200)
    plt.close(figure)


def run_analysis(config: ProjectConfig, logger) -> dict:
    connection = connect(config)
    try:
        mart_frame = connection.execute("SELECT * FROM mart_vendor_performance").df()
    finally:
        connection.close()

    logger.info("Loaded mart_vendor_performance with %s rows.", len(mart_frame))
    analysis_frame = _get_filtered_analysis_frame(mart_frame)
    logger.info("Filtered analysis dataset down to %s commercially valid rows.", len(analysis_frame))

    data_quality_summary = _build_data_quality_summary(mart_frame)
    summary_statistics = _summary_statistics(mart_frame)

    top_n = config.analysis.chart_top_n
    brand_performance = (
        analysis_frame.groupby("description", as_index=False)
        .agg(
            total_sales_dollars=("total_sales_dollars", "sum"),
            profit_margin=("profit_margin", "mean"),
            gross_profit=("gross_profit", "sum"),
        )
    )
    low_sales_threshold = brand_performance["total_sales_dollars"].quantile(config.analysis.target_brand_sales_quantile)
    high_margin_threshold = brand_performance["profit_margin"].quantile(config.analysis.target_brand_margin_quantile)
    target_brands = brand_performance[
        (brand_performance["total_sales_dollars"] <= low_sales_threshold)
        & (brand_performance["profit_margin"] >= high_margin_threshold)
    ].sort_values(["profit_margin", "total_sales_dollars"], ascending=[False, True])

    top_vendors = (
        analysis_frame.groupby("vendor_name", as_index=False)["total_sales_dollars"]
        .sum()
        .sort_values("total_sales_dollars", ascending=False)
        .head(top_n)
    )
    top_brands = (
        analysis_frame.groupby("description", as_index=False)["total_sales_dollars"]
        .sum()
        .sort_values("total_sales_dollars", ascending=False)
        .head(top_n)
    )

    vendor_purchase_contribution = (
        analysis_frame.groupby("vendor_name", as_index=False)["total_purchase_dollars"]
        .sum()
        .sort_values("total_purchase_dollars", ascending=False)
    )
    vendor_purchase_contribution["purchase_contribution_pct"] = (
        vendor_purchase_contribution["total_purchase_dollars"]
        / vendor_purchase_contribution["total_purchase_dollars"].sum()
        * 100
    )
    vendor_purchase_contribution["cumulative_contribution_pct"] = vendor_purchase_contribution["purchase_contribution_pct"].cumsum()
    top_vendor_contribution = vendor_purchase_contribution.head(top_n).copy()

    order_size_frame = analysis_frame.copy()
    order_size_frame["order_size"] = pd.qcut(
        order_size_frame["total_purchase_quantity"],
        q=3,
        labels=["Small", "Medium", "Large"],
        duplicates="drop",
    )
    bulk_pricing_summary = (
        order_size_frame.groupby("order_size", observed=False)["unit_purchase_cost"]
        .agg(["mean", "median", "min", "max"])
        .reset_index()
    )

    low_turnover = (
        analysis_frame[analysis_frame["stock_turnover"] < 1]
        .groupby("vendor_name", as_index=False)["stock_turnover"]
        .mean()
        .sort_values("stock_turnover", ascending=True)
        .head(top_n)
    )

    unsold_inventory = (
        analysis_frame.groupby("vendor_name", as_index=False)["unsold_inventory_value"]
        .sum()
        .sort_values("unsold_inventory_value", ascending=False)
        .head(top_n)
    )

    vendor_tiers = analysis_frame.groupby("vendor_name", as_index=False)["total_sales_dollars"].sum()
    top_threshold = vendor_tiers["total_sales_dollars"].quantile(config.analysis.top_performer_sales_quantile)
    low_threshold = vendor_tiers["total_sales_dollars"].quantile(config.analysis.low_performer_sales_quantile)
    top_vendor_names = vendor_tiers[vendor_tiers["total_sales_dollars"] >= top_threshold]["vendor_name"]
    low_vendor_names = vendor_tiers[vendor_tiers["total_sales_dollars"] <= low_threshold]["vendor_name"]
    top_profit_margins = analysis_frame[analysis_frame["vendor_name"].isin(top_vendor_names)]["profit_margin"].dropna()
    low_profit_margins = analysis_frame[analysis_frame["vendor_name"].isin(low_vendor_names)]["profit_margin"].dropna()

    top_margin_mean, top_margin_lower, top_margin_upper = confidence_interval(top_profit_margins)
    low_margin_mean, low_margin_lower, low_margin_upper = confidence_interval(low_profit_margins)
    ttest_statistic, ttest_p_value = stats.ttest_ind(
        top_profit_margins,
        low_profit_margins,
        equal_var=False,
        nan_policy="omit",
    )

    spearman_corr, spearman_p_value = stats.spearmanr(
        analysis_frame["total_purchase_quantity"],
        analysis_frame["unit_purchase_cost"],
        nan_policy="omit",
    )

    kpi_snapshot = {
        "mart_rows": int(len(mart_frame)),
        "analysis_rows": int(len(analysis_frame)),
        "distinct_vendors": int(analysis_frame["vendor_number"].nunique()),
        "distinct_brands": int(analysis_frame["brand_id"].nunique()),
        "total_sales_dollars": float(analysis_frame["total_sales_dollars"].sum()),
        "total_purchase_dollars": float(analysis_frame["total_purchase_dollars"].sum()),
        "gross_profit": float(analysis_frame["gross_profit"].sum()),
        "avg_profit_margin": float(analysis_frame["profit_margin"].mean()),
        "unsold_inventory_value": float(analysis_frame["unsold_inventory_value"].sum()),
        "top_10_purchase_contribution_pct": float(top_vendor_contribution["purchase_contribution_pct"].sum()),
        "vendor_hhi": float(herfindahl_hirschman_index(vendor_purchase_contribution["total_purchase_dollars"])),
        "bulk_purchase_spearman_corr": float(spearman_corr),
        "bulk_purchase_spearman_p_value": float(spearman_p_value),
        "profit_margin_ttest_p_value": float(ttest_p_value),
    }

    hypothesis_results = pd.DataFrame(
        [
            {
                "comparison": "top_vs_low_vendor_profit_margin",
                "top_mean": top_margin_mean,
                "top_ci_lower": top_margin_lower,
                "top_ci_upper": top_margin_upper,
                "low_mean": low_margin_mean,
                "low_ci_lower": low_margin_lower,
                "low_ci_upper": low_margin_upper,
                "ttest_statistic": ttest_statistic,
                "ttest_p_value": ttest_p_value,
            }
        ]
    )

    _save_dataframe(data_quality_summary, config.table_dir / "data_quality_summary.csv")
    _save_dataframe(summary_statistics, config.table_dir / "summary_statistics.csv")
    _save_dataframe(target_brands, config.table_dir / "target_brands.csv")
    _save_dataframe(top_vendors, config.table_dir / "top_vendors_by_sales.csv")
    _save_dataframe(top_brands, config.table_dir / "top_brands_by_sales.csv")
    _save_dataframe(top_vendor_contribution, config.table_dir / "top_vendor_purchase_contribution.csv")
    _save_dataframe(bulk_pricing_summary, config.table_dir / "bulk_pricing_summary.csv")
    _save_dataframe(low_turnover, config.table_dir / "low_inventory_turnover_vendors.csv")
    _save_dataframe(unsold_inventory, config.table_dir / "unsold_inventory_exposure.csv")
    _save_dataframe(hypothesis_results, config.table_dir / "hypothesis_results.csv")
    _save_json(kpi_snapshot, config.table_dir / "kpi_snapshot.json")

    _plot_top_vendors(top_vendors, config.chart_dir / "top_vendors_by_sales.png")
    _plot_top_brands(top_brands, config.chart_dir / "top_brands_by_sales.png")
    _plot_target_brands(brand_performance, target_brands, config.chart_dir / "target_brands_scatter.png")
    _plot_vendor_purchase_concentration(top_vendor_contribution, config.chart_dir / "vendor_purchase_contribution.png")
    _plot_bulk_pricing(order_size_frame, config.chart_dir / "bulk_pricing_boxplot.png")
    _plot_low_turnover(low_turnover, config.chart_dir / "low_inventory_turnover.png")
    _plot_profit_margin_distribution(top_profit_margins, low_profit_margins, config.chart_dir / "profit_margin_distribution.png")

    report_payload = {
        "kpis": kpi_snapshot,
        "target_brand_count": int(len(target_brands)),
        "top_vendor": top_vendors.iloc[0]["vendor_name"] if not top_vendors.empty else "N/A",
        "top_vendor_sales": format_currency(float(top_vendors.iloc[0]["total_sales_dollars"])) if not top_vendors.empty else "$0.00",
        "top_brand": top_brands.iloc[0]["description"] if not top_brands.empty else "N/A",
        "top_brand_sales": format_currency(float(top_brands.iloc[0]["total_sales_dollars"])) if not top_brands.empty else "$0.00",
        "top_10_purchase_contribution_pct": round(float(top_vendor_contribution["purchase_contribution_pct"].sum()), 2),
        "lowest_turnover_vendor": low_turnover.iloc[0]["vendor_name"] if not low_turnover.empty else "N/A",
        "lowest_turnover_value": round(float(low_turnover.iloc[0]["stock_turnover"]), 2) if not low_turnover.empty else 0.0,
        "unsold_inventory_total": format_currency(float(analysis_frame["unsold_inventory_value"].sum())),
        "bulk_purchase_corr": round(float(spearman_corr), 3),
        "bulk_purchase_p_value": round(float(spearman_p_value), 6),
        "profit_margin_top_ci": [round(float(top_margin_lower), 2), round(float(top_margin_upper), 2)],
        "profit_margin_low_ci": [round(float(low_margin_lower), 2), round(float(low_margin_upper), 2)],
        "profit_margin_p_value": round(float(ttest_p_value), 8),
    }
    return report_payload
