from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import DataSource, Dataset,DatasetColumn
from src.scan.mysql_client import connect_to_mysql
from .utils import mask_value
from fastapi import HTTPException

class MaskingService:
    async def preview_dataset(
        self,
        dataset_id:int,
        session:AsyncSession,
        limit:int=20
    ):
        dataset=await session.get(
            Dataset,
            dataset_id
        )
        if not dataset:
            raise HTTPException(
                status_code=404,
                detail=f"Dataset with id {dataset_id} not found"
            )
        datasource = await session.get(
            DataSource,
            dataset.datasource_id
        )
        connection=await connect_to_mysql(datasource)
        cursor=await connection.cursor()
        await cursor.execute(
            f"SELECT * FROM `{dataset.name}` LIMIT {limit}"
        )
        rows=await cursor.fetchall()
        description=cursor.description
        column_names=[col[0] for col in description]
        columns=await session.exec(
            select(DatasetColumn).where(
                DatasetColumn.dataset_id==dataset.id
            )
        )
        dataset_columns=columns.all()
        semantic_map = {
        c.name.split(".")[-1]: c.semantic_type
        for c in dataset_columns
        }
        result=[]

        for row in rows:
            item={}
            for index,column_name in enumerate(column_names):
                value=row[index]
                semantic_type=semantic_map.get(column_name)
                item[column_name]=mask_value(
                    value,
                    semantic_type
                )
            result.append(item)

        await cursor.close()
        connection.close()
        return result

