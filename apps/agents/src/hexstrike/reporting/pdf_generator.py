"""PDF Report Generator — Executive and technical reports."""

from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent / "templates"


class PDFReportGenerator:
    """Generate PDF pentest reports from scan results."""

    async def generate(
        self,
        findings: list[dict],
        chains: list[dict],
        scan_metadata: dict,
        report_type: str = "technical",
    ) -> str:
        """Generate a PDF report and return the file path."""
        # TODO: Phase 3 — implement with WeasyPrint + Jinja2
        # 1. Load appropriate template
        # 2. Render findings, chains, OWASP/MITRE mappings
        # 3. Generate PDF
        # 4. Upload to S3
        raise NotImplementedError("PDF generation coming in Phase 3")
