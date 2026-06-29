from datetime import datetime
from sqlmodel import SQLModel
from src.db.enum import ScanStatus

class ScanJobResponse(SQLModel):
    id: int
    datasource_id: int
    status: ScanStatus
    started_at: datetime | None
    finished_at: datetime | None
    error_message: str | None