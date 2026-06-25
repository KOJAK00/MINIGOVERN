from sqlmodel import SQLModel


class CategoryCreate(SQLModel):
    name: str
    description: str | None = None

class CategoryUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
