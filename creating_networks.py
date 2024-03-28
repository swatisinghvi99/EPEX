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

#function to process commits data from CSVs in eclipse-commits-analysis-data
def process_commit_data(csv_file_path, intervals):
    commit_details_by_month = {month: {} for month in intervals}
    commit_summary_by_month = {month: {} for month in intervals} 

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            commit_datetime = row[8]  
            commit_date = datetime.strptime(commit_datetime.split(' ')[0], '%Y-%m-%d')
            committer = row[7]
            full_file_path = row[10]
            file_name = os.path.basename(full_file_path)  
            file_type = file_name.split('.')[-1] if '.' in file_name else 'unknown'

            for month, (start, end) in intervals.items():
                if start <= commit_date.strftime('%Y-%m-%d') <= end:
                    if committer not in commit_details_by_month[month]:
                        commit_details_by_month[month][committer] = []
                    commit_details_by_month[month][committer].append({
                        'date_time': commit_datetime,
                        'file': file_name,  
                        'committer_name': committer
                    })

                    if committer not in commit_summary_by_month[month]:
                        commit_summary_by_month[month][committer] = {}
                    if file_type not in commit_summary_by_month[month][committer]:
                        commit_summary_by_month[month][committer][file_type] = 0
                    commit_summary_by_month[month][committer][file_type] += 1
                    break
    return commit_details_by_month, commit_summary_by_month

#function to process issues data from CSVs in issue-data
def process_issue_data(csv_file_path, intervals):
    issue_data_by_month = {month: [] for month in intervals}
    temp_counts = {month: {} for month in intervals}

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            created_at = datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            issue_num = row['issue_num']
            user_login = row['user_login']
            issue_type = row['type']
            project_name = row['repo_name'] 

            for month, (start, end) in intervals.items():
                if start <= created_at.strftime('%Y-%m-%d') <= end:
                    if issue_num not in temp_counts[month]:
                        temp_counts[month][issue_num] = {'issuer': None, 'commenters': {}}
                    if issue_type == "issue":
                        temp_counts[month][issue_num]['issuer'] = user_login
                    elif issue_type == "comment":
                        if user_login not in temp_counts[month][issue_num]['commenters']:
                            temp_counts[month][issue_num]['commenters'][user_login] = 0
                        temp_counts[month][issue_num]['commenters'][user_login] += 1
                    break

    for month, issues in temp_counts.items():
        for issue_num, data in issues.items():
            issuer = data['issuer']
            for commenter, count in data['commenters'].items():
                if issuer:
                    issue_data_by_month[month].append([issuer, commenter, count])

    return project_name, issue_data_by_month

def create_person_monthly_csvs(csv_file_path, project_name, intervals):
    # Loop through the intervals to ensure all month directories are created
    for month in intervals.keys():
        month_dir = os.path.join(new_monthly_issues_dir, project_name, month)
        os.makedirs(month_dir, exist_ok=True)

    # Process the issue data CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        person_data = {}  # Temporary storage for person data

        # Collect data for each person across all months
        for row in reader:
            created_at = datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            person = row['user_login']
            # Determine the month for the current row
            for month, (start, end) in intervals.items():
                if start <= created_at.strftime('%Y-%m-%d') <= end:
                    if month not in person_data:
                        person_data[month] = {}
                    if person not in person_data[month]:
                        person_data[month][person] = []
                    person_data[month][person].append(row)
                    break

    # Write the data to CSV files
    for month, persons in person_data.items():
        month_dir = os.path.join(new_monthly_issues_dir, project_name, month)
        for person, rows in persons.items():
            csv_file_path = os.path.join(month_dir, f"{person}.csv")
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['date/time', 'link', 'type', 'status'])  # Headers
                for row in rows:
                    created_at = datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    formatted_date_time = created_at.strftime('%a %b %d %H:%M:%S %Y')
                    link = row['issue_url'].replace('https://api.github.com/repos', 'https://github.com')
                    issue_type = row['type']
                    status = row.get('issue_state', 'N/A')  # Assuming 'issue_state' might not be present
                    writer.writerow([formatted_date_time, link, issue_type, status])

# Function to convert the structured commit data into the desired output format
def convert_to_desired_format(commit_data):
    formatted_data = []
    for committer, types_data in commit_data.items():
        for file_type, count in types_data.items():
            formatted_data.append([committer, file_type, count])
    return formatted_data

csv_directory = '../eclipse-data/eclipse-commits-analysis-data'
issue_csv_directory = '../eclipse-data/issue-data'

output_directory = 'UPDATED_Data/new/new_month_intervals'
commit_output_base = 'UPDATED_Data/new/new_commit'
new_monthly_commits_dir = 'UPDATED_Data/new_monthly_commits'
email_output_base = 'UPDATED_Data/new/new_issues'
new_monthly_issues_dir = 'UPDATED_Data/new_monthly_issues'

os.makedirs(output_directory, exist_ok=True)
os.makedirs(commit_output_base, exist_ok=True)
os.makedirs(new_monthly_commits_dir, exist_ok=True)
os.makedirs(email_output_base, exist_ok=True)
os.makedirs(new_monthly_issues_dir, exist_ok=True)

for csv_file_name in os.listdir(csv_directory):
    if csv_file_name.endswith('.csv'):
        csv_file_path = os.path.join(csv_directory, csv_file_name)
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                if headers is None:
                    print(f"The file {csv_file_name} is empty. Skipping.")
                    continue
                
                first_data_row = next(reader, None) 
                if first_data_row is None:
                    print(f"The file {csv_file_name} has headers but no data rows. Skipping.")
                    continue
                
                project_name, start_date_str, end_date_str = first_data_row[:3]
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                intervals = month_intervals(start_date, end_date)

            json_file_path = os.path.join(output_directory, f"{project_name}.json")
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(intervals, json_file, indent=4)
                
            commit_details_by_month_csv, commit_data_by_month = process_commit_data(csv_file_path, intervals)

            project_dir = os.path.join(commit_output_base, project_name)
            os.makedirs(project_dir, exist_ok=True)

            for month, commit_data in commit_data_by_month.items():
                json_file_path = os.path.join(project_dir, f"{project_name}_{month}.json")
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(convert_to_desired_format(commit_data), json_file, indent=4)

            project_dir_csv = os.path.join(new_monthly_commits_dir, project_name)
            os.makedirs(project_dir_csv, exist_ok=True)

            for month, committers in commit_details_by_month_csv.items():
                month_dir = os.path.join(project_dir_csv, month)
                os.makedirs(month_dir, exist_ok=True)

                for committer, commits in committers.items():
                    csv_file_path = os.path.join(month_dir, f"{committer}.csv")
                    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(['date_time', 'file', 'committer_name'])  # CSV Header

                        for commit in commits:
                            original_datetime = datetime.strptime(commit['date_time'], '%Y-%m-%d %H:%M:%S %Z')
                            formatted_datetime = original_datetime.strftime('%a %b %d %H:%M:%S %Y').replace(' 0', '  ')
                            writer.writerow([formatted_datetime, commit['file'], commit['committer_name']])

            print(f"Technical Network data created for {project_name}")
        except Exception as e:
            print(f"Failed to process file {csv_file_path}.")

for issue_csv_file_name in os.listdir(issue_csv_directory):
    if issue_csv_file_name.endswith('.csv'):
        csv_file_path = os.path.join(issue_csv_directory, issue_csv_file_name)
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader, None)  
                if headers is None:
                    print(f"The file {issue_csv_file_name} is empty. Skipping.")
                    continue
                
                first_row = next(reader, None)
                if first_row is None:
                    print(f"The file {issue_csv_file_name} has no data rows. Skipping.")
                    continue

            project_name, issue_data_by_month = process_issue_data(csv_file_path, intervals)
            create_person_monthly_csvs(csv_file_path, project_name, intervals)
            
            output_dir = os.path.join(email_output_base, project_name)
            os.makedirs(output_dir, exist_ok=True)

            for month, data in issue_data_by_month.items():
                json_file_path = os.path.join(output_dir, f"{project_name}_{month}.json")
                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, indent=4)

            print(f"Social Network data created for {project_name}")
        except Exception as e:
            print(f"Failed to process file {csv_file_path}.")
