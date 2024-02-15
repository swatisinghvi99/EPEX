import psycopg2
import json

# Database connection details
db_config = {
    "host": "localhost",
    "port": "5432",
    "database": "swatis",
    "user": "swatisinghvi",
    "password": ""  # Use your actual password (if set)
}

def fetch_projects_by_technology():
    # Connect to the database
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    
    # Fetch all projects with their technology
    cur.execute("SELECT project_name, technology FROM eclipse_projects")
    projects = cur.fetchall()
    
    cur.close()
    conn.close()
    return projects

def group_projects_by_category(projects, categories):
    d = {category: [] for category in categories}
    
    for project_name, technology in projects:
        if technology in categories:  # Direct match with category
            d[technology].append(project_name)
        else:
            # Handle cases where a project's technology may not directly match the predefined categories
            for category in categories:
                if category.lower() in technology.lower():
                    d[category].append(project_name)
                    break
    
    return d

def main():
    categories = ["Automotive", "Digital Twin", "Cloud Development", "Eclipse Project", "EE4J", "Adoptium", "IoT", 
                  "LocationTech", "Modeling", "PolarSys", "RT", "SOA Platform", "Technology", "Tools", "Science", 
                  "Web Tools Platform", "AsciiDoc", "OpenHW Group", "Oniro"]
    
    projects = fetch_projects_by_technology()
    d = group_projects_by_category(projects, categories)
    
    with open('project_names.json', 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
