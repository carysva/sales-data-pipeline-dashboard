import requests
import pandas as pd
import os

# Step 1: Download and load the data
url = 'http://ballings.co/data.py'
exec(requests.get(url).content)  # this creates the 'data' DataFrame

# Step 2: Define file to store data
file_path = '/Users/oliviahelms/ballings_group_777/sales_data2.csv'

# Step 3: Check if file exists
if os.path.exists(file_path):
    # Load existing data
    existing_data = pd.read_csv(file_path)
    
    # Optional: remove duplicates based on unique columns (like date + productid + region)
    combined = pd.concat([existing_data, data], ignore_index=True)
    combined.drop_duplicates(subset=['salesdate', 'productid', 'region'], keep='last', inplace=True)
    
    # Save back to CSV
    combined.to_csv(file_path, index=False)
else:
    # If file doesn't exist, save the current data
    data.to_csv(file_path, index=False)

print(f"Data saved to {file_path}")





# import requests
# import pandas as pd
# import os

# def fetch_and_store_data():
#     url = 'http://ballings.co/data.py'
#     exec(requests.get(url).content)  # creates 'data' DataFrame

#     file_path = 'sales_data.csv'

#     if os.path.exists(file_path):
#         existing_data = pd.read_csv(file_path)
#         combined = pd.concat([existing_data, data], ignore_index=True)
#         combined.to_csv(file_path, index=False)
#     else:
#         data.to_csv(file_path, index=False)

#     print("Daily data updated!")

# if __name__ == "__main__":
#     fetch_and_store_data()

