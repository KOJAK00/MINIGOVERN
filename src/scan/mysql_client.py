import aiomysql
from src.common.encryption import decrypt_password

async def connect_to_mysql(datasource):

    connection = await aiomysql.connect(
        host=datasource.host,
        port=datasource.port,
        user=datasource.username,
        password=decrypt_password(datasource.encrypted_password),
        db=datasource.database_name,
    )

    return connection