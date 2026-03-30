"""Hydra wrapper — Network login brute-forcer."""

from .base import SecurityTool, ToolResult


class HydraTool(SecurityTool):
    name = "hydra"
    description = "Network login brute-force tool"
    docker_image = "hexstrike/hydra:latest"

    async def execute(
        self,
        target: str,
        service: str = "ssh",
        username: str | None = None,
        wordlist: str = "/usr/share/wordlists/rockyou-mini.txt",
    ) -> ToolResult:
        """Run Hydra credential brute-force."""
        user_flag = f"-l {username}" if username else "-L /usr/share/wordlists/users.txt"
        cmd = f"hydra {user_flag} -P {wordlist} {target} {service} -o /tmp/hydra.txt -t 4"
        result = await self.sandbox.run_tool(self.docker_image, cmd, timeout=300)
        return ToolResult(
            tool_name=self.name,
            exit_code=result["exit_code"],
            raw_output=result["output"],
        )
