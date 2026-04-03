import pandas as pd
import os
from db import insert_data
from logger import log_info, log_error

FILE_TABLE_MAP = {
    "machine_data": "machines_data",
    "machine_maintenance": "machines_maintenance",
    "labour_data": "labours_data",
    "material_data": "material_data",
    "progress": "progress_data",
    "site_data": "site_data"
}


def detect_table(filename):
    filename = filename.lower()

    for key in FILE_TABLE_MAP:
        if key in filename:
            return FILE_TABLE_MAP[key]

    return None


def clean_dataframe(df):
    df.columns = df.columns.str.strip().str.lower()

    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.date

    df = df.drop_duplicates()

    return df


def process_file(file_path):
    try:
        filename = os.path.basename(file_path)

        table_name = detect_table(filename)

        if not table_name:
            log_error(f"❌ Unknown file type: {filename}")
            return

        log_info(f"⚙️ Processing: {filename}")

        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        original = len(df)

        df = clean_dataframe(df)

        cleaned = len(df)

        log_info(f"📊 Rows: {original} → {cleaned}")

        insert_data(df, table_name)

        log_info(f"📦 Attempted: {cleaned} rows into {table_name}")

    except Exception as e:
        log_error(f"❌ Failed: {file_path} → {e}")
        raise e