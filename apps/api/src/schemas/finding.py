"""Pydantic schemas for findings."""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class FindingResponse(BaseModel):
    id: uuid.UUID
    scan_id: uuid.UUID
    title: str
    description: str
    severity: str
    cvss_score: Decimal | None
    cwe_id: str | None
    owasp_category: str | None
    mitre_technique: str | None
    affected_asset: str
    evidence: dict
    remediation: dict | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class FindingStatusUpdate(BaseModel):
    status: str  # open, confirmed, fixed, accepted, false_positive
