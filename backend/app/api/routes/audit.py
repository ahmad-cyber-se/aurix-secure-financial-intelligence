from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.audit import AuditLog
from app.models.user import User
from app.schemas.audit import AuditLogResponse

router = APIRouter(prefix="/audit-logs", tags=["Audit"])


@router.get("", response_model=list[AuditLogResponse])
def list_audit_logs(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = (
        select(AuditLog)
        .where(AuditLog.user_id == user.id)
        .order_by(AuditLog.timestamp.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(stmt).all())
