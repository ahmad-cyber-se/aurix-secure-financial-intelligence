from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import AssetType, AuditResult, TransactionStatus, TransactionType
from app.models.etf import ETF
from app.models.portfolio import PortfolioAsset
from app.models.transaction import Transaction
from app.models.user import User
from app.services.audit_service import add_audit_log
from app.services.eligibility_service import is_etf_eligible
from app.services.fraud_service import assess_transaction
from app.services.portfolio_service import get_user_portfolio, portfolio_summary


class InvestmentError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def execute_etf_investment(db: Session, user: User, etf_id, amount: Decimal, ip_address: str):
    etf = db.get(ETF, etf_id)
    if etf is None:
        raise InvestmentError("ETF not found", 404)
    if not is_etf_eligible(db, user, etf.id):
        add_audit_log(
            db,
            user_id=user.id,
            action="INVESTMENT_DENIED",
            entity="ETF",
            entity_id=etf.id,
            ip_address=ip_address,
            result=AuditResult.DENIED,
            details={"reason": "ETF not eligible for country/subscription"},
        )
        db.commit()
        raise InvestmentError("ETF is not eligible for this user", 403)

    portfolio = get_user_portfolio(db, user)
    cash = db.scalar(
        select(PortfolioAsset).where(
            PortfolioAsset.portfolio_id == portfolio.id,
            PortfolioAsset.asset_type == AssetType.CASH,
        )
    )
    if cash is None or Decimal(cash.current_value) < amount:
        raise InvestmentError("Insufficient cash balance", 400)

    since = datetime.now(timezone.utc) - timedelta(seconds=60)
    recent_count = db.scalar(
        select(func.count(Transaction.id)).where(Transaction.user_id == user.id, Transaction.created_at >= since)
    ) or 0
    assessment = assess_transaction(amount, Decimal(cash.current_value), int(recent_count))

    try:
        cash.current_value = Decimal(cash.current_value) - amount
        etf_asset = db.scalar(
            select(PortfolioAsset).where(
                PortfolioAsset.portfolio_id == portfolio.id,
                PortfolioAsset.asset_type == AssetType.ETF,
                PortfolioAsset.etf_id == etf.id,
            )
        )
        if etf_asset is None:
            etf_asset = PortfolioAsset(
                portfolio_id=portfolio.id,
                asset_type=AssetType.ETF,
                etf_id=etf.id,
                name=etf.name,
                current_value=Decimal("0.00"),
            )
            db.add(etf_asset)
        etf_asset.current_value = Decimal(etf_asset.current_value) + amount
        portfolio.updated_at = datetime.now(timezone.utc)

        transaction = Transaction(
            user_id=user.id,
            portfolio_id=portfolio.id,
            etf_id=etf.id,
            asset=etf.name,
            type=TransactionType.ETF_BUY,
            amount=amount,
            currency=portfolio.base_currency,
            status=TransactionStatus.COMPLETED,
            risk_level=assessment.level,
            risk_reason=assessment.reason_text,
        )
        db.add(transaction)
        db.flush()

        add_audit_log(
            db,
            user_id=user.id,
            action="INVESTMENT",
            entity="TRANSACTION",
            entity_id=transaction.id,
            ip_address=ip_address,
            result=AuditResult.SUCCESS,
            details={"etf": etf.ticker, "amount": str(amount), "risk": assessment.level.value, "score": assessment.score},
        )
        add_audit_log(
            db,
            user_id=user.id,
            action="PORTFOLIO_CHANGE",
            entity="PORTFOLIO",
            entity_id=portfolio.id,
            ip_address=ip_address,
            result=AuditResult.SUCCESS,
            details={"reason": "ETF investment", "transaction_id": str(transaction.id)},
        )
        db.commit()
        db.refresh(transaction)
        return transaction, portfolio_summary(db, user)
    except Exception:
        db.rollback()
        raise
