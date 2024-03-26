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

# Adjusted function to process commit data and correctly handle month-wise separation
def process_commit_data(csv_file_path, intervals):
    # Structure to hold commit data: {month: {committer: {file_type: count}}}
    commit_data_by_month = {month: {} for month in intervals}

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            commit_date_str = row[8]  # Assuming zero-based indexing
            commit_date = datetime.strptime(commit_date_str.split(' ')[0], '%Y-%m-%d')
            committer = row[7]
            file_path = row[10]
            file_type = file_path.split('.')[-1] if '.' in file_path else 'unknown'

            for month, (start, end) in intervals.items():
                if start <= commit_date.strftime('%Y-%m-%d') <= end:
                    if committer not in commit_data_by_month[month]:
                        commit_data_by_month[month][committer] = {}
                    if file_type not in commit_data_by_month[month][committer]:
                        commit_data_by_month[month][committer][file_type] = 0
                    commit_data_by_month[month][committer][file_type] += 1
                    break
    return commit_data_by_month

# Function to convert the structured commit data into the desired output format, per month
def convert_to_desired_format(commit_data):
    formatted_data = []
    for committer, types_data in commit_data.items():
        for file_type, count in types_data.items():
            formatted_data.append([committer, file_type, count])
    return formatted_data

csv_directory = '../eclipse-data/eclipse-commits-analysis-data'
output_directory = 'UPDATED_Data/new/new_month_intervals'
commit_output_base = 'UPDATED_Data/new/new_commit'

os.makedirs(output_directory, exist_ok=True)
os.makedirs(commit_output_base, exist_ok=True)

for csv_file_name in os.listdir(csv_directory):
    if csv_file_name.endswith('.csv'):
        try:
            csv_file_path = os.path.join(csv_directory, csv_file_name)
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                first_row = next(reader)
                project_name, start_date_str, end_date_str = first_row[:3]

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            intervals = month_intervals(start_date, end_date)
            json_file_path = os.path.join(output_directory, f"{project_name}.json")

            # Save to JSON file
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(intervals, json_file, indent=4)
            commit_data_by_month = process_commit_data(csv_file_path, intervals)

            project_dir = os.path.join(commit_output_base, project_name)
            os.makedirs(project_dir, exist_ok=True)

            for month, commit_data in commit_data_by_month.items():
                json_file_path = os.path.join(project_dir, f"{project_name}_{month}.json")
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(convert_to_desired_format(commit_data), json_file, indent=4)

            print(f"Monthly commit JSONs created for {project_name}")
        except Exception as e:
            print(f"Failed to process file {csv_file_path}. Error: {e}")
