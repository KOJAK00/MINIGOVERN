from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from .schemas import *
from .services import TagService
from src.auth.permissions import PermissionChecker

tag_service = TagService()
tag_router = APIRouter()

@tag_router.post("/",response_model=TagResponse,status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: TagCreate,
    _ = Depends(
        PermissionChecker(
            "tags.create"
        )
    ),
    session: AsyncSession = Depends(get_session)
):
    return await tag_service.create_tag(tag, session)

@tag_router.get("/",response_model=list[TagResponse])
async def get_tags(
    _ = Depends(
        PermissionChecker(
            "tags.read"
        )
    ),
    session: AsyncSession = Depends(get_session)
):
    return await tag_service.get_tags(session)

@tag_router.get("/{tag_id}",response_model=TagResponse)
async def get_tag(
    tag_id: int,
    _ = Depends(
        PermissionChecker(
            "tags.read"
        )
    ),
    session: AsyncSession = Depends(get_session)
):
    return await tag_service.get_tag(tag_id, session)

@tag_router.put("/{tag_id}",response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag: TagUpdate,
    _ = Depends(
        PermissionChecker(
            "tags.update"
        )
    ),
    session: AsyncSession = Depends(get_session)
):
    return await tag_service.update_tag(tag_id,tag,session)

@tag_router.delete("/{tag_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    _ = Depends(
        PermissionChecker(
            "tags.delete"
        )
    ),
    session: AsyncSession = Depends(get_session)
):
    await tag_service.delete_tag(tag_id,session)

@tag_router.post("/datasets/{dataset_id}/tags/{tag_id}")
async def assign_tag(
    dataset_id: int,
    tag_id: int,
    _ = Depends(
        PermissionChecker(
            "tags.update"
        )
    ),
    session: AsyncSession = Depends(get_session)
):
    return await tag_service.assign_tag_to_dataset(dataset_id,tag_id,session)

@tag_router.delete("/datasets/{dataset_id}/tags/{tag_id}")
async def remove_tag(
    dataset_id: int,
    tag_id: int,
    _ = Depends(
        PermissionChecker(
            "tags.delete"
        )
    ),
    session: AsyncSession = Depends(get_session)
):
    return await tag_service.remove_tag_from_dataset(dataset_id,tag_id,session)

@tag_router.get("/dataset/filter")
async def filter_by_tag(
    tag_name: str,
    _ = Depends(
        PermissionChecker(
            "datasources.read"
        )
    ),
    session: AsyncSession = Depends(get_session)
):
    return await tag_service.get_datasets_by_tag(tag_name,session)