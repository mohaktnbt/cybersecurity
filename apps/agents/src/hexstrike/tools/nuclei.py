"""Nuclei wrapper — Template-based vulnerability scanner."""

from .base import SecurityTool, ToolResult


class NucleiTool(SecurityTool):
    name = "nuclei"
    description = "Template-based vulnerability scanner"
    docker_image = "hexstrike/nuclei:latest"

    async def execute(
        self,
        target: str,
        templates: list[str] | None = None,
        severity: str | None = None,
        tags: list[str] | None = None,
    ) -> ToolResult:
        """Run Nuclei scan against target."""
        cmd = self._build_command(
            target, templates=templates, severity=severity, tags=tags
        )
        result = await self.sandbox.run_tool(self.docker_image, cmd)
        return ToolResult(
            tool_name=self.name,
            exit_code=result["exit_code"],
            raw_output=result["output"],
            parsed_data=self._parse_json(result["output"]),
        )

    def _build_command(self, target: str, **kwargs) -> str:
        flags = ["-u", target, "-jsonl"]
        if kwargs.get("severity"):
            flags.extend(["-severity", kwargs["severity"]])
        if kwargs.get("templates"):
            for t in kwargs["templates"]:
                flags.extend(["-t", t])
        if kwargs.get("tags"):
            flags.extend(["-tags", ",".join(kwargs["tags"])])
        return f"nuclei {' '.join(flags)}"

    def _parse_json(self, output: str) -> list[dict]:
        """Parse Nuclei JSONL output."""
        import json
        results = []
        for line in output.strip().split("\n"):
            if line.strip():
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return results
