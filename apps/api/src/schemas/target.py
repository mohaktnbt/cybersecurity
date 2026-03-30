"""Pydantic schemas for targets."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class TargetScope(BaseModel):
    domains: list[str] = []
    ips: list[str] = []
    cidrs: list[str] = []
    excluded: list[str] = []


class TargetCreate(BaseModel):
    name: str
    type: str  # web_app, api, network, cloud, mobile
    scope: TargetScope
    config: dict = {}


class TargetUpdate(BaseModel):
    name: str | None = None
    scope: TargetScope | None = None
    config: dict | None = None


class TargetResponse(BaseModel):
    id: uuid.UUID
    org_id: uuid.UUID
    name: str
    type: str
    scope: TargetScope
    config: dict
    verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}
