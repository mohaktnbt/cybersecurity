"""Shodan API client — OSINT via Shodan search engine."""

import httpx

from .base import ToolResult


class ShodanClient:
    """Query Shodan API for host intelligence."""

    BASE_URL = "https://api.shodan.io"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30)

    async def host_lookup(self, ip: str) -> ToolResult:
        """Look up host information by IP."""
        url = f"{self.BASE_URL}/shodan/host/{ip}"
        response = await self.client.get(url, params={"key": self.api_key})
        return ToolResult(
            tool_name="shodan",
            exit_code=0 if response.status_code == 200 else 1,
            raw_output=response.text,
            parsed_data=response.json() if response.status_code == 200 else None,
        )

    async def search(self, query: str) -> ToolResult:
        """Search Shodan for matching hosts."""
        url = f"{self.BASE_URL}/shodan/host/search"
        response = await self.client.get(
            url, params={"key": self.api_key, "query": query}
        )
        return ToolResult(
            tool_name="shodan",
            exit_code=0 if response.status_code == 200 else 1,
            raw_output=response.text,
            parsed_data=response.json() if response.status_code == 200 else None,
        )

    async def close(self):
        await self.client.aclose()
