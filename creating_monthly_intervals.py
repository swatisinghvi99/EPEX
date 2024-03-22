import csv
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

# Function to generate month intervals
def month_intervals(start_date, end_date):
    intervals = {}
    current_date = start_date
    month_count = 1
    while current_date < end_date:
        next_month_date = current_date + relativedelta(months=+1)
        if next_month_date > end_date:
            next_month_date = end_date
        intervals[str(month_count)] = [current_date.strftime('%Y-%m-%d'), next_month_date.strftime('%Y-%m-%d')]
        current_date = next_month_date
        month_count += 1
    return intervals

# Directory containing the CSV files
csv_directory = '../eclipse-data/eclipse-commits-analysis-data'

# Output directory for JSON files
output_directory = 'UPDATED_Data/new/new_month_intervals'
os.makedirs(output_directory, exist_ok=True)

# Iterate over each CSV file in the directory
for csv_file_name in os.listdir(csv_directory):
    if csv_file_name.endswith('.csv'):
        csv_file_path = os.path.join(csv_directory, csv_file_name)
        
        # Read the first row from the CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            first_row = next(reader)
            project_name, start_date_str, end_date_str = first_row[:3]

        # Parse dates
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # Calculate the month intervals
        intervals = month_intervals(start_date, end_date)

        # JSON file path
        json_file_path = os.path.join(output_directory, f"{project_name}.json")

        # Save to JSON file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(intervals, json_file, indent=4)

        print(f"Monthly interval JSON created for {project_name}")
