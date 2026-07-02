from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import DataSource, ScanJob,Dataset
from src.db.enum import ScanStatus
from datetime import datetime
from sqlmodel import delete
from src.common.base_service import BaseService
from src.db.enum import AuditAction

class ScanService(BaseService):

    async def create_scan_job(
    self,
    datasource_id: int,
    bg_tasks,
    current_user,
    session: AsyncSession
):
        datasource = await session.get(
            DataSource,
            datasource_id)
        if not datasource:
            raise HTTPException(
                status_code=404,
                detail="Datasource not found"
            )
        scan_job = ScanJob(
            datasource_id=datasource.id,
            status=ScanStatus.PENDING,
            started_at=datetime.now()
        )
        session.add(scan_job)
        await session.commit()
        await session.refresh(scan_job)
        self.create_audit(
            bg_tasks,
            AuditAction.START_SCAN,
            "SCAN",
            scan_job.id,
            current_user.id,
            session
        )
        return scan_job
        
    async def clear_old_scan(
    self,
    datasource_id: int,
    session
):
        statement = delete(Dataset).where(Dataset.datasource_id == datasource_id)
        await session.execute(statement)

        await session.commit()