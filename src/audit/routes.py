from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from .service import AuditService
from .schemas import AuditLogResponse

audit_router = APIRouter()
audit_service = AuditService()

@audit_router.get("/", response_model=list[AuditLogResponse])
async def get_audit_logs(
    session: AsyncSession = Depends(get_session)
):
    return await audit_service.get_logs(session)