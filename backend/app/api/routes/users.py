from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import client_ip, get_current_user
from app.db.session import get_db
from app.models.enums import AuditResult
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionResponse
from app.schemas.user import UserResponse, UserUpdateRequest
from app.services.audit_service import add_audit_log
from app.services.portfolio_service import portfolio_summary

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserResponse)
def update_me(
    payload: UserUpdateRequest,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    changes = payload.model_dump(exclude_none=True)
    for field, value in changes.items():
        setattr(user, field, value)
    add_audit_log(
        db,
        user_id=user.id,
        action="PROFILE_CHANGE",
        entity="USER",
        entity_id=user.id,
        ip_address=client_ip(request),
        result=AuditResult.SUCCESS,
        details={"fields": list(changes.keys())},
    )
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}/portfolio")
def portfolio_authorization_demo(
    user_id: UUID,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id != user.id:
        add_audit_log(
            db,
            user_id=user.id,
            action="UNAUTHORIZED_ACCESS_ATTEMPT",
            entity="PORTFOLIO",
            entity_id=user_id,
            ip_address=client_ip(request),
            result=AuditResult.DENIED,
            details={"requested_user_id": str(user_id)},
        )
        db.commit()
        raise HTTPException(status_code=403, detail="You may only access your own portfolio")
    return portfolio_summary(db, user)


@router.get("/{user_id}/transactions", response_model=list[TransactionResponse])
def transactions_authorization_demo(
    user_id: UUID,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_id != user.id:
        add_audit_log(
            db,
            user_id=user.id,
            action="UNAUTHORIZED_ACCESS_ATTEMPT",
            entity="TRANSACTIONS",
            entity_id=user_id,
            ip_address=client_ip(request),
            result=AuditResult.DENIED,
            details={"requested_user_id": str(user_id)},
        )
        db.commit()
        raise HTTPException(status_code=403, detail="You may only access your own transactions")
    return list(db.scalars(select(Transaction).where(Transaction.user_id == user.id).order_by(Transaction.created_at.desc())).all())
