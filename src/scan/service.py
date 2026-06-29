from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import DataSource, ScanJob,Dataset
from src.db.enum import ScanStatus
from datetime import datetime
from sqlmodel import delete
class ScanService:
    async def create_scan_job(
    self,
    datasource_id: int,
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

        return scan_job
    async def clear_old_scan(
    self,
    datasource_id: int,
    session
):
        statement = delete(Dataset).where(
            Dataset.datasource_id == datasource_id
        )

        await session.execute(statement)

        await session.commit()