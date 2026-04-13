from __future__ import annotations

import argparse
import sys

from src.vendor_performance.analysis import run_analysis
from src.vendor_performance.config import load_config
from src.vendor_performance.etl import build_analytics_mart, export_powerbi_dataset
from src.vendor_performance.logging_utils import setup_logging
from src.vendor_performance.reporting import render_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Vendor performance analytics pipeline")
    parser.add_argument(
        "command",
        choices=["etl", "analyze", "all"],
        nargs="?",
        default="all",
        help="Pipeline stage to execute.",
    )
    parser.add_argument(
        "--config",
        default="config/project.yaml",
        help="Path to the YAML project configuration.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    logger = setup_logging(config.log_dir)

    try:
        if args.command in {"etl", "all"}:
            build_analytics_mart(config, logger)
            export_powerbi_dataset(config, logger)

        if args.command in {"analyze", "all"}:
            report_payload = run_analysis(config, logger)
            render_report(config, report_payload, logger)

        logger.info("Pipeline command `%s` finished successfully.", args.command)
        return 0
    except Exception as exc:  # pragma: no cover
        logger.exception("Pipeline failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
