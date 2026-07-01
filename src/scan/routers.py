import asyncio
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.permissions import PermissionChecker
from .schemas import ScanJobResponse
from .service import ScanService
from .background import run_scan

scan_router = APIRouter()
scan_service=ScanService()

@scan_router.post(
    "/{datasource_id}",
    response_model=ScanJobResponse
)
async def scan(
    datasource_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(
        PermissionChecker("scan.run")
    ),
):
    scan_job = await scan_service.create_scan_job(datasource_id,session)
    asyncio.create_task(run_scan(scan_job.id))
    return scan_job