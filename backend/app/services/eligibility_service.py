from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.etf import ETF, EligibilityRule
from app.models.user import User


def get_eligible_etfs(db: Session, user: User) -> list[ETF]:
    stmt = (
        select(ETF)
        .join(EligibilityRule, EligibilityRule.etf_id == ETF.id)
        .where(
            EligibilityRule.country == user.country,
            EligibilityRule.subscription_plan == user.subscription_plan,
            EligibilityRule.allowed.is_(True),
        )
        .order_by(ETF.name)
    )
    return list(db.scalars(stmt).all())


def is_etf_eligible(db: Session, user: User, etf_id: UUID) -> bool:
    stmt = select(EligibilityRule.id).where(
        EligibilityRule.country == user.country,
        EligibilityRule.subscription_plan == user.subscription_plan,
        EligibilityRule.etf_id == etf_id,
        EligibilityRule.allowed.is_(True),
    )
    return db.scalar(stmt) is not None
