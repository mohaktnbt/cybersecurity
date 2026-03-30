"""Target management endpoints."""

from fastapi import APIRouter, Depends

from ..auth.jwt import get_current_user
from ..schemas.target import TargetCreate, TargetResponse, TargetUpdate

router = APIRouter()


@router.get("/", response_model=list[TargetResponse])
async def list_targets(user: dict = Depends(get_current_user)):
    """List all targets for the current user's organization."""
    # TODO: Implement with DB query
    return []


@router.post("/", response_model=TargetResponse, status_code=201)
async def create_target(target: TargetCreate, user: dict = Depends(get_current_user)):
    """Create a new scan target."""
    # TODO: Implement with DB insert
    raise NotImplementedError


@router.get("/{target_id}", response_model=TargetResponse)
async def get_target(target_id: str, user: dict = Depends(get_current_user)):
    """Get a specific target by ID."""
    # TODO: Implement with DB query
    raise NotImplementedError


@router.patch("/{target_id}", response_model=TargetResponse)
async def update_target(target_id: str, update: TargetUpdate, user: dict = Depends(get_current_user)):
    """Update an existing target."""
    # TODO: Implement with DB update
    raise NotImplementedError


@router.delete("/{target_id}", status_code=204)
async def delete_target(target_id: str, user: dict = Depends(get_current_user)):
    """Delete a target."""
    # TODO: Implement with DB delete
    raise NotImplementedError
