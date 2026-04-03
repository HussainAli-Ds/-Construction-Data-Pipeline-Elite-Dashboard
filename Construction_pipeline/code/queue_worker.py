import os
import shutil
from queue import Queue
from threading import Thread
from processor import process_file
from config import MAX_RETRIES, PROCESSED_DIR, FAILED_DIR
from logger import log_info, log_error

file_queue = Queue()


def worker():
    while True:
        filepath = file_queue.get()

        success = False

        for attempt in range(MAX_RETRIES):
            try:
                log_info(f"⚙️ Processing: {filepath} (Attempt {attempt+1})")

                process_file(filepath)

                # ✅ MOVE TO PROCESSED ONLY ON SUCCESS
                dest = os.path.join(PROCESSED_DIR, os.path.basename(filepath))
                if os.path.exists(filepath):
                    shutil.move(filepath, dest)

                log_info(f"📁 Moved to processed: {dest}")
                log_info(f"✅ Success: {os.path.basename(filepath)}")

                success = True
                break

            except Exception as e:
                log_error(f"❌ Retry {attempt+1} failed for {filepath}: {e}")

        # ❌ MOVE ONLY AFTER FINAL FAILURE
        if not success:
            if os.path.exists(filepath):
                failed_path = os.path.join(FAILED_DIR, os.path.basename(filepath))
                shutil.move(filepath, failed_path)

                log_error(f"📁 Moved to failed: {failed_path}")

            log_error(f"❌ FAILED permanently: {filepath}")

        file_queue.task_done()


def start_workers(num_workers=2):
    for _ in range(num_workers):
        t = Thread(target=worker, daemon=True)
        t.start()