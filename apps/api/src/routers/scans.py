"""Scan management endpoints."""

from fastapi import APIRouter, Depends

from ..auth.jwt import get_current_user
from ..schemas.scan import ScanCreate, ScanResponse

router = APIRouter()


@router.get("/", response_model=list[ScanResponse])
async def list_scans(user: dict = Depends(get_current_user)):
    """List all scans for the current user's organization."""
    # TODO: Implement with DB query
    return []


@router.post("/", response_model=ScanResponse, status_code=201)
async def create_scan(scan: ScanCreate, user: dict = Depends(get_current_user)):
    """Start a new penetration test scan."""
    # TODO: Create scan record, enqueue job to Redis
    raise NotImplementedError


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(scan_id: str, user: dict = Depends(get_current_user)):
    """Get scan details and status."""
    # TODO: Implement with DB query
    raise NotImplementedError


@router.post("/{scan_id}/cancel", status_code=200)
async def cancel_scan(scan_id: str, user: dict = Depends(get_current_user)):
    """Cancel a running scan."""
    # TODO: Update status, signal agent to stop
    raise NotImplementedError


@router.get("/{scan_id}/events")
async def stream_scan_events(scan_id: str, user: dict = Depends(get_current_user)):
    """Stream scan events via Server-Sent Events."""
    # TODO: Implement SSE from scan_events table
    raise NotImplementedError
