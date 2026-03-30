"""Organization (tenant) model."""


from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class Organization(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    plan: Mapped[str] = mapped_column(String, server_default="free")
    settings: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'"))

    members = relationship("OrgMembership", back_populates="organization")
    targets = relationship("Target", back_populates="organization")
    scans = relationship("Scan", back_populates="organization")
