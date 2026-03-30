"""Chain Finder — Discover multi-step attack paths in Neo4j."""

from neo4j import AsyncGraphDatabase


class ChainFinder:
    """Find attack chains through graph traversal."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

    async def find_chains(self, max_depth: int = 5) -> list[dict]:
        """Find all multi-step attack paths up to max_depth."""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH path = (start:Vulnerability)-[:ENABLES*1..%d]->(end:Vulnerability)
                WHERE start <> end
                RETURN path, length(path) as depth
                ORDER BY depth DESC
                LIMIT 50
                """
                % max_depth
            )
            chains = []
            async for record in result:
                chains.append({
                    "path": str(record["path"]),
                    "depth": record["depth"],
                })
            return chains

    async def find_critical_paths(self) -> list[dict]:
        """Find paths that lead to critical impact."""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH path = (start:Vulnerability)-[:ENABLES*]->(end:Vulnerability)
                WHERE end.severity = 'critical'
                RETURN path, length(path) as depth
                ORDER BY depth DESC
                LIMIT 20
                """
            )
            paths = []
            async for record in result:
                paths.append({
                    "path": str(record["path"]),
                    "depth": record["depth"],
                })
            return paths

    async def close(self):
        await self.driver.close()
