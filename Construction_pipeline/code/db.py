import psycopg2
from config import DB_CONFIG
from logger import log_error, log_info

def get_connection():
    try:
        # Added sslmode for Neon Cloud and timeout for stability
        return psycopg2.connect(
            **DB_CONFIG, 
            sslmode='require', 
            connect_timeout=10
        )
    except Exception as e:
        log_error(f"❌ Connection Failed: {e}")
        raise e

def insert_data(df, table_name):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Handle generated columns and duplicates
        if table_name == "machines_maintenance":
            if "total_cost" in df.columns:
                df = df.drop(columns=["total_cost"])

        df = df.drop_duplicates()
        cols = list(df.columns)
        values = [tuple(x) for x in df.to_numpy()]

        columns = ", ".join(cols)
        placeholders = ", ".join(["%s"] * len(cols))

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.executemany(query, values)

        conn.commit()
        log_info(f"📦 Inserted into {table_name}")

    except Exception as e:
        log_error(f"❌ DB Error ({table_name}): {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()