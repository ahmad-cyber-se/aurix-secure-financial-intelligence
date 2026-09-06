from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.etf import ETF
from app.models.user import User
from app.schemas.etf import ETFResponse
from app.services.eligibility_service import get_eligible_etfs, is_etf_eligible

router = APIRouter(prefix="/etfs", tags=["ETFs"])


@router.get("", response_model=list[ETFResponse])
def list_etfs(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_eligible_etfs(db, user)[offset : offset + limit]


@router.get("/{etf_id}", response_model=ETFResponse)
def get_etf(etf_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    etf = db.get(ETF, etf_id)
    if etf is None:
        raise HTTPException(status_code=404, detail="ETF not found")
    if not is_etf_eligible(db, user, etf_id):
        raise HTTPException(status_code=403, detail="ETF is not available for your country/subscription")
    return etf
