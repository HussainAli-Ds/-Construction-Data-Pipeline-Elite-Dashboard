import os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Folders
INPUT_DIR = os.path.join(BASE_DIR, "input_files")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed_files")
FAILED_DIR = os.path.join(BASE_DIR, "failed_files")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Ensure folders exist
for path in [INPUT_DIR, PROCESSED_DIR, FAILED_DIR, LOG_DIR]:
    os.makedirs(path, exist_ok=True)

# Database
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}

# Settings
CHUNK_SIZE = 5000
MAX_RETRIES = 3        # ✅ REQUIRED FOR queue_worker
SCAN_INTERVAL = 3