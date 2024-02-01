import json
import os

def process_file(input_file_path, output_json_file, output_folder):
    all_data = {}
    with open(input_file_path, 'r') as file:
        for line in file:
            # Remove quotes, commas, and whitespace
            key = line.replace('"', '').replace(',', '').strip()

            # Add to the main JSON object
            all_data[key] = key

            # Individual JSON content
            individual_data = {
                "project_name": key,
                "project_url": "automotive.ambientlight",
                "alias": "ambientlight",
                "description": "",
                "sponsor": "Incubator",
                "mentor": "Garrett Rooney, Paul Querna",
                "start_date": "2006-06-06",
                "end_date": "2008-11-08",
                "status": "Incubating",
                "incubation_time": "29",
                "tech": "Automotive"
            }

            # Write individual JSON file
            individual_file_path = os.path.join(output_folder, f"{key}.json")
            with open(individual_file_path, 'w') as individual_file:
                json.dump(individual_data, individual_file, indent=4)

    # Write the combined JSON file
    with open(output_json_file, 'w') as outfile:
        json.dump(all_data, outfile, indent=4)

# File paths
input_file_path = 'list_of_projects.txt'
output_json_file = 'new_name_to_alias.json'
output_folder = 'UPDATED_Data/new/new_about_data'

# Process the file
process_file(input_file_path, output_json_file, output_folder)
