from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CategoryCreate,CategoryUpdate
from src.db.models import Category
from src.errors import CategoryAlreadyExists,CategoryNotFound
class CategoryService:
    async def create_category(
    self,
    data: CategoryCreate,
    session: AsyncSession
):
        existing = await session.scalar(
            select(Category).where(
                Category.name == data.name
            )
        )

        if existing:
            raise CategoryAlreadyExists

        category = Category(**data.model_dump())

        session.add(category)

        await session.commit()
        await session.refresh(category)

        return category
    
    async def get_categories(
    self,
    session: AsyncSession
):
        result = await session.exec(
            select(Category)
        )

        return result.all()
    
    async def get_category(
    self,
    category_id: int,
    session: AsyncSession
):
        category = await session.get(
            Category,
            category_id
        )

        if not category:
            raise CategoryNotFound

        return category
    
    async def get_category_by_name(
    self,
    category_name: str,
    session: AsyncSession
):
        statement = select(Category).where(Category.name == category_name)

        result = await session.exec(statement)

        return result.first()
    
    async def update_category(
    self,
    category_id: int,
    data: CategoryUpdate,
    session: AsyncSession
):
        category = await session.get(
            Category,
            category_id
        )
        if not category:
            raise CategoryNotFound()

        update_data = data.model_dump(
            exclude_unset=True
        )
        if "name" in update_data:
            existing = await self.get_category_by_name(
                update_data["name"],
                session
                )
            
            if existing and existing.id != category_id:
                raise CategoryAlreadyExists()
            
        for key, value in update_data.items():
            setattr(category, key, value)

        session.add(category)

        await session.commit()
        await session.refresh(category)

        return category
    
    async def delete_category(
    self,
    category_id: int,
    session: AsyncSession
):
        category = await session.get(
            Category,
            category_id
        )

        if not category:
            raise CategoryNotFound

        await session.delete(category)

        await session.commit()

        return {
            "message": "Category deleted"
        }