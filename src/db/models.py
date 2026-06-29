from sqlmodel import SQLModel, Field,Relationship
from pydantic import EmailStr
from sqlalchemy import Column, Integer,String, Enum as SQLEnum,DateTime,Float
from .enum import UserRole,DatasetState
from datetime import datetime

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
    scan_jobs: list["ScanJob"] = Relationship(back_populates="datasource")
    datasets: list["Dataset"] = Relationship(back_populates="datasource")

class ScanJob(SQLModel, table=True):
    __tablename__ = "scan_jobs"

    id: int | None = Field(default=None, primary_key=True)
    datasource_id: int = Field(foreign_key="data_sources.id")
    status: str = Field(sa_column=Column(String(20), nullable=False, default="pending"))
    started_at: datetime | None = Field(default=None,sa_column=Column(DateTime))
    finished_at: datetime | None = Field(default=None,sa_column=Column(DateTime))

    error_message: str | None = Field(default=None,sa_column=Column(String(500)))
    datasource: "DataSource" = Relationship(back_populates="scan_jobs")
    datasets: list["Dataset"] = Relationship(back_populates="scan_job")

class DatasetTag(SQLModel, table=True):
    __tablename__ = "dataset_tags"

    dataset_id: int = Field(foreign_key="datasets.id",primary_key=True)
    tag_id: int = Field(foreign_key="tags.id",primary_key=True)

class Dataset(SQLModel, table=True):
    __tablename__ = "datasets"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(100),nullable=False))
    datasource_id: int = Field(foreign_key="data_sources.id")
    scan_job_id: int = Field(foreign_key="scan_jobs.id")
    state: DatasetState = Field(sa_type=SQLEnum(DatasetState),default=DatasetState.DRAFT,nullable=False)

    datasource: "DataSource" = Relationship(back_populates="datasets")
    scan_job: "ScanJob" = Relationship(back_populates="datasets")
    columns: list["DatasetColumn"] = Relationship(back_populates="dataset")
    tags: list["Tag"] = Relationship(back_populates="datasets",link_model=DatasetTag)

class DatasetColumn(SQLModel, table=True):
    __tablename__ = "dataset_columns"

    id: int | None = Field(default=None, primary_key=True)
    dataset_id: int = Field(foreign_key="datasets.id",ondelete="CASCADE")
    name: str = Field(sa_column=Column(String(100), nullable=False))
    data_type: str = Field(sa_column=Column(String(100), nullable=False))
    is_nullable: bool = Field(default=True)
    semantic_type: str | None = Field(default=None,sa_column=Column(String(100)))
    valid_ratio: float | None = Field(default=None)
    row_count: int = Field(default=0,sa_column=Column(Integer,nullable=False))
    null_ratio: float = Field(default=0,sa_column=Column(Float,nullable=False))

    dataset: "Dataset" = Relationship(back_populates="columns") 

class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String(100), unique=True, nullable=False))
    description: str | None = Field(default=None,sa_column=Column(String(255)))
    datasets: list["Dataset"] = Relationship(back_populates="tags",link_model=DatasetTag)