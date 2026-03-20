import pandas as pd
import pickle
import os
import glob
import sys
from sqlalchemy import create_engine, types
from sqlalchemy.engine import URL

# Import configuration from config.py
from config import DB_CONFIG, DATA_DIR


# -------------------------------------------------------------------
# 1. SCHEMA MAPPING (mimics your friend’s DAILY_DATA_SCHEMA structure)
# -------------------------------------------------------------------
# The Ballings dataset has consistent column names, so we map them here.
# Adjust if your dataset contains additional columns.
DATA_SCHEMA = {
    'date': types.DateTime(),        # timestamp column
    'product_id': types.Integer(),   # integer
    'quantity': types.Integer(),     # integer
    'price': types.Float(),          # float
    'customer_id': types.Integer(),  # integer
}


# -------------------------------------------------------------------
# 2. Find the most recent pickle file in DATA_DIR
# -------------------------------------------------------------------
def find_latest_data_file(data_directory):
    """
    Finds the most recently saved pickle file in the data directory.
    Matches friend's logic exactly: glob → check → max() by modification time.
    """
    search_path = os.path.join(data_directory, "*.pkl")
    files = glob.glob(search_path)

    if not files:
        print(f"Error: No pickle files found in {data_directory}")
        sys.exit(1)

    latest_file = max(files, key=os.path.getmtime)
    print(f"Found latest data file: {latest_file}")
    return latest_file


# -------------------------------------------------------------------
# 3. Load the pickle file into a Pandas DataFrame
# -------------------------------------------------------------------
def load_data(file_path):
    """
    Loads a pickle file containing a Pandas DataFrame.
    Matches friend’s strict checking and prints record count.
    """
    try:
        with open(file_path, "rb") as f:
            df = pickle.load(f)

        if not isinstance(df, pd.DataFrame):
            raise TypeError("Loaded object is not a Pandas DataFrame.")

        print(f"Successfully loaded data. Total records: {len(df)}")
        return df

    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        sys.exit(1)


# -------------------------------------------------------------------
# 4. Insert the DataFrame into local PostgreSQL
# -------------------------------------------------------------------
def insert_records(df, table_name, dtype_map):
    """
    Inserts the DataFrame into a PostgreSQL database using SQLAlchemy.
    Follows the same style and function structure as your friend's code.
    """
    try:
        url = URL.create(
            drivername="postgresql",
            username=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=int(DB_CONFIG["port"]),
            database=DB_CONFIG["dbname"]
        )

        engine = create_engine(url)

        df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            dtype=dtype_map
        )

        print(f"Successfully inserted {len(df)} records into table '{table_name}'.")

    except Exception as e:
        print(f"Database insertion failed: {e}")
        sys.exit(1)


# -------------------------------------------------------------------
# MAIN EXECUTION (matches friend's structure exactly)
# -------------------------------------------------------------------
if __name__ == "__main__":

    # 1. Find most recent pickle file
    latest_file = find_latest_data_file(DATA_DIR)

    # 2. Load DataFrame
    df = load_data(latest_file)

    # 3. Insert into database
    TARGET_TABLE = "data_daily"
    insert_records(df, TARGET_TABLE, DATA_SCHEMA)
