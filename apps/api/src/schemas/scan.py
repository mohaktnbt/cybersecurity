"""Pydantic schemas for scans."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class ScanCreate(BaseModel):
    target_id: uuid.UUID
    scan_type: str = "full"  # full, quick, recon_only, custom
    config: dict = {}


class ScanResponse(BaseModel):
    id: uuid.UUID
    target_id: uuid.UUID
    org_id: uuid.UUID
    status: str
    scan_type: str
    config: dict
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
