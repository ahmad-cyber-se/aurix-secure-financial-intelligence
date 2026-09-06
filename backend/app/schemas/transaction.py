from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import RiskLevel, TransactionStatus, TransactionType
from app.schemas.portfolio import PortfolioResponse


class InvestmentRequest(BaseModel):
    etf_id: UUID
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    asset: str
    type: TransactionType
    amount: Decimal
    currency: str
    status: TransactionStatus
    risk_level: RiskLevel
    risk_reason: str
    created_at: datetime


class InvestmentResponse(BaseModel):
    transaction: TransactionResponse
    portfolio: PortfolioResponse
