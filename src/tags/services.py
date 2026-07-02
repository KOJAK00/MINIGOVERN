from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Tag, DatasetTag,Dataset
from .schemas import TagCreate,TagUpdate
from fastapi import HTTPException
from src.common.base_service import BaseService
from src.db.enum import AuditAction

class TagService(BaseService):
    async def get_tag_by_name(
        self,
        name: str,
        session: AsyncSession
    ):
        return await session.scalar(
            select(Tag).where(Tag.name == name)
            )


    async def attach_tag_to_dataset(
        self,
        dataset_id: int,
        tag_name: str,
        session: AsyncSession
    ):

        tag = await self.get_tag_by_name(tag_name, session)

        if not tag:
            return
        
        exists = await session.scalar(
            select(DatasetTag).where(
                DatasetTag.dataset_id == dataset_id,
                DatasetTag.tag_id == tag.id
            )
        )
        if exists:
            return
        session.add(
            DatasetTag(
                dataset_id=dataset_id,
                tag_id=tag.id
            )
        )

    async def create_tag(
        self,
        tag_data: TagCreate,
        session: AsyncSession
    ):

        exists = await session.scalar(
            select(Tag).where(Tag.name == tag_data.name)
        )

        if exists:
            raise HTTPException(
                status_code=400,
                detail="Tag already exists"
            )

        tag = Tag(**tag_data.model_dump())

        session.add(tag)

        await session.commit()

        await session.refresh(tag)

        return tag

    async def get_tags(self, session: AsyncSession):

        result = await session.exec(select(Tag))

        return result.all()

    async def get_tag(
        self,
        tag_id: int,
        session: AsyncSession
    ):

        tag = await session.get(Tag, tag_id)

        if not tag:
            raise HTTPException(
                status_code=404,
                detail="Tag not found"
            )

        return tag

    async def update_tag(
        self,
        tag_id: int,
        tag_data: TagUpdate,
        session: AsyncSession
    ):

        tag = await self.get_tag(tag_id, session)

        tag.sqlmodel_update(tag_data.model_dump())

        session.add(tag)

        await session.commit()

        await session.refresh(tag)

        return tag

    async def delete_tag(
        self,
        tag_id: int,
        session: AsyncSession
    ):

        tag = await self.get_tag(tag_id, session)

        await session.delete(tag)

        await session.commit()
    
    async def assign_tag_to_dataset(
    self,
    dataset_id: int,
    tag_id: int,
    bg_tasks,
    current_user,
    session: AsyncSession
):
        dataset = await session.get(Dataset, dataset_id)
        if not dataset:
            raise HTTPException(
                status_code=404,
                detail="Dataset not found"
            )
        
        tag = await session.get(Tag, tag_id)
        if not tag:
            raise HTTPException(
                status_code=404,
                detail="Tag not found"
            )
        
        exists = await session.scalar(
            select(DatasetTag).where(
                DatasetTag.dataset_id == dataset_id,
                DatasetTag.tag_id == tag_id
            )
        )
        if exists:
            raise HTTPException(
                status_code=400,
                detail="Tag already assigned"
            )
        
        session.add(
            DatasetTag(
                dataset_id=dataset_id,
                tag_id=tag_id
            )
        )
        await session.commit()
        self.create_audit(
            bg_tasks,
            AuditAction.ASSIGN_TAG,
            "TAG",
            tag_id,
            current_user.id,
            session
        )
        return {"message": "Tag assigned successfully"}
    
    async def remove_tag_from_dataset(
    self,
    dataset_id: int,
    tag_id: int,
    bg_tasks,
    current_user,
    session: AsyncSession
):
        relation = await session.scalar(
            select(DatasetTag).where(
                DatasetTag.dataset_id == dataset_id,
                DatasetTag.tag_id == tag_id
            )
        )
        if not relation:
            raise HTTPException(
                status_code=404,
                detail="Relation not found"
            )
        
        await session.delete(relation)
        await session.commit()
        self.create_audit(
            bg_tasks,
            AuditAction.REMOVE_TAG,
            "TAG",
            tag_id,
            current_user.id,
            session
        )
        return {"message": "Tag removed successfully"}
    
    async def get_datasets_by_tag(
    self,
    tag_name: str,
    session: AsyncSession
):

        statement = (
            select(Dataset)
            .join(DatasetTag)
            .join(Tag)
            .where(Tag.name == tag_name)
        )

        result = await session.exec(statement)
        return result.all()