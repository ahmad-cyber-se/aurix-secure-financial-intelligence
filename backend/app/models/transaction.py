import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from app.db.base import Base
from app.models.enums import RiskLevel, TransactionStatus, TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    portfolio_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)
    etf_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("etfs.id", ondelete="SET NULL"), nullable=True)
    asset: Mapped[str] = mapped_column(String(160), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType, native_enum=False), nullable=False, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="EUR", nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus, native_enum=False), nullable=False, index=True)
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel, native_enum=False), nullable=False)
    risk_reason: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
