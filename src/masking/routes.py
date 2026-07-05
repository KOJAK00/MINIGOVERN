from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from .service import MaskingService
from src.auth.dependencies import get_current_user

masking_service=MaskingService()
masking_router=APIRouter()

@masking_router.get("/preview/{dataset_id}")
async def preview_dataset(
    dataset_id:int,
    _= Depends(get_current_user),
    session:AsyncSession=Depends(get_session)
):
    return await masking_service.preview_dataset(dataset_id,session)