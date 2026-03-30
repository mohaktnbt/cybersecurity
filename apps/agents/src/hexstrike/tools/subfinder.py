"""Subfinder wrapper — Fast subdomain discovery."""

from .base import SecurityTool, ToolResult


class SubfinderTool(SecurityTool):
    name = "subfinder"
    description = "Fast passive subdomain enumeration"
    docker_image = "hexstrike/subfinder:latest"

    async def execute(self, target: str) -> ToolResult:
        """Run Subfinder against target domain."""
        cmd = f"subfinder -d {target} -json -silent"
        result = await self.sandbox.run_tool(self.docker_image, cmd)
        return ToolResult(
            tool_name=self.name,
            exit_code=result["exit_code"],
            raw_output=result["output"],
        )
