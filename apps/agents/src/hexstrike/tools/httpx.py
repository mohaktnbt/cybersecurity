"""httpx wrapper — HTTP probe and technology detection."""

from .base import SecurityTool, ToolResult


class HttpxTool(SecurityTool):
    name = "httpx"
    description = "HTTP probe for live host detection and tech fingerprinting"
    docker_image = "hexstrike/httpx:latest"

    async def execute(self, target: str, probe_options: list[str] | None = None) -> ToolResult:
        """Probe target for HTTP services."""
        cmd = self._build_command(target, probe_options=probe_options)
        result = await self.sandbox.run_tool(self.docker_image, cmd)
        return ToolResult(
            tool_name=self.name,
            exit_code=result["exit_code"],
            raw_output=result["output"],
        )

    def _build_command(self, target: str, **kwargs) -> str:
        flags = ["-u", target, "-json", "-status-code", "-title", "-tech-detect"]
        return f"httpx {' '.join(flags)}"
