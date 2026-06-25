from sqlmodel import SQLModel, Field,Relationship
from pydantic import EmailStr
from sqlalchemy import Column, Integer,String, Enum as SQLEnum
from .enum import UserRole

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None,sa_column=Column(Integer,primary_key=True,autoincrement=True,nullable=False))
    username: str = Field(sa_column=Column(String(50),unique=True,nullable=False))
    email: EmailStr = Field(sa_column=Column(String(255),unique=True,nullable=False))
    hashed_password: str = Field(sa_column=Column(String(255),nullable=False))
    is_active: bool = Field(default=True)
    role_id: int = Field(foreign_key="roles.id")

    role: "Role" = Relationship(back_populates="users")
    datasources: list["DataSource"] = Relationship(back_populates="owner")
class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permissions"

    role_id: int = Field(foreign_key="roles.id",primary_key=True)
    permission_id: int = Field(foreign_key="permissions.id",primary_key=True)

class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(50),unique=True,nullable=False))
    description: str | None = Field(default=None,sa_column=Column(String(255)))
    users: list["User"] = Relationship(back_populates="role")
    permissions: list["Permission"] = Relationship(back_populates="roles",link_model=RolePermission)

class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(100),unique=True,nullable=False))
    description: str | None = Field(default=None,sa_column=Column(String(255)))  
    roles: list["Role"] = Relationship(back_populates="permissions",link_model=RolePermission)  

class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(100),unique=True,nullable=False))
    description: str | None = Field(default=None,sa_column=Column(String(255)))

    datasources: list["DataSource"] = Relationship(back_populates="category")



class DataSource(SQLModel, table=True):
    __tablename__ = "data_sources"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(100), nullable=False))
    host: str = Field(sa_column=Column(String(255), nullable=False))
    port: int = Field(default=3306)
    database_name: str = Field(sa_column=Column(String(100), nullable=False))
    username: str = Field(sa_column=Column(String(100), nullable=False))
    encrypted_password: str = Field(sa_column=Column(String(255), nullable=False))
    owner_id: int = Field(foreign_key="users.id")
    category_id: int = Field(foreign_key="categories.id")
    
    owner: "User" = Relationship(back_populates="datasources")
    category: "Category" = Relationship(back_populates="datasources")
