import uuid
from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base
from app.models.enums import SubscriptionPlan
from sqlalchemy import Enum


class ETF(Base):
    __tablename__ = "etfs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    ticker: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    isin: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(120), nullable=False)
    asset_class: Mapped[str] = mapped_column(String(80), nullable=False)
    region: Mapped[str] = mapped_column(String(80), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    expense_ratio: Mapped[Decimal] = mapped_column(Numeric(6, 4), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)


class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"
    __table_args__ = (UniqueConstraint("country", "subscription_plan", "etf_id", name="uq_eligibility_rule"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    country: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        Enum(SubscriptionPlan, native_enum=False), nullable=False, index=True
    )
    etf_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("etfs.id", ondelete="CASCADE"), nullable=False)
    allowed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    etf = relationship("ETF")
