"""Nmap wrapper — Network port scanner and service detector."""

from .base import SecurityTool, ToolResult


class NmapTool(SecurityTool):
    name = "nmap"
    description = "Network port scanner and service detector"
    docker_image = "hexstrike/nmap:latest"

    async def execute(
        self,
        target: str,
        scan_type: str = "default",
        ports: str | None = None,
        scripts: list[str] | None = None,
    ) -> ToolResult:
        """Run Nmap scan against target."""
        cmd = self._build_command(target, scan_type=scan_type, ports=ports, scripts=scripts)
        result = await self.sandbox.run_tool(self.docker_image, cmd)
        return ToolResult(
            tool_name=self.name,
            exit_code=result["exit_code"],
            raw_output=result["output"],
            parsed_data=self._parse_xml(result["output"]),
        )

    def _build_command(self, target: str, **kwargs) -> str:
        flags = ["-oX", "-"]
        scan_type = kwargs.get("scan_type", "default")
        if scan_type == "quick":
            flags.extend(["-T4", "-F"])
        elif scan_type == "intensive":
            flags.extend(["-T4", "-A", "-v"])
        else:
            flags.extend(["-sV", "-sC"])
        if kwargs.get("ports"):
            flags.extend(["-p", kwargs["ports"]])
        if kwargs.get("scripts"):
            flags.extend(["--script", ",".join(kwargs["scripts"])])
        return f"nmap {' '.join(flags)} {target}"

    def _parse_xml(self, xml_output: str) -> dict:
        """Parse Nmap XML output into structured data."""
        # TODO: Implement XML parsing
        return {"raw": xml_output}
