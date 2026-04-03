import os
import time
import shutil
from config import INPUT_DIR, PROCESSED_DIR, FAILED_DIR, SCAN_INTERVAL
from processor import process_file
from logger import log_info, log_error


def is_file_ready(filepath):
    """Avoid Windows file lock issue"""
    try:
        os.rename(filepath, filepath)
        return True
    except:
        return False


def start_watching():
    log_info(f"👀 Watching folder: {INPUT_DIR}")

    while True:
        try:
            files = os.listdir(INPUT_DIR)

            if not files:
                log_info("📂 No files yet...")

            for file in files:
                file_path = os.path.join(INPUT_DIR, file)

                if not (file.endswith(".xlsx") or file.endswith(".csv")):
                    continue

                if not is_file_ready(file_path):
                    continue

                try:
                    log_info(f"📥 New file detected: {file}")

                    process_file(file_path)

                    shutil.move(
                        file_path,
                        os.path.join(PROCESSED_DIR, file)
                    )

                    log_info(f"✅ Success: {file}")

                except Exception as e:
                    log_error(f"❌ Failed: {file} → {e}")

                    shutil.move(
                        file_path,
                        os.path.join(FAILED_DIR, file)
                    )

        except Exception as e:
            log_error(f"Watcher error: {e}")

        time.sleep(SCAN_INTERVAL)