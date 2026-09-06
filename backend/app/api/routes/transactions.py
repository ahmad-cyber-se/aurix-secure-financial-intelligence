from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=list[TransactionResponse])
def list_transactions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Transaction)
        .where(Transaction.user_id == user.id)
        .order_by(Transaction.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(stmt).all())
