from enum import StrEnum


class SubscriptionPlan(StrEnum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"


class KYCStatus(StrEnum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class AssetType(StrEnum):
    GOLD = "GOLD"
    SILVER = "SILVER"
    ETF = "ETF"
    CASH = "CASH"
    OTHER = "OTHER"


class TransactionType(StrEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    ETF_BUY = "ETF_BUY"
    ETF_SELL = "ETF_SELL"
    GOLD_BUY = "GOLD_BUY"
    SILVER_BUY = "SILVER_BUY"


class TransactionStatus(StrEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"
    FLAGGED = "FLAGGED"


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AuditResult(StrEnum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    DENIED = "DENIED"
