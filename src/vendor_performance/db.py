from __future__ import annotations

from pathlib import Path

import duckdb
from jinja2 import Template

from .config import ProjectConfig


def connect(config: ProjectConfig) -> duckdb.DuckDBPyConnection:
    connection = duckdb.connect(str(config.database_path))
    connection.execute(f"SET temp_directory = '{config.temp_dir.as_posix()}'")
    connection.execute(f"SET memory_limit = '{config.memory_limit}'")
    connection.execute(f"SET threads = {config.threads}")
    return connection


def render_sql(sql_path: Path, context: dict[str, str]) -> str:
    template = Template(sql_path.read_text(encoding="utf-8"))
    return template.render(**context)


def execute_sql_file(
    connection: duckdb.DuckDBPyConnection,
    sql_path: Path,
    context: dict[str, str] | None = None,
) -> None:
    rendered_sql = render_sql(sql_path, context or {})
    connection.execute(rendered_sql)
