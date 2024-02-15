import psycopg2
import os
import json

# Database connection details
db_config = {
    "host": "localhost",
    "port": "5432",
    "database": "swatis",
    "user": "swatisinghvi",
    "password": ""  
}

def fetch_projects():
    # Connect to the database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT project_name, project_url, state, technology, releases FROM eclipse_projects")
    projects = cur.fetchall()
    cur.close()
    conn.close()
    return projects

def save_project_to_json(project, base_dir):
    project_name, project_url, status, technology, releases = project
    # Sanitize project_name to create a valid filename
    filename = f"{project_name.replace('/', '_')}.json"  # Replace any slashes to avoid path issues
    file_path = os.path.join(base_dir, filename)
    
    # Parse the releases JSON string back into a Python object
    releases_data = json.loads(releases)
    
    # Create the project data dictionary
    project_data = {
        "project_name": project_name,
        "project_url": project_url,
        "status": status,
        "tech": technology,
        "releases": releases_data
    }
    
    # Ensure the base directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Write the JSON data to a file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, ensure_ascii=False, indent=4)

def main():
    base_dir = "UPDATED_Data/new/new_about_data"
    projects = fetch_projects()
    for project in projects:
        save_project_to_json(project, base_dir)

if __name__ == "__main__":
    main()
