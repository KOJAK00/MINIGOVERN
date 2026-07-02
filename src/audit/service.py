from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import AuditLog
from sqlmodel import select

class AuditService:

    async def log(
        self,
        action,
        entity_type: str,
        entity_id: int,
        user_id: int,
        session: AsyncSession,
    ):

        log = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            user_id=user_id,
        )

        session.add(log)
        await session.commit()

    async def get_logs(
        self,
        session: AsyncSession,
    ):
        logs = await session.execute(
            select(AuditLog).order_by(AuditLog.created_at.desc())
        )
        return logs.scalars().all()