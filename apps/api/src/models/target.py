"""Target (asset to test) model."""

import uuid

from sqlalchemy import Boolean, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Target(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "targets"

    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    scope: Mapped[dict] = mapped_column(JSONB, nullable=False)
    config: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'"))
    verified: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    organization = relationship("Organization", back_populates="targets")
    scans = relationship("Scan", back_populates="target")
