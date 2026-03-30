"""ffuf wrapper — Web fuzzer for directory/file discovery."""

from .base import SecurityTool, ToolResult


class FfufTool(SecurityTool):
    name = "ffuf"
    description = "Fast web fuzzer for directory and file brute-forcing"
    docker_image = "hexstrike/ffuf:latest"

    async def execute(
        self, target: str, wordlist: str = "/usr/share/wordlists/common.txt"
    ) -> ToolResult:
        """Run ffuf directory brute-force."""
        cmd = f"ffuf -u {target}/FUZZ -w {wordlist} -o /tmp/ffuf.json -of json -mc 200,301,302,403"
        result = await self.sandbox.run_tool(self.docker_image, cmd, timeout=300)
        return ToolResult(
            tool_name=self.name,
            exit_code=result["exit_code"],
            raw_output=result["output"],
        )
