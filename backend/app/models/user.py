import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base
from app.models.enums import KYCStatus, SubscriptionPlan


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    country: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    subscription_plan: Mapped[SubscriptionPlan] = mapped_column(
        Enum(SubscriptionPlan, native_enum=False), default=SubscriptionPlan.FREE, nullable=False
    )
    kyc_status: Mapped[KYCStatus] = mapped_column(
        Enum(KYCStatus, native_enum=False), default=KYCStatus.PENDING, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    portfolio = relationship("Portfolio", back_populates="user", uselist=False, cascade="all, delete-orphan")
