from sqlmodel import SQLModel

class DataSourceCreate(SQLModel):
    name: str
    host: str
    port: int = 3306
    database_name: str
    username: str
    password: str
    category_id: int

class DataSourceUpdate(SQLModel):
    name: str | None = None
    host: str | None = None
    port: int | None = None
    database_name: str | None = None
    username: str | None = None
    password: str | None = None
    category_id: int | None = None

class DataSourceResponse(SQLModel):
    id: int
    name: str
    host: str
    port: int
    database_name: str
    username: str
    category_id: int
    owner_id: int