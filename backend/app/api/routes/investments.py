from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import client_ip, get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.transaction import InvestmentRequest, InvestmentResponse
from app.services.investment_service import InvestmentError, execute_etf_investment

router = APIRouter(prefix="/investments", tags=["Investments"])


@router.post("", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
def invest(
    payload: InvestmentRequest,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        transaction, portfolio = execute_etf_investment(db, user, payload.etf_id, payload.amount, client_ip(request))
        return {"transaction": transaction, "portfolio": portfolio}
    except InvestmentError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))
