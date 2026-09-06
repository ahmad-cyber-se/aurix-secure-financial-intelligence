from decimal import Decimal

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.enums import SubscriptionPlan
from app.models.user import User
from app.services.eligibility_service import get_eligible_etfs
from app.services.fraud_service import assess_transaction
from app.services.insight_service import build_portfolio_insight


def test_germany_free_has_limited_catalogue():
    with SessionLocal() as db:
        user = User(
            name="Unit User",
            email="unit@example.com",
            password_hash="unused",
            country="Germany",
            subscription_plan=SubscriptionPlan.FREE,
        )
        db.add(user)
        db.commit()
        etfs = get_eligible_etfs(db, user)
        assert {etf.ticker for etf in etfs} == {"IWDA", "CSPX", "EUE"}


def test_germany_premium_has_expanded_catalogue():
    with SessionLocal() as db:
        user = User(
            name="Premium User",
            email="premium@example.com",
            password_hash="unused",
            country="Germany",
            subscription_plan=SubscriptionPlan.PREMIUM,
        )
        db.add(user)
        db.commit()
        etfs = get_eligible_etfs(db, user)
        assert len(etfs) == 6


def test_uae_free_country_restriction():
    with SessionLocal() as db:
        user = User(
            name="UAE User",
            email="uae@example.com",
            password_hash="unused",
            country="UAE",
            subscription_plan=SubscriptionPlan.FREE,
        )
        db.add(user)
        db.commit()
        tickers = {etf.ticker for etf in get_eligible_etfs(db, user)}
        assert tickers == {"IWDA", "CSPX", "VWRL"}
        assert "EUE" not in tickers


def test_fraud_large_transaction_is_high_risk():
    assessment = assess_transaction(Decimal("9500"), Decimal("15000"), 0)
    assert assessment.level.value == "HIGH"
    assert "Unusually large transaction" in assessment.reason_text


def test_fraud_rapid_transactions_raise_risk():
    assessment = assess_transaction(Decimal("100"), Decimal("1000"), 3)
    assert assessment.level.value == "MEDIUM"
    assert "rapidly" in assessment.reason_text


def test_rule_based_insight_reports_precious_metals_concentration():
    summary = {"allocations": {"GOLD": Decimal("40"), "SILVER": Decimal("15"), "ETF": Decimal("35")}}
    result = build_portfolio_insight(summary)
    assert result["portfolio_risk"] == "Medium"
    assert "55.00%" in result["observation"]
    assert result["engine"] == "RULE-BASED"
