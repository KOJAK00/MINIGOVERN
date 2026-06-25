from fastapi import status
from src.db.models import User,Role
from src.db.redis import add_jti_to_blocklist
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import generate_password_hash,verify_password,create_access_token
from src.errors import UserAlreadyExists,InvalidCredentials
from .schemas import UserCreateModel,UserLoginModel
from fastapi.responses import JSONResponse

class UserService:
    async def get_role_id(self, role: str, session:AsyncSession):
        statement = select(Role).where(Role.name==role)
        result = await session.exec(statement)
        role_name = result.first()
        return role_name.id
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        return result.first()
    
    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)

        result = await session.exec(statement)

        return result.first()
    
    async def user_exists(self, email , session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None  else False
    
    async def username_exists(self, username, session: AsyncSession):
        user = await self.get_user_by_username(username, session)

        return True if user is not None  else False
    
    async def create_user(self, user_data: UserCreateModel,session: AsyncSession):
        id = await self.get_role_id(user_data.role,session)

        new_user = User(username=user_data.username,
                        email=user_data.email,
                        hashed_password=user_data.password,
                        role_id=id)
        new_user.hashed_password = generate_password_hash(user_data.password)
        
        if await self.user_exists(new_user.email,session):
            raise UserAlreadyExists()
        
        if await self.username_exists(new_user.username,session):
            raise UserAlreadyExists()
    
        session.add(new_user)


        await session.commit()


        return {
            "messagee":"Account Created!"
        }
    async def login_users(
        self,login_data: UserLoginModel, session: AsyncSession 
    ):
        username = login_data.username
        password = login_data.password

        user = await self.get_user_by_username(username, session)

        if user is not None:
            password_valid = verify_password(password, user.hashed_password)

            if password_valid:
                access_token = create_access_token(
                    user_data={"email": user.email, "user_id": str(user.id)}
                )

                return JSONResponse(
                    content={
                        "message": "Login successful",
                        "access_token": access_token,
                        "user": {"email": user.email, "id": str(user.id)},
                    }
                )

        raise InvalidCredentials()
    
    async def get_current_logged_user(self,user,_):
        return user
    
    async def revoke_token(self,token_details):

        jti = token_details['jti']

        await add_jti_to_blocklist(jti)

        return JSONResponse(
            content={
                "message":"Logged Out Successfully"
            },
            status_code=status.HTTP_200_OK
        )
    