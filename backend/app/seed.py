from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import SubscriptionPlan
from app.models.etf import ETF, EligibilityRule

ETF_DATA = [
    {"name": "MSCI World", "ticker": "IWDA", "isin": "IE00B4L5Y983", "provider": "iShares", "asset_class": "Equity", "region": "Global Developed", "currency": "EUR", "expense_ratio": Decimal("0.0020"), "risk_level": "MEDIUM"},
    {"name": "S&P 500", "ticker": "CSPX", "isin": "IE00B5BMR087", "provider": "iShares", "asset_class": "Equity", "region": "United States", "currency": "EUR", "expense_ratio": Decimal("0.0007"), "risk_level": "MEDIUM"},
    {"name": "Nasdaq-100", "ticker": "CNDX", "isin": "IE00B53SZB19", "provider": "iShares", "asset_class": "Equity", "region": "United States", "currency": "EUR", "expense_ratio": Decimal("0.0033"), "risk_level": "HIGH"},
    {"name": "FTSE All-World", "ticker": "VWRL", "isin": "IE00B3RBWM25", "provider": "Vanguard", "asset_class": "Equity", "region": "Global", "currency": "EUR", "expense_ratio": Decimal("0.0022"), "risk_level": "MEDIUM"},
    {"name": "Emerging Markets", "ticker": "EIMI", "isin": "IE00BKM4GZ66", "provider": "iShares", "asset_class": "Equity", "region": "Emerging Markets", "currency": "EUR", "expense_ratio": Decimal("0.0018"), "risk_level": "HIGH"},
    {"name": "Euro Stoxx 50", "ticker": "EUE", "isin": "IE00B53L3W79", "provider": "iShares", "asset_class": "Equity", "region": "Eurozone", "currency": "EUR", "expense_ratio": Decimal("0.0010"), "risk_level": "MEDIUM"},
]

RULES = {
    ("Germany", SubscriptionPlan.FREE): {"IWDA", "CSPX", "EUE"},
    ("Germany", SubscriptionPlan.PREMIUM): {"IWDA", "CSPX", "CNDX", "VWRL", "EIMI", "EUE"},
    ("UAE", SubscriptionPlan.FREE): {"IWDA", "CSPX", "VWRL"},
    ("UAE", SubscriptionPlan.PREMIUM): {"IWDA", "CSPX", "CNDX", "VWRL", "EIMI", "EUE"},
}


def seed_reference_data(db: Session) -> None:
    if db.scalar(select(ETF.id).limit(1)) is None:
        db.add_all([ETF(**item) for item in ETF_DATA])
        db.commit()

    etfs = {etf.ticker: etf for etf in db.scalars(select(ETF)).all()}
    existing = db.scalar(select(EligibilityRule.id).limit(1))
    if existing is None:
        for (country, plan), tickers in RULES.items():
            for ticker in tickers:
                db.add(EligibilityRule(country=country, subscription_plan=plan, etf_id=etfs[ticker].id, allowed=True))
        db.commit()
