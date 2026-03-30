"""Docker Sandbox Executor — Run security tools in isolated containers."""

import asyncio
import logging

import docker

logger = logging.getLogger(__name__)


class SandboxExecutor:
    """Execute security tools inside isolated Docker containers."""

    def __init__(self):
        self.client = docker.from_env()

    async def run_tool(
        self,
        image: str,
        command: str,
        timeout: int = 300,
        network_mode: str = "bridge",
        scope: dict | None = None,
    ) -> dict:
        """Run a security tool in a sandboxed container.

        Args:
            image: Docker image name
            command: Command to execute
            timeout: Max execution time in seconds
            network_mode: Docker network mode
            scope: Target scope for validation

        Returns:
            Dict with exit_code and output
        """
        if scope:
            self._validate_scope(command, scope)

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self._run_container, image, command, timeout, network_mode
        )

    def _run_container(
        self, image: str, command: str, timeout: int, network_mode: str
    ) -> dict:
        """Synchronous container execution."""
        container = self.client.containers.run(
            image=image,
            command=command,
            detach=True,
            network_mode=network_mode,
            mem_limit="512m",
            cpu_period=100000,
            cpu_quota=50000,
            read_only=True,
            security_opt=["no-new-privileges"],
            cap_drop=["ALL"],
        )
        try:
            result = container.wait(timeout=timeout)
            logs = container.logs().decode()
            return {"exit_code": result["StatusCode"], "output": logs}
        except Exception as e:
            logger.error("Container execution failed: %s", e)
            return {"exit_code": -1, "output": str(e)}
        finally:
            container.remove(force=True)

    def _validate_scope(self, command: str, scope: dict) -> None:
        """Validate that command targets are within authorized scope."""
        excluded = scope.get("excluded", [])
        for excluded_target in excluded:
            if excluded_target in command:
                raise ValueError(
                    f"Target {excluded_target} is excluded from scope"
                )
