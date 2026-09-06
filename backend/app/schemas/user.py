from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import KYCStatus, SubscriptionPlan


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str
    country: str
    subscription_plan: SubscriptionPlan
    kyc_status: KYCStatus
    created_at: datetime


class UserUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    country: str | None = Field(default=None, min_length=2, max_length=80)
    subscription_plan: SubscriptionPlan | None = None
