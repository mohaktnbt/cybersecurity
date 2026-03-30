"""Shared Pydantic schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class UUIDMixin(BaseModel):
    id: uuid.UUID


class TimestampMixin(BaseModel):
    created_at: datetime
