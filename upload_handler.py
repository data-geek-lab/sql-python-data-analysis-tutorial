from mysql_config import get_connection
import pandas as pd

from mysql_config import get_connection

def save_to_mysql(df, table_name):
    conn = get_connection()
    cursor = conn.cursor()

    # Drop table if it exists
    cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")

    # Build CREATE TABLE with correct types
    columns = []
    for col in df.columns:
        dtype = "TEXT"
        if pd.api.types.is_integer_dtype(df[col]):
            dtype = "INT"
        elif pd.api.types.is_float_dtype(df[col]):
            dtype = "FLOAT"
        columns.append(f"`{col}` {dtype}")
    
    create_stmt = f"CREATE TABLE `{table_name}` ({', '.join(columns)})"
    cursor.execute(create_stmt)

    # Insert rows
    for _, row in df.iterrows():
        values = "', '".join([str(val).replace("'", "''") for val in row])
        insert_stmt = f"INSERT INTO `{table_name}` VALUES ('{values}')"
        cursor.execute(insert_stmt)

    conn.commit()
    conn.close()
