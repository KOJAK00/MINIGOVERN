from fastapi import APIRouter,Depends, status
from .services import UserService
from .schemas import UserCreateModel,UserLoginModel,UserModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .dependencies import get_current_user,IsActive,AccessTokenBearer
from src.auth.permissions import PermissionChecker
isactive=IsActive()
auth_router = APIRouter()
user_service = UserService()

@auth_router.post(
    "/create_user",  status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel,
    current_user=Depends(PermissionChecker(
        "create.user"
    )),
    session: AsyncSession = Depends(get_session)
):
    
    return await user_service.create_user(user_data,session)

@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    return await user_service.login_users(login_data,session)

@auth_router.get("/me", response_model=UserModel)
async def get_current_logged_user(
    user=Depends(get_current_user),  _: bool = Depends(isactive)
):
    return await user_service.get_current_logged_user(user,_)

@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):

    return await user_service.revoke_token(token_details)