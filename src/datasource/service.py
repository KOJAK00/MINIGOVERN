from sqlmodel import select
from .schemas import DataSourceCreate,DataSourceUpdate
from src.db.models import DataSource, Category
from src.errors import CategoryNotFound,DataSourceNotFound,InsufficientPermission
from src.common.encryption import encrypt_password
class DataService():
    async def create_datasource(
    self,
    data: DataSourceCreate,
    current_user,
    session
):
        category = await session.get(
            Category,
            data.category_id
        )

        if not category:
            raise CategoryNotFound

        datasource = DataSource(
            name=data.name,
            host=data.host,
            port=data.port,
            database_name=data.database_name,
            username=data.username,
            encrypted_password=encrypt_password(
                data.password
            ),
            owner_id=current_user.id,
            category_id=data.category_id
        )

        session.add(datasource)

        await session.commit()
        await session.refresh(datasource)

        return datasource
    
    async def get_datasources(
    self,
    current_user,
    session
    ):
        if current_user.role.name == "admin":

            result = await session.exec(
                select(DataSource)
            )

            return result.all()
        result = await session.exec(
        select(DataSource).where(
            DataSource.owner_id == current_user.id
        )
    )

        return result.all()
    
    async def get_datasource(
    self,
    datasource_id: int,
    current_user,
    session
):      
        
        datasource = await session.get(
            DataSource,
            datasource_id
        )
        if (
        current_user.role.name != "admin"
        and datasource.owner_id != current_user.id):
            raise InsufficientPermission()
        
        if not datasource:
            raise DataSourceNotFound()
        
        return datasource
    
    async def update_datasource(
    self,
    datasource_id: int,
    data:DataSourceUpdate,
    current_user,
    session
):
        datasource = await session.get(
            DataSource,
            datasource_id
        )
        if (
        current_user.role.name != "admin"
        and datasource.owner_id != current_user.id):
            raise InsufficientPermission()
        if not datasource:
            raise DataSourceNotFound()

        update_data = data.model_dump(
            exclude_unset=True
        )
        if "password" in update_data:
            datasource.encrypted_password = (
                encrypt_password(
                    update_data.pop("password")
                )
    )
        for key, value in update_data.items():
            setattr(datasource, key, value)

        session.add(datasource)

        await session.commit()
        await session.refresh(datasource)

        return datasource
    
    async def delete_datasource(
    self,
    datasource_id: int,
    current_user,
    session
):
        datasource = await session.get(
            DataSource,
            datasource_id
        )

        if (
        current_user.role.name != "admin"
        and datasource.owner_id != current_user.id):
            raise InsufficientPermission()
        
        if not datasource:
            raise DataSourceNotFound()

        await session.delete(datasource)

        await session.commit()

        return {
            "message": "Data_Source deleted"
        }