"""sqlmap wrapper — SQL injection detection and exploitation."""

from .base import SecurityTool, ToolResult


class SqlmapTool(SecurityTool):
    name = "sqlmap"
    description = "SQL injection detection and exploitation tool"
    docker_image = "hexstrike/sqlmap:latest"

    async def execute(
        self,
        target: str,
        method: str = "GET",
        data: str | None = None,
        level: int = 1,
        risk: int = 1,
    ) -> ToolResult:
        """Run sqlmap against a target URL."""
        cmd = self._build_command(
            target, method=method, data=data, level=level, risk=risk
        )
        result = await self.sandbox.run_tool(self.docker_image, cmd, timeout=300)
        return ToolResult(
            tool_name=self.name,
            exit_code=result["exit_code"],
            raw_output=result["output"],
        )

    def _build_command(self, target: str, **kwargs) -> str:
        flags = ["-u", f'"{target}"', "--batch", "--output-dir=/tmp/sqlmap"]
        if kwargs.get("data"):
            flags.extend(["--data", f'"{kwargs["data"]}"'])
        flags.extend(["--level", str(kwargs.get("level", 1))])
        flags.extend(["--risk", str(kwargs.get("risk", 1))])
        return f"sqlmap {' '.join(flags)}"
