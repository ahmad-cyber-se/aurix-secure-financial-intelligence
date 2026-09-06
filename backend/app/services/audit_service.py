from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.enums import AuditResult


def add_audit_log(
    db: Session,
    *,
    user_id: UUID | None,
    action: str,
    entity: str,
    entity_id: UUID | None,
    ip_address: str,
    result: AuditResult,
    details: dict | None = None,
) -> AuditLog:
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        ip_address=ip_address or "unknown",
        result=result,
        details=details,
    )
    db.add(log)
    return log
