from __future__ import annotations

from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from .config import ProjectConfig


def render_report(config: ProjectConfig, report_payload: dict, logger) -> None:
    environment = Environment(loader=FileSystemLoader(str(config.template_dir)))
    template = environment.get_template("executive_report.md.j2")
    rendered = template.render(
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        payload=report_payload,
    )
    output_path = config.report_dir / "executive_summary.md"
    output_path.write_text(rendered, encoding="utf-8")
    logger.info("Executive summary written to %s", output_path)
