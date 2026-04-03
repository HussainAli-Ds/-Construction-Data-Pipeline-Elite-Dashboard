import psycopg2
from config import DB_CONFIG
from logger import log_error, log_info

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def insert_data(df, table_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # ❌ REMOVE GENERATED COLUMN
        if table_name == "machines_maintenance":
            if "total_cost" in df.columns:
                df = df.drop(columns=["total_cost"])

        # ❌ REMOVE DUPLICATES BEFORE INSERT (FULL ROW)
        df = df.drop_duplicates()

        cols = list(df.columns)
        values = [tuple(x) for x in df.to_numpy()]

        columns = ", ".join(cols)
        placeholders = ", ".join(["%s"] * len(cols))

        query = f"""
        INSERT INTO {table_name} ({columns})
        VALUES ({placeholders})
        """

        cursor.executemany(query, values)

        conn.commit()
        cursor.close()
        conn.close()

        log_info(f"📦 Inserted into {table_name} (duplicates handled)")

    except Exception as e:
        log_error(f"❌ DB Error ({table_name}): {e}")
        raise e