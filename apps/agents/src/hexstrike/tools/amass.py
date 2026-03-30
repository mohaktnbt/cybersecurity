"""Amass wrapper — Subdomain enumeration."""

from .base import SecurityTool, ToolResult


class AmassTool(SecurityTool):
    name = "amass"
    description = "In-depth subdomain enumeration"
    docker_image = "hexstrike/amass:latest"

    async def execute(self, target: str, passive: bool = True) -> ToolResult:
        """Run Amass subdomain enumeration."""
        mode = "enum -passive" if passive else "enum -active"
        cmd = f"amass {mode} -d {target} -json /tmp/amass.json"
        result = await self.sandbox.run_tool(self.docker_image, cmd, timeout=600)
        return ToolResult(
            tool_name=self.name,
            exit_code=result["exit_code"],
            raw_output=result["output"],
        )
