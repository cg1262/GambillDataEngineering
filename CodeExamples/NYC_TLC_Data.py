import requests
import os
from datetime import datetime
import time
# Directory to save files
save_dir = "D:/nyc_tlc_data"
os.makedirs(save_dir, exist_ok=True)

# Base URL for NYC TLC data (e.g., Yellow Taxi)
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/{DataSet}_{year}-{month:02}.parquet"

# Date range for data
start_year = 2019  # starting year
end_year = 2023    # ending year
datasets = [#'yellow_tripdata'
            #,'green_tripdata',
            'fhv_tripdata'] #TLC datasets
# Function to download a single file
def download_data(Dataset,year, month):
    url = base_url.format(DataSet=Dataset,year=year, month=month)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = f"{save_dir}/{Dataset}_{year}-{month:02}.parquet"
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {filename}")
        return_value = response.status_code
    else:
        print(f"Failed to download data for {year}-{month:02} (Status code: {response.status_code})")
        return_value = response.status_code
    return return_value
#loop through datasets
for ds in datasets:
    # Loop over years and months
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # Only download data up to the current month of the current year
            if year == datetime.now().year and month > datetime.now().month:
                break
            dd = download_data(ds,year, month)
            while dd == 403:
                time.sleep(5)
                dd = download_data(ds,year, month)

print("Download complete.")