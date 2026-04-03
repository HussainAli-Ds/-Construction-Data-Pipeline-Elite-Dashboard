import os
from datetime import datetime
from config import LOG_DIR

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")

def write_log(level, msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} {level}: {msg}\n")

def log_info(msg):
    print(msg)
    write_log("INFO", msg)

def log_error(msg):
    print(msg)
    write_log("ERROR", msg)