"""Attack Graph Builder — Neo4j graph for vulnerability relationships."""

from neo4j import AsyncGraphDatabase


class AttackGraphBuilder:
    """Build and query attack graphs in Neo4j."""

    def __init__(self, uri: str, user: str, password: str):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

    async def add_asset(self, asset: dict) -> None:
        """Add an asset node to the attack graph."""
        async with self.driver.session() as session:
            await session.run(
                "MERGE (a:Asset {url: $url}) SET a += $props",
                url=asset["url"],
                props=asset,
            )

    async def add_vulnerability(self, vuln: dict, asset_url: str) -> None:
        """Add a vulnerability and link it to an asset."""
        async with self.driver.session() as session:
            await session.run(
                """
                MATCH (a:Asset {url: $asset_url})
                MERGE (v:Vulnerability {id: $vuln_id})
                SET v += $props
                MERGE (a)-[:HAS_VULN]->(v)
                """,
                asset_url=asset_url,
                vuln_id=vuln["id"],
                props=vuln,
            )

    async def add_chain_link(self, from_vuln_id: str, to_vuln_id: str, description: str) -> None:
        """Link two vulnerabilities in an attack chain."""
        async with self.driver.session() as session:
            await session.run(
                """
                MATCH (v1:Vulnerability {id: $from_id})
                MATCH (v2:Vulnerability {id: $to_id})
                MERGE (v1)-[:ENABLES {description: $desc}]->(v2)
                """,
                from_id=from_vuln_id,
                to_id=to_vuln_id,
                desc=description,
            )

    async def close(self):
        await self.driver.close()
