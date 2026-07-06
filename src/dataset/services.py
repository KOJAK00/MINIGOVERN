from fastapi import HTTPException
from src.db.enum import DatasetState
from src.db.models import Dataset
from sqlmodel.ext.asyncio.session import AsyncSession
from src.dataset.schemas import RejectDatasetRequest
from src.common.base_service import BaseService
from src.db.enum import AuditAction
from sqlmodel import select

class DatasetService(BaseService):
    async def get_datasets(
        self,
        session: AsyncSession
    ):
        datasets = await session.exec(
            select(Dataset)
        )
        return datasets.all()
    async def submit_dataset(
        self,
        dataset_id: int,
        bg_tasks,
        current_user,
        session: AsyncSession
):
        dataset = await session.get(Dataset, dataset_id)
        if not dataset:
            raise HTTPException(404, "Dataset not found")

        if dataset.state != DatasetState.DRAFT:
            raise HTTPException(
                400,
                "Only draft datasets can be submitted"
            )

        dataset.state = DatasetState.SUBMITTED
        session.add(dataset)
        await session.commit()
        await session.refresh(dataset)
        self.create_audit(
            bg_tasks,
            AuditAction.SUBMIT_DATASET,
            "DATASET",
            dataset.id,
            current_user.id,
            session
        )
        return dataset

    async def approve_dataset(
        self,
        dataset_id: int,
        bg_tasks,
        current_user,
        session: AsyncSession
    ):
        dataset = await session.get(Dataset, dataset_id)
        if not dataset:
            raise HTTPException(404, "Dataset not found")

        if dataset.state != DatasetState.SUBMITTED:
            raise HTTPException(
                400,
                "Only submitted datasets can be approved"
            )

        dataset.state = DatasetState.APPROVED
        session.add(dataset)
        await session.commit()
        await session.refresh(dataset)
        self.create_audit(
            bg_tasks,
            AuditAction.APPROVE_DATASET,
            "DATASET",
            dataset.id,
            current_user.id,
            session
        )
        return dataset

    async def reject_dataset(
        self,
        dataset_id: int,
        comment: RejectDatasetRequest,
        bg_tasks,
        current_user,
        session: AsyncSession
    ):
        dataset = await session.get(Dataset, dataset_id)
        if not dataset:
            raise HTTPException(404, "Dataset not found")

        if dataset.state != DatasetState.SUBMITTED:
            raise HTTPException(
                400,
                "Only submitted datasets can be rejected"
            )
        
        dataset.state = DatasetState.REJECTED
        dataset.rejection_comment = comment.comment
        session.add(dataset)
        await session.commit()
        await session.refresh(dataset)
        self.create_audit(
            bg_tasks,
            AuditAction.REJECT_DATASET,
            "DATASET",
            dataset.id,
            current_user.id,
            session
        )
        return dataset
    
    async def return_to_draft(
    self,
    dataset_id: int,
    session: AsyncSession
    ):
        dataset = await session.get(Dataset, dataset_id)
        if not dataset:
            raise HTTPException(404, "Dataset not found")

        if dataset.state != DatasetState.REJECTED:
            raise HTTPException(
                400,
                "Only rejected datasets can return to draft"
            )
        
        dataset.state = DatasetState.DRAFT
        dataset.rejection_comment = None
        session.add(dataset)
        await session.commit()
        await session.refresh(dataset)
        return dataset
    
    async def get_dataset_by_id(
        self,
        dataset_id: int,
        session: AsyncSession
    ):
        dataset = await session.get(Dataset, dataset_id)
        if not dataset:
            raise HTTPException(404, "Dataset not found")
        return dataset