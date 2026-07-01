from src.db.main import async_session_maker
from src.db.models import ScanJob,DataSource,Dataset,DatasetColumn
from src.db.enum import ScanStatus
from .mysql_client import connect_to_mysql
from .service import ScanService
from .profiler import profile_column
from .semantic_detector import detect_semantic_type
from .validator import validate_countries
from src.tags.services import TagService

scan_service = ScanService()
tags_service = TagService()

AUTO_TAGS = {
    "EMAIL": ["pii"],
    "PHONE": ["pii"],
    "PERSON_NAME": ["pii"],
    "IBAN": ["sensitive"],
    "CREDIT_CARD": ["sensitive"],
}
async def run_scan(scan_job_id: int):

    connection = None
    cursor = None
    async with async_session_maker() as session:
        scan_job = await session.get(ScanJob, scan_job_id)
        if not scan_job:
            return
        
        try:
            scan_job.status = ScanStatus.RUNNING
            scan_job.error_message = None
            await session.commit()
            datasource = await session.get(
                DataSource,
                scan_job.datasource_id
            )
            if not datasource:
                raise Exception("Datasource not found.")
            await scan_service.clear_old_scan(
                datasource.id,
                session
            )
            connection = await connect_to_mysql(datasource)
            cursor = await connection.cursor()
            await cursor.execute("SHOW TABLES")
            tables = await cursor.fetchall()
            for table in tables:

                table_name = table[0]
                dataset = Dataset(
                    name=table_name,
                    datasource_id=datasource.id,
                    scan_job_id=scan_job.id,
                )
                session.add(dataset)
                await session.flush()
                await cursor.execute(
                    """
                    SELECT
                        COLUMN_NAME,
                        DATA_TYPE,
                        IS_NULLABLE
                    FROM information_schema.columns
                    WHERE table_schema=%s
                    AND table_name=%s
                    ORDER BY ORDINAL_POSITION
                    """,
                    (
                        datasource.database_name,
                        table_name,
                    ),
                )

                columns = await cursor.fetchall()
                for column in columns:

                    profile = await profile_column(connection,table_name,column[0])
                    semantic_type = detect_semantic_type(
                        profile["sample_values"],
                        column[0],
                        )
                    valid_ratio = None
                    if semantic_type == "COUNTRY":
                        valid_ratio = await validate_countries(
                            profile["sample_values"]
                            )
                    for tag in AUTO_TAGS.get(semantic_type, []):
                        await tags_service.attach_tag_to_dataset(
                            dataset.id,
                            tag,
                            session
                                    )
                    dataset_column = DatasetColumn(
                        dataset_id=dataset.id,
                        name=f"{table_name}.{column[0]}",
                        data_type=column[1],
                        is_nullable=(column[2] == "YES"),
                        row_count=profile["row_count"],
                        null_ratio=profile["null_ratio"],
                        semantic_type=semantic_type,
                        valid_ratio= valid_ratio
                    )
                    session.add(dataset_column)
            scan_job.status = ScanStatus.COMPLETED
            await session.commit()

        except Exception as e:
            await session.rollback()
            scan_job = await session.get(
                ScanJob,
                scan_job_id
            )
            if scan_job:
                scan_job.status = ScanStatus.FAILED
                scan_job.error_message = str(e)
                await session.commit()
            print(f"Scan failed: {e}")
        finally:

            if cursor is not None:
                await cursor.close()
            if connection is not None:
                connection.close()