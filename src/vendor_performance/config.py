from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True)
class AnalysisThresholds:
    target_brand_sales_quantile: float
    target_brand_margin_quantile: float
    top_performer_sales_quantile: float
    low_performer_sales_quantile: float
    chart_top_n: int


@dataclass(slots=True)
class ProjectConfig:
    project_name: str
    base_dir: Path
    database_path: Path
    data_dir: Path
    output_dir: Path
    log_dir: Path
    memory_limit: str
    threads: int
    raw_files: dict[str, Path]
    analysis: AnalysisThresholds

    @property
    def sql_dir(self) -> Path:
        return self.base_dir / "sql"

    @property
    def template_dir(self) -> Path:
        return self.base_dir / "templates"

    @property
    def chart_dir(self) -> Path:
        return self.output_dir / "charts"

    @property
    def table_dir(self) -> Path:
        return self.output_dir / "tables"

    @property
    def report_dir(self) -> Path:
        return self.output_dir / "reports"

    @property
    def powerbi_dir(self) -> Path:
        return self.output_dir / "powerbi"

    @property
    def temp_dir(self) -> Path:
        return self.output_dir / "temp_duckdb"


def load_config(config_path: str | Path = "config/project.yaml") -> ProjectConfig:
    resolved_path = Path(config_path).resolve()
    base_dir = resolved_path.parent.parent
    with resolved_path.open("r", encoding="utf-8") as file_handle:
        raw_config = yaml.safe_load(file_handle)

    data_dir = (base_dir / raw_config["data_dir"]).resolve()
    output_dir = (base_dir / raw_config["output_dir"]).resolve()
    log_dir = (base_dir / raw_config["log_dir"]).resolve()
    database_path = (base_dir / raw_config["database_path"]).resolve()

    analysis = AnalysisThresholds(**raw_config["analysis"])
    raw_files = {
        logical_name: (data_dir / file_name).resolve()
        for logical_name, file_name in raw_config["raw_files"].items()
    }

    config = ProjectConfig(
        project_name=raw_config["project_name"],
        base_dir=base_dir,
        database_path=database_path,
        data_dir=data_dir,
        output_dir=output_dir,
        log_dir=log_dir,
        memory_limit=str(raw_config["memory_limit"]),
        threads=int(raw_config["threads"]),
        raw_files=raw_files,
        analysis=analysis,
    )

    for directory in (
        config.output_dir,
        config.chart_dir,
        config.table_dir,
        config.report_dir,
        config.powerbi_dir,
        config.log_dir,
        config.temp_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    return config
