from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import AssetType
from app.models.portfolio import Portfolio, PortfolioAsset
from app.models.user import User

TWO_DP = Decimal("0.01")


def money(value) -> Decimal:
    return Decimal(value or 0).quantize(TWO_DP, rounding=ROUND_HALF_UP)


def get_user_portfolio(db: Session, user: User) -> Portfolio:
    portfolio = db.scalar(select(Portfolio).where(Portfolio.user_id == user.id))
    if portfolio is None:
        raise LookupError("Portfolio not found")
    return portfolio


def portfolio_summary(db: Session, user: User) -> dict:
    portfolio = get_user_portfolio(db, user)
    assets = list(db.scalars(select(PortfolioAsset).where(PortfolioAsset.portfolio_id == portfolio.id)).all())
    totals = {asset_type: Decimal("0.00") for asset_type in AssetType}
    for asset in assets:
        totals[asset.asset_type] += money(asset.current_value)
    total_value = money(sum(totals.values(), Decimal("0.00")))
    allocations = {}
    for asset_type in AssetType:
        allocations[asset_type.value] = (
            money((totals[asset_type] / total_value) * Decimal("100")) if total_value > 0 else Decimal("0.00")
        )
    return {
        "id": portfolio.id,
        "base_currency": portfolio.base_currency,
        "total_value": total_value,
        "gold": money(totals[AssetType.GOLD]),
        "silver": money(totals[AssetType.SILVER]),
        "etfs": money(totals[AssetType.ETF]),
        "cash": money(totals[AssetType.CASH]),
        "other_assets": money(totals[AssetType.OTHER]),
        "allocations": allocations,
    }


def portfolio_assets(db: Session, user: User) -> list[dict]:
    portfolio = get_user_portfolio(db, user)
    assets = list(db.scalars(select(PortfolioAsset).where(PortfolioAsset.portfolio_id == portfolio.id)).all())
    total = sum((money(a.current_value) for a in assets), Decimal("0.00"))
    return [
        {
            "id": a.id,
            "asset_type": a.asset_type.value,
            "name": a.name,
            "etf_id": a.etf_id,
            "current_value": money(a.current_value),
            "allocation_percent": money((money(a.current_value) / total) * Decimal("100")) if total else Decimal("0.00"),
        }
        for a in assets
    ]
