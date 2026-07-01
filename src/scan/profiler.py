from sqlalchemy import text

async def profile_column(
    connection,
    table_name: str,
    column_name: str,
):
    cursor = await connection.cursor()
    await cursor.execute(
        f"SELECT COUNT(*) FROM `{table_name}`"
    )
    row_count = (await cursor.fetchone())[0]
    await cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM `{table_name}`
        WHERE `{column_name}` IS NULL
        """
    )
    null_count = (await cursor.fetchone())[0]
    
    await cursor.execute(
        f"""
        SELECT `{column_name}`
        FROM `{table_name}`
        WHERE `{column_name}` IS NOT NULL
        LIMIT 20
        """
    )
    values = await cursor.fetchall()
    await cursor.close()

    if row_count == 0:
        null_ratio = 0
    else:
        null_ratio = round(null_count / row_count, 2)

    return {
        "row_count": row_count,
        "null_ratio": null_ratio,
        "sample_values": [v[0] for v in values],
    }