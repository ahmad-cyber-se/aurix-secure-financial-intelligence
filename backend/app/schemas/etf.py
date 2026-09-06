from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ETFResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    ticker: str
    isin: str
    provider: str
    asset_class: str
    region: str
    currency: str
    expense_ratio: Decimal
    risk_level: str
