"""Finding query endpoints."""

from fastapi import APIRouter, Depends, Query

from ..auth.jwt import get_current_user
from ..schemas.finding import FindingResponse, FindingStatusUpdate

router = APIRouter()


@router.get("/", response_model=list[FindingResponse])
async def list_findings(
    scan_id: str | None = Query(None),
    severity: str | None = Query(None),
    status: str | None = Query(None),
    user: dict = Depends(get_current_user),
):
    """List findings with optional filters."""
    # TODO: Implement with DB query + filters
    return []


@router.get("/{finding_id}", response_model=FindingResponse)
async def get_finding(finding_id: str, user: dict = Depends(get_current_user)):
    """Get detailed finding with evidence."""
    # TODO: Implement with DB query
    raise NotImplementedError


@router.patch("/{finding_id}/status")
async def update_finding_status(
    finding_id: str, update: FindingStatusUpdate, user: dict = Depends(get_current_user)
):
    """Update finding status (confirm, fix, accept, false positive)."""
    # TODO: Implement with DB update
    raise NotImplementedError
