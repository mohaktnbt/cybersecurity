"""Report generation and retrieval endpoints."""

from fastapi import APIRouter, Depends

from ..auth.jwt import get_current_user

router = APIRouter()


@router.get("/")
async def list_reports(user: dict = Depends(get_current_user)):
    """List generated reports."""
    # TODO: Implement with DB query
    return []


@router.post("/generate", status_code=202)
async def generate_report(
    scan_id: str,
    report_type: str = "technical",
    report_format: str = "pdf",
    user: dict = Depends(get_current_user),
):
    """Queue report generation for a completed scan."""
    # TODO: Validate scan is complete, enqueue report generation job
    raise NotImplementedError


@router.get("/{report_id}/download")
async def download_report(report_id: str, user: dict = Depends(get_current_user)):
    """Download a generated report from S3."""
    # TODO: Get pre-signed S3 URL and redirect
    raise NotImplementedError
