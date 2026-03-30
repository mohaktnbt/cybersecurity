"""Scan and ScanEvent models."""

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Scan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "scans"

    target_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("targets.id", ondelete="CASCADE")
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE")
    )
    status: Mapped[str] = mapped_column(String, server_default="pending")
    scan_type: Mapped[str] = mapped_column(String, server_default="full")
    config: Mapped[dict] = mapped_column(JSONB, server_default="'{}'")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    target = relationship("Target", back_populates="scans")
    organization = relationship("Organization", back_populates="scans")
    findings = relationship("Finding", back_populates="scan")
    events = relationship("ScanEvent", back_populates="scan")


class ScanEvent(Base):
    __tablename__ = "scan_events"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scans.id", ondelete="CASCADE")
    )
    agent: Mapped[str] = mapped_column(String, nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )

    scan = relationship("Scan", back_populates="events")
