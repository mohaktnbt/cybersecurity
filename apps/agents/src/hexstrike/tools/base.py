"""Base class for all security tool wrappers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResult:
    """Standard result from a security tool execution."""

    tool_name: str
    exit_code: int
    raw_output: str
    parsed_data: Any = None
    errors: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return self.exit_code == 0


class SecurityTool(ABC):
    """Abstract base class for Docker-sandboxed security tools."""

    name: str = ""
    description: str = ""
    docker_image: str = ""

    def __init__(self, sandbox_executor=None):
        self.sandbox = sandbox_executor

    @abstractmethod
    async def execute(self, target: str, **kwargs) -> ToolResult:
        """Execute the tool against a target."""
        ...

    def _build_command(self, target: str, **kwargs) -> str:
        """Build the CLI command string."""
        raise NotImplementedError
