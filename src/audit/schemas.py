from pydantic import BaseModel
from datetime import datetime

class AuditLogResponse(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: int
    user_id: int
    created_at: datetime
