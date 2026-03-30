"""Finding and AttackChain models."""

import uuid
from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Finding(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "findings"

    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scans.id", ondelete="CASCADE")
    )
    target_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("targets.id")
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id")
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    cvss_score: Mapped[Decimal | None] = mapped_column(Numeric(3, 1), nullable=True)
    cvss_vector: Mapped[str | None] = mapped_column(String, nullable=True)
    cwe_id: Mapped[str | None] = mapped_column(String, nullable=True)
    owasp_category: Mapped[str | None] = mapped_column(String, nullable=True)
    mitre_technique: Mapped[str | None] = mapped_column(String, nullable=True)
    affected_asset: Mapped[str] = mapped_column(String, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False)
    remediation: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String, server_default="open")
    is_chain_part: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    chain_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    scan = relationship("Scan", back_populates="findings")


class AttackChain(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "attack_chains"

    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scans.id", ondelete="CASCADE")
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    total_impact: Mapped[str] = mapped_column(String, nullable=False)
    steps: Mapped[dict] = mapped_column(JSONB, nullable=False)
    mitre_tactics: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
