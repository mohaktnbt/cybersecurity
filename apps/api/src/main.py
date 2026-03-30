"""HexStrike API — Main application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import findings, reports, scans, targets


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # TODO: Initialize DB connection pool, Redis, S3 client
    yield
    # TODO: Close connections


app = FastAPI(
    title="HexStrike API",
    description="AI-Powered Autonomous Penetration Testing Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(targets.router, prefix="/api/v1/targets", tags=["targets"])
app.include_router(scans.router, prefix="/api/v1/scans", tags=["scans"])
app.include_router(findings.router, prefix="/api/v1/findings", tags=["findings"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "hexstrike-api", "version": "0.1.0"}
