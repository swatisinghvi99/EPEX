import psycopg2
import os
import json

# Database connection details
db_config = {
    "host": "localhost",
    "port": "5432",
    "database": "eclipseoss",
    "user": "swatisinghvi",
    "password": "pass1234"    
}

def fetch_projects():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT project_name, project_url, state, technology, releases FROM eclipse_projects")
    projects = cur.fetchall()
    cur.close()
    conn.close()
    return projects

def save_project_to_json(project, base_dir):
    project_name, project_url, status, technology, releases = project
    filename = f"{project_name.replace('/', '_')}.json"  
    file_path = os.path.join(base_dir, filename)
    
    releases_data = json.loads(releases)
    
    project_data = {
        "project_name": project_name,
        "project_url": project_url,
        "status": status,
        "tech": technology,
        "releases": releases_data
    }
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, ensure_ascii=False, indent=4)

def main():
    base_dir = "UPDATED_Data/new/new_about_data"
    projects = fetch_projects()
    for project in projects:
        save_project_to_json(project, base_dir)

if __name__ == "__main__":
    main()
