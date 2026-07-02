from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .services import DatasetService
from .schemas import RejectDatasetRequest
from src.auth.permissions import PermissionChecker

dataset_router = APIRouter()
dataset_service = DatasetService()

@dataset_router.get("/{dataset_id}")
async def get_dataset(
    dataset_id: int,
    _=Depends(
        PermissionChecker(
            "dataset.read")
            ),
    session: AsyncSession = Depends(get_session)
):
    return await dataset_service.get_dataset_by_id(dataset_id, session)

@dataset_router.post("/{dataset_id}/submit")
async def submit_dataset(
    dataset_id: int,
    _=Depends(
        PermissionChecker(
            "dataset.submit")
            ),
    session: AsyncSession = Depends(get_session)
):
    return await dataset_service.submit_dataset(dataset_id, session)

@dataset_router.post("/{dataset_id}/approve")
async def approve_dataset(
    dataset_id: int,
    _=Depends(
        PermissionChecker(
            "dataset.approve")
            ),
    session: AsyncSession = Depends(get_session)
):
    return await dataset_service.approve_dataset(dataset_id, session)

@dataset_router.post("/{dataset_id}/reject")
async def reject_dataset(
    dataset_id: int,
    comment: RejectDatasetRequest,
    _=Depends(
        PermissionChecker(
            "dataset.reject")
            ),
    session: AsyncSession = Depends(get_session)
):
    return await dataset_service.reject_dataset(dataset_id, comment, session)

@dataset_router.post("/{dataset_id}/draft")
async def create_draft(
    dataset_id: int,
    _=Depends(
        PermissionChecker(
            "dataset.reject")
            ),
    session: AsyncSession = Depends(get_session)
):
    return await dataset_service.return_to_draft(dataset_id, session)