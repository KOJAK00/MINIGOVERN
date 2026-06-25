from pydantic import BaseModel,EmailStr
from src.db.enum import UserRole

class UserCreateModel(BaseModel):
    username: str 
    email: EmailStr 
    password: str
    role: UserRole


class UserModel (BaseModel):
    username: str
    is_active: bool
    email: EmailStr
    
class UserLoginModel(BaseModel):
    username : str
    password : str 