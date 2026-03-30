"""Application configuration via environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """HexStrike API settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql+asyncpg://dev:dev@localhost:5432/hexstrike_dev"

    # Redis
    redis_url: str = "redis://localhost:6379"

    # Auth
    jwt_secret_key: str = "CHANGE-ME-IN-PRODUCTION"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # S3 / MinIO
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "hexstrike"

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "devpassword"

    # AI
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
