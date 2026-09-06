import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base
from app.models.enums import AssetType


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    base_currency: Mapped[str] = mapped_column(String(3), default="EUR", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="portfolio")
    assets = relationship("PortfolioAsset", back_populates="portfolio", cascade="all, delete-orphan")


class PortfolioAsset(Base):
    __tablename__ = "portfolio_assets"
    __table_args__ = (UniqueConstraint("portfolio_id", "asset_type", "etf_id", "name", name="uq_portfolio_asset"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)
    asset_type: Mapped[AssetType] = mapped_column(Enum(AssetType, native_enum=False), nullable=False, index=True)
    etf_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("etfs.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    current_value: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=Decimal("0.00"), nullable=False)

    portfolio = relationship("Portfolio", back_populates="assets")
    etf = relationship("ETF")
