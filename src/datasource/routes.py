from fastapi import APIRouter,Depends
from .schemas import DataSourceCreate,DataSourceResponse,DataSourceUpdate
from .service import DataService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.permissions import PermissionChecker
data_router = APIRouter()
data_service = DataService()

@data_router.post("/",response_model=DataSourceResponse)
async def create_datasource_route(
    data: DataSourceCreate,
    current_user=Depends(
        PermissionChecker(
            "datasources.create"
        )
    ),
    session:AsyncSession=Depends(get_session)
):
    return await data_service.create_datasource(data,current_user,session)

@data_router.get("/",response_model=list[DataSourceResponse])
async def get_datasources_route(
    current_user=Depends(
        PermissionChecker(
            "datasources.read"
        )
    ),
    session:AsyncSession=Depends(get_session)
):
    return await data_service.get_datasources(current_user,session)

@data_router.get(
    "/{datasource_id}",
    response_model=DataSourceResponse
)
async def get_datasource_route(
    datasource_id:int,
    current_user=Depends(
        PermissionChecker(
            "datasources.read")
            ),
    session:AsyncSession = Depends(get_session)      
):
    return await data_service.get_datasource(datasource_id,current_user,session)
@data_router.patch(
    "/{datasource_id}",
    response_model=DataSourceResponse
)
async def update_datasource(
    datasource_id: int,
    data: DataSourceUpdate,
    current_user= Depends(
        PermissionChecker("datasources.update")
    ),
    session :AsyncSession = Depends(get_session)
):
    return await data_service.update_datasource(datasource_id,data,current_user,session)

@data_router.delete("/{datasource_id}")
async def update_datasource(
    datasource_id: int,
    current_user= Depends(
        PermissionChecker("datasources.delete")
    ),
    session :AsyncSession = Depends(get_session)
):
    return await data_service.delete_datasource(datasource_id,current_user,session)
