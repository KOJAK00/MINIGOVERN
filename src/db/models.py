from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from sqlalchemy import Column, Integer,String, Enum as SQLEnum
from .enum import UserRole

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None,sa_column=Column(Integer,primary_key=True,autoincrement=True,nullable=False))
    username: str = Field(sa_column=Column(String(50),unique=True,nullable=False))
    email: EmailStr = Field(sa_column=Column(String(255),unique=True,nullable=False))
    hashed_password: str = Field(sa_column=Column(String(255),nullable=False))
    role: UserRole = Field(sa_type=SQLEnum(UserRole),nullable=False)
    is_active: bool = Field(default=False)