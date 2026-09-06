from dataclasses import dataclass
from decimal import Decimal

from app.models.enums import RiskLevel


@dataclass(frozen=True)
class FraudAssessment:
    level: RiskLevel
    score: int
    reasons: list[str]

    @property
    def reason_text(self) -> str:
        return "; ".join(self.reasons) if self.reasons else "No anomaly detected"


def assess_transaction(amount: Decimal, cash_balance: Decimal, recent_transaction_count: int) -> FraudAssessment:
    score = 10
    reasons: list[str] = []

    if amount >= Decimal("7500"):
        score += 70
        reasons.append("Unusually large transaction")
    elif amount >= Decimal("3000"):
        score += 35
        reasons.append("Large transaction amount")

    if cash_balance > 0 and amount / cash_balance >= Decimal("0.80"):
        score += 45
        reasons.append("Transaction uses at least 80% of available cash")

    if recent_transaction_count >= 2:
        score += 35
        reasons.append("Multiple transactions occurred rapidly")

    score = min(score, 100)
    if score >= 70:
        level = RiskLevel.HIGH
    elif score >= 40:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW
    return FraudAssessment(level=level, score=score, reasons=reasons)
