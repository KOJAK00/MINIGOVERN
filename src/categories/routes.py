from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.auth.permissions import PermissionChecker
from .schemas import CategoryCreate,CategoryUpdate
from .services import CategoryService

categories_router = APIRouter()
categories_service = CategoryService()

@categories_router.post("/")
async def create_category_route(
    data: CategoryCreate,
    session: AsyncSession = Depends(get_session),
    _=Depends(
        PermissionChecker(
            "categories.create"
        )
    )
):
    return await categories_service.create_category(data,session)

@categories_router.get("/")
async def get_categories_route(
    session: AsyncSession = Depends(get_session),
    _=Depends(
        PermissionChecker(
            "categories.read"
        )
    )
):
    return await categories_service.get_categories(session)

@categories_router.get("/{category_id}")
async def get_category_route(
    category_id: int,
    session: AsyncSession = Depends(get_session),
    _=Depends(
        PermissionChecker(
            "categories.read"
        )
    )
):
    return await categories_service.get_category(category_id,session)

@categories_router.patch("/{category_id}")
async def update_category_route(
    category_id: int,
    data: CategoryUpdate,
    session: AsyncSession = Depends(get_session),
    _=Depends(
        PermissionChecker(
            "categories.update"
        )
    )
):
    return await categories_service.update_category(category_id,data,session)

@categories_router.delete("/{category_id}")
async def delete_category_route(
    category_id: int,
    session: AsyncSession = Depends(get_session),
    _=Depends(
        PermissionChecker(
            "categories.delete"
        )
    )
):
    return await categories_service.delete_category(category_id,session)