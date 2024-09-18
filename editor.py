import json
import pandas as pd
from datetime import datetime
import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def create_csv_file(data: dict):
    if not data:
        raise "No data for create CSV file"
    now = datetime.now()
    time_format = now.strftime("%H%M%S%d%m%Y")
    lengths = [len(v) for v in data.values()]
    if len(set(lengths)) != 1:
        raise ValueError("All columns must have the same number of elements")
    file_path = fr"C:\GIT\SAM\csv_files\stress_result_{time_format}.csv"
    print(file_path)
    data_frame = pd.DataFrame(data)
    data_frame.to_csv(file_path, index=False)

# Data to be written to the CSV file
csv_data = {
    'Title': [
        'Requests in total',
        'Total requests time (seconds)',
        'Time in total (seconds)',
        'Error rate (%)',
        'Average time for one request (seconds)',
        'Max time for one request (seconds)',
        'Min time for one request (seconds)',
        'P90 time measure (seconds)'
    ],
    'Results': [None, None, None, None, None, None, None, None]
}

# create_csv_file(csv_data)
