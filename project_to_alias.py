import json

def txt_to_json(file_path, output_file):
    result = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Remove quotes and commas, and strip whitespace
            key = line.replace('"', '').replace(',', '').strip()
            result[key] = key

    # Write the JSON data to the output file
    with open(output_file, 'w') as outfile:
        json.dump(result, outfile, indent=4)

# Replace 'your_file.txt' with the path to your text file
txt_to_json('list_of_projects.txt', 'new_name_to_alias.json')