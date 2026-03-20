import requests
import pandas as pd
import os

url = 'http://ballings.co/data.py'

# Safe exec environment
local_vars = {}
exec(requests.get(url).content, {}, local_vars)

if "data" not in local_vars:
    raise ValueError("ERROR: 'data' was not created from the URL.")

data = pd.DataFrame(local_vars["data"])

file_path = '/Users/katiewatts/ballings_group_777/sales_data2.csv'

# If file exists
if os.path.exists(file_path):
    try:
        existing_data = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        existing_data = pd.DataFrame()   # handle empty file

    combined = pd.concat([existing_data, data], ignore_index=True)
    combined.drop_duplicates(subset=['salesdate', 'productid', 'region'], keep='last', inplace=True)
    combined.to_csv(file_path, index=False)

else:
    data.to_csv(file_path, index=False)

print(f"Data saved to {file_path}")

