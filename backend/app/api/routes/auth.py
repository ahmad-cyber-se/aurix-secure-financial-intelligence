from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import client_ip, get_current_user, get_token_payload
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.audit import RevokedToken
from app.models.enums import AssetType, AuditResult
from app.models.etf import ETF
from app.models.portfolio import Portfolio, PortfolioAsset
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.audit_service import add_audit_log

router = APIRouter(prefix="/auth", tags=["Authentication"])


def create_initial_portfolio(db: Session, user: User) -> Portfolio:
    portfolio = Portfolio(user_id=user.id, base_currency="EUR")
    db.add(portfolio)
    db.flush()
    default_etf = db.scalar(select(ETF).where(ETF.ticker == "IWDA"))
    db.add_all(
        [
            PortfolioAsset(portfolio_id=portfolio.id, asset_type=AssetType.GOLD, name="Gold", current_value=4000),
            PortfolioAsset(portfolio_id=portfolio.id, asset_type=AssetType.SILVER, name="Silver", current_value=1500),
            PortfolioAsset(
                portfolio_id=portfolio.id,
                asset_type=AssetType.ETF,
                etf_id=default_etf.id if default_etf else None,
                name=default_etf.name if default_etf else "MSCI World ETF",
                current_value=3500,
            ),
            PortfolioAsset(portfolio_id=portfolio.id, asset_type=AssetType.CASH, name="Cash", current_value=1000),
        ]
    )
    return portfolio


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    normalized_email = payload.email.lower()
    if db.scalar(select(User.id).where(User.email == normalized_email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")

    user = User(
        name=payload.name.strip(),
        email=normalized_email,
        password_hash=hash_password(payload.password),
        country=payload.country.strip(),
        subscription_plan=payload.subscription_plan,
    )
    db.add(user)
    db.flush()
    create_initial_portfolio(db, user)
    add_audit_log(
        db,
        user_id=user.id,
        action="REGISTER",
        entity="USER",
        entity_id=user.id,
        ip_address=client_ip(request),
        result=AuditResult.SUCCESS,
    )
    token, _, _ = create_access_token(user.id)
    db.commit()
    return TokenResponse(access_token=token, expires_in=settings.jwt_expire_minutes * 60)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        add_audit_log(
            db,
            user_id=user.id if user else None,
            action="FAILED_LOGIN",
            entity="USER",
            entity_id=user.id if user else None,
            ip_address=client_ip(request),
            result=AuditResult.FAILURE,
            details={"email": payload.email.lower()},
        )
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token, _, _ = create_access_token(user.id)
    add_audit_log(
        db,
        user_id=user.id,
        action="LOGIN",
        entity="USER",
        entity_id=user.id,
        ip_address=client_ip(request),
        result=AuditResult.SUCCESS,
    )
    db.commit()
    return TokenResponse(access_token=token, expires_in=settings.jwt_expire_minutes * 60)


@router.post("/logout", status_code=200)
def logout(
    request: Request,
    payload: dict = Depends(get_token_payload),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    db.add(RevokedToken(jti=payload["jti"], user_id=user.id, expires_at=expires_at))
    add_audit_log(
        db,
        user_id=user.id,
        action="LOGOUT",
        entity="USER",
        entity_id=user.id,
        ip_address=client_ip(request),
        result=AuditResult.SUCCESS,
    )
    db.commit()
    return {"message": "Logged out successfully"}
