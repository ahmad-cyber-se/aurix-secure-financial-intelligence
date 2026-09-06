from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class PortfolioAssetResponse(BaseModel):
    id: UUID
    asset_type: str
    name: str
    etf_id: UUID | None = None
    current_value: Decimal
    allocation_percent: Decimal


class PortfolioResponse(BaseModel):
    id: UUID
    base_currency: str
    total_value: Decimal
    gold: Decimal
    silver: Decimal
    etfs: Decimal
    cash: Decimal
    other_assets: Decimal
    allocations: dict[str, Decimal]


class PortfolioAssetsResponse(BaseModel):
    assets: list[PortfolioAssetResponse]
