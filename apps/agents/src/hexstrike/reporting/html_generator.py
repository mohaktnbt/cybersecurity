"""HTML Report Generator — Interactive web reports."""

from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "templates"


class HTMLReportGenerator:
    """Generate interactive HTML pentest reports."""

    async def generate(
        self,
        findings: list[dict],
        chains: list[dict],
        scan_metadata: dict,
    ) -> str:
        """Generate an HTML report and return the file path."""
        # TODO: Phase 3 — implement with Jinja2
        raise NotImplementedError("HTML report generation coming in Phase 3")
