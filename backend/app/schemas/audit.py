from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import AuditResult


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID | None
    action: str
    entity: str
    entity_id: UUID | None
    timestamp: datetime
    ip_address: str
    result: AuditResult
    details: dict | None
