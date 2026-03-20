import os
from dotenv import load_dotenv
from datetime import datetime

# -----------------------------------------------------------
# Load environment variables (similar to your friend’s file)
# -----------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------
# DATA ACQUISITION SETTINGS
# -----------------------------------------------------------

# Required URL for daily data extract (Ballings function)
DATA_URL = "https://ballings.co/data.py"

# Folder where the raw extracted pickle files will be saved locally
# Matches your friend's style → DATA_DIR
DATA_DIR = os.path.join("data", "raw_downloads")

# Ensure the directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# File naming pattern with date (mm-dd-yyyy.pkl)
# Matches friend’s use of "TEMPLATE" naming
DATA_FILENAME_TEMPLATE = f"raw_data_{datetime.now().strftime('%m-%d-%Y')}.pkl"


# -----------------------------------------------------------
# DATABASE SETTINGS (LOCAL POSTGRES)
# Matches your friend's DB_CONFIG structure closely
# -----------------------------------------------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": str(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")   # From .env file
}


# -----------------------------------------------------------
# PICKLE OUTPUT DIRECTORY (if exporting DB later)
# Matches style: simple constant, no functions
# -----------------------------------------------------------
PICKLE_EXPORT_DIR = os.path.join("data", "database_exports")
os.makedirs(PICKLE_EXPORT_DIR, exist_ok=True)

# Timestamped database export filename style
PICKLE_EXPORT_TEMPLATE = f"db_dump_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"


password = os.getenv("DB_PASSWORD")
print(password)