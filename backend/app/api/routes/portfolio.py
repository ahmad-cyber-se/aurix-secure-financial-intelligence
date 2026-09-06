from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.insight import InsightResponse
from app.schemas.portfolio import PortfolioAssetsResponse, PortfolioResponse
from app.services.insight_service import build_portfolio_insight
from app.services.portfolio_service import portfolio_assets, portfolio_summary

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("", response_model=PortfolioResponse)
def get_portfolio(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return portfolio_summary(db, user)


@router.get("/assets", response_model=PortfolioAssetsResponse)
def get_assets(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"assets": portfolio_assets(db, user)}


@router.get("/insights", response_model=InsightResponse)
def get_insights(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return build_portfolio_insight(portfolio_summary(db, user))
