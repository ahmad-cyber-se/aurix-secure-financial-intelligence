from pydantic import BaseModel, EmailStr, Field

from app.models.enums import SubscriptionPlan


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    country: str = Field(min_length=2, max_length=80)
    subscription_plan: SubscriptionPlan = SubscriptionPlan.FREE


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
