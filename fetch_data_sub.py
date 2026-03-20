import requests
import pickle
import pandas as pd
import os
import sys

# Import the configuration settings
from config import DATA_URL, DATA_DIR, DATA_FILENAME_TEMPLATE


def fetch_and_save_data():
    """
    Fetches the Ballings data (which creates a 'data' DataFrame),
    then saves it locally as a pickle file using the filename
    template defined in the config file.
    """

    print(f"Starting data retrieval from {DATA_URL}...")

    try:
        # ---------------------------------------------------------
        # 1. Retrieve the remote script content
        # ---------------------------------------------------------
        response = requests.get(DATA_URL)
        response.raise_for_status()

        # ---------------------------------------------------------
        # 2. Execute the script (required — produces 'data')
        # ---------------------------------------------------------
        local_vars = {}
        exec(response.content, local_vars)

        # The Ballings script creates a variable called `data`
        data_obj = local_vars.get("data")

        if data_obj is None or not isinstance(data_obj, pd.DataFrame):
            print("Error: The Ballings script did not produce a valid DataFrame named 'data'.")
            sys.exit(1)

        # ---------------------------------------------------------
        # 3. Ensure directory exists
        # ---------------------------------------------------------
        os.makedirs(DATA_DIR, exist_ok=True)

        # Full save path (directory + template filename)
        save_path = os.path.join(DATA_DIR, DATA_FILENAME_TEMPLATE)

        # ---------------------------------------------------------
        # 4. Save the DataFrame as a pickle file
        # ---------------------------------------------------------
        with open(save_path, "wb") as f:
            pickle.dump(data_obj, f)

        print(f"Success: Saved {len(data_obj)} records to {save_path}")

        return save_path

    except requests.exceptions.RequestException as e:
        print(f"Network error while retrieving data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)



# Allow script to be run directly
if __name__ == "__main__":
    fetch_and_save_data()
