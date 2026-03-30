"""OWASP ZAP wrapper — Web application security scanner."""

from .base import SecurityTool, ToolResult


class ZapTool(SecurityTool):
    name = "zap"
    description = "OWASP ZAP web application security scanner"
    docker_image = "hexstrike/zap:latest"

    async def execute(self, target: str, scan_type: str = "baseline") -> ToolResult:
        """Run ZAP scan against target."""
        cmd = self._build_command(target, scan_type=scan_type)
        result = await self.sandbox.run_tool(self.docker_image, cmd, timeout=600)
        return ToolResult(
            tool_name=self.name,
            exit_code=result["exit_code"],
            raw_output=result["output"],
        )

    def _build_command(self, target: str, **kwargs) -> str:
        scan_type = kwargs.get("scan_type", "baseline")
        if scan_type == "full":
            return f"zap-full-scan.py -t {target} -J report.json"
        return f"zap-baseline.py -t {target} -J report.json"
